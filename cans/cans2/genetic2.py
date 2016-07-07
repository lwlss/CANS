import numpy as np
import time
import random
import inspyred


from cans2.plate import Plate
from cans2.cans_funcs import frexp_10, pickleable
from cans2.guesser import fit_imag_neigh
from cans2.model import CompModel, CompModelBC
from cans2.fitter import Fitter


# Generator functions for evolutionary strategy.
def gen_random_uniform(random, args):
    """Generate random parameters between the bounds.

    random : A numpy RandomState object seeded with current system
    time upon instatiation.

    bounds : Contained in the args dict. A 2d array of lower and upper
    bounds for each parameter in the model.

    For all parameters values are sampled from a uniform distribution
    in linear space.

    """
    bounds = args.get("gen_kwargs")["bounds"]
    # Random uniform. For b we could use N(mean, var) (clipped above zero) and
    # could even randomize mean and var.
    params = [random.uniform(l, h) for l, h in zip(bounds[:, 0], bounds[:, 1])]
    return params


def gen_random_uniform_log_C(random, args):
    """Generate random parameters between the bounds.

    random : A numpy RandomState object seeded with current system
    time upon instatiation.

    bounds : Contained in the args dict. A 2d array of lower and upper
    bounds for each parameter in the model.

    For the initial concentration of cells, the exponent is sampled
    over a uniform space and it is assumed that the mantissas of the
    lower and upper bounds are equal. For all other parameters,
    values are sampled from uniform distributions in linear space.

    """
    bounds = args.get("bounds")
    params = [random.uniform(l, h) for l, h in zip(bounds[:, 0], bounds[:, 1])]
    C_0_mantissa, C_0_exp = frexp_10(bounds[0])
    exponent = random.uniform(C_0_exp[0], C_0_exp[1])
    params[0] = C_0_mantissa[0]*10.0**exponent
    return params


# This will be quite slow for a large population. Can we use
# multiprocessing?
def gen_imag_neigh_guesses(random, args):
    """Generate parameters from imaginary neighbour guesses.

    These guesses are obtained from "quick" fits of a simplified
    "imaginary neighbour" model. The quick fits also also require
    starting guesses for the ratio of starting to final cell
    concentration, the ratio of edge to internal culture area, and an
    approximate magnitude of growth parameter b. These are sampled
    randomly from uniform distributions between the bounds. For the
    case of cell ratios samples are taken from the logspace.

    """
    gen_kwargs = args.get("gen_kwargs")

    area_range = gen_kwargs["area_range"]
    C_range = gen_kwargs["C_range"]
    b_range = gen_kwargs["b_range"]

    area_ratio = random.uniform(area_range[0], area_range[1])
    C_0_mantissa, C_0_exp = frexp_10(C_range)
    exponent = random.uniform(C_0_exp[0], C_0_exp[1])
    C_ratio = C_0_mantissa[0]*10.0**exponent
    b_guess = random.uniform(b_range[0], b_range[1])

    # Necessary for multiprocessing as Models cannot be pickled.
    potential_models = [CompModel(), CompModelBC()]
    for model in potential_models:
        if gen_kwargs["imag_neigh_kwargs"]["plate_model"] == model.name:
            gen_kwargs["imag_neigh_kwargs"]["plate_model"] = model

    guess_kwargs = gen_kwargs["imag_neigh_kwargs"]    # Obviously do not unpack.
    guess_kwargs["area_ratio"] = area_ratio
    guess_kwargs["C_ratio"] = C_ratio
    guess_kwargs["imag_neigh_params"][-2:] = [b_guess*1.5, b_guess]

    guess, guesser = fit_imag_neigh(**guess_kwargs)
    return list(guess)    # AttributeError: 'numpy.ndarray' object has no attribute 'extend'.


# Functions for evaluating the candidates.
def evaluate_fit(candidates, args):
    # Evaluate the objective function for each set of canditate
    # parameters and return this as the fitness. Here fitter and plate
    # are defined outside the scope of the function.
    fitter = args.get("fitter")
    plate = args.get("plate")
    return [fitter._rr_obj_no_scaling(plate, cs) for cs in candidates]


@inspyred.ec.evaluators.evaluator
def evaluate_b_candidate(candidate, args):
    """Evaluate the objective function of a candidate of b parameters.

    Allows multiprocessing, but has a bit of an overhead because SWIG
    objects produced by roadrunner cannot be pickled. I have been able
    to wrap the RoadRunner class so that it can be pickled (see
    http://stackoverflow.com/a/9325185) but not the attribute
    RoadRunner.ExecutableModel. As a result the ExecutableModel must
    be set inside the function using roadrunner.RoadRunner.load()
    which is more than 10x slower than solving for a full
    plate. Therefore more than 10 cores will be needed to see any
    benefit.

    Plate level parameters should be contained in the dictionary
    "eval_kwargs" and passed in through args. They can be simply a
    random guess or evolved at a higher level.

    """
    eval_kwargs = args.get("eval_kwargs")
    params = np.concatenate((eval_kwargs["plate_lvl"], candidate))
    plate = eval_kwargs["plate"]
    plate.rr.load(eval_kwargs["sbml"])
    fitter = eval_kwargs["fitter"]
    return fitter._rr_obj_no_scaling(plate, params)


def evaluate_b_candidates(candidates, args):
    """Evaluate all b_canditates without multiprocessing.

    The roadrunner model should already be loaded on the plate object
    using dummy parameter values.

    """
    eval_kwargs = args.get("eval_kwargs")
    plate_lvl = eval_kwargs["plate_lvl"]
    params = (np.concatenate((plate_lvl, bs)) for bs in candidates)
    plate = eval_kwargs["plate"]
    fitter = eval_kwargs["fitter"]    # Should contain a Model attribute
    return [fitter._rr_obj_no_scaling(plate, p) for p in params]


# @inspyred.ec.utilities.memoize(maxlen=100)    # cache up to last 100 return values.
@inspyred.ec.evaluators.evaluator
def evaluate_with_grad_fit(candidate, args):
    """Gradient fitting using a candidate initial guess.

    For multiprocessing, args must be
    pickleable. SwigPyObject/RoadRunner objects are not pickleable so
    I have to create new Plate objects and set the roadrunner
    attribute each time (or rewrite Plate so that the RoadRunner
    object is never an attribute). This has a low overhead compared to
    the minimization and is a lot easier than finding ways to pickle
    the objects/methods.

    """
    eval_kwargs = args.get("eval_kwargs")
    plate = Plate(**eval_kwargs["plate_kwargs"])

    # Necessary for multiprocessing as Models cannot be pickled.
    models = [CompModel(), CompModelBC()]    # potential models.
    model = next((m for m in models if m.name == eval_kwargs["model"]))
    plate.set_rr_model(model, candidate)

    # Now need to fit using.
    bounds = eval_kwargs["bounds"]
    est = plate.fit_model(model, param_guess=candidate, bounds=bounds,
                          rr=True, minimizer_opts={"disp": False})
    # candidate.fitted_params = est.x   # Cannot add attribute to a list.
    return est.fun


def evolver(generator, evaluator, bounds, args,
            pop_size=100, max_evals=1000,
            tau=None, tau_prime=None, epsilon=0.00001):
    """Run an evolutionary strategy using serial processing."""
    seed = int(time.time())
    rand = random.Random(seed)
    with open("seeds.txt", 'a') as f:
        f.write("{0}\n".format(seed))
    es = inspyred.ec.ES(rand)
    es.observer = inspyred.ec.observers.stats_observer
    es.terminator = [inspyred.ec.terminators.evaluation_termination,
                     inspyred.ec.terminators.diversity_termination]
    final_pop = es.evolve(generator=generator,
                          evaluator=evaluator,
                          pop_size=pop_size,
                          maximize=False,
                          bounder=inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
                          max_evaluations=max_evals,
                          tau=tau,
                          tau_prime=tau_prime,
                          epsilon=epsilon,
#                          mutation_rate=mut_rate,
                          # Other arguments for generator and evaluator.
                          **args)
    return final_pop


def mp_evolver(generator, evaluator, bounds, args,
               cpus=4, pop_size=100, max_evals=100,
               tau=None, tau_prime=None, epsilon=0.00001):
    """Run an evolutionary strategy using multiprocessing."""
    pickleable(args)    # Necessary for multiprocessing.
    seed = int(time.time())
    rand = random.Random(seed)
    with open("seeds.txt", 'a') as f:
        f.write("{0}\n".format(seed))
    es = inspyred.ec.ES(rand)
    es.observer = inspyred.ec.observers.stats_observer
    es.terminator = [inspyred.ec.terminators.evaluation_termination,
                     inspyred.ec.terminators.diversity_termination]
    final_pop = es.evolve(generator=generator,
                          evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                          mp_evaluator=evaluator,
                          mp_num_cpus=cpus,
                          pop_size=pop_size,
                          maximize=False,
                          bounder=inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
                          max_evaluations=max_evals,
                          tau=tau,
                          tau_prime=tau_prime,
                          epsilon=epsilon,
                          # Other arguments for generator and evaluator.
                          **args)
    return final_pop

# Also want to try a particle swarm


def custom_evolver(generator, evaluator, bounds, args,
                   pop_size=100, num_selected=100, max_evals=1000,
                   mut_rate=1.0, crowd_dist=10):
    seed = int(time.time())
    rand = random.Random(seed)
    with open("seeds.txt", 'a') as f:
        f.write("{0}\n".format(seed))
    ea = inspyred.ec.EvolutionaryComputation(rand)
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.replacer = inspyred.ec.replacers.crowding_replacement
    ea.variator = inspyred.ec.variators.gaussian_mutation
    ea.observer = inspyred.ec.observers.stats_observer
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    final_pop = ea.evolve(generator=generator,
                          evaluator=evaluator,
                          pop_size=pop_size,
                          maximize=False,
                          bounder=inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
                          max_evaluations=max_evals,
                          num_selected=num_selected,
                          mutation_rate=mut_rate,
                          crowding_distance=crowd_dist,
                          #distance_function=,
                          **args)
    return final_pop
