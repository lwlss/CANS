import numpy as np
import time
import random
import inspyred


import cans2.genetic_kwargs as kwargs


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
    bounds = args.get("gen_kwargs")["bounds"]
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
def eval_candidates(candidates, args):
    """Evaluate the objective function for parameter canditates.

    Candidates should have values for all parameters in the model.

    """
    eval_kwargs = args.get("eval_kwargs")
    fitter = eval_kwargs["fitter"]
    plate = eval_kwargs["plate"]
    return [fitter._rr_obj_no_scaling(plate, cs) for cs in candidates]


@inspyred.ec.evaluators.evaluator
def eval_b_candidate(candidate, args):
    """Evaluate the objective function for a candidate of b parameters.

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


def eval_b_candidates(candidates, args):
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


@inspyred.ec.evaluators.evaluator
def eval_plate_lvl(candidate, args):
    """Evaluate the objective function for a candidate parameters.

    Candidates are plate level parameters (e.g. [C_0, N_0, NE_0,
    kn]). Evolution is hierarchical with culture level parameters
    (e.g. bs) evoled at a lower level inside this function. The
    procedure may be parallelized on the plate level. On the culture
    level, overheads arrise due to issues with pickleing roadrunner's
    SWIG objects. Therefore, the culture level is evolved in series.

    """
    eval_kwargs = args.get("eval_kwargs")

    # kwargs supplied to make c level eval kwargs (convoluted).
    c_eval_kwargs_kwargs = eval_kwargs["c_lvl_make_kwargs_kwargs"]
    c_eval_kwargs_kwargs["plate_lvl"] = candidate

    # Retrieve the culture level evolver and evolver_kwargs.
    c_evolver = eval_kwargs["c_evolver"]
    evolver = c_evolver["evolver"]
    evolver_kwargs = c_evolver["evolver_kwargs"]

    # Make culture level evolver args.
    c_args = {
        "gen_kwargs": {"bounds": evolver_kwargs["bounds"]},
        "eval_kwargs": kwargs.make_eval_b_candidates_kwargs(**c_eval_kwargs_kwargs)
        }
    # Add args, which includes the unpickleable objects, to the evolver kwargs.
    evolver_kwargs["args"] = c_args

    # Call the culture_level evolver
    final_pop = evolver(**evolver_kwargs)
    fitness = min(final_pop).fitness
    return fitness    # Can we also return the candidate attribute somehow?


@inspyred.ec.evaluators.evaluator
def eval_plate_lvl_im_neigh_grad(candidate, args):
    """Evaluate a candidate of plate level parameters and b_guess.

    Uses imaginary neighbour model guessing and gradient fitting
    (parallelizeable). In the gradient fit, the candidate plate level
    parameters are fixed and culture level b values are estimated. The
    initial guess of b parameters for the gradient fit come from
    imaginary neighbour guessing.

    candidate : Plate level parameters and b_guess. b_guess is for the
    imaginary neighbour guesser and is essentially evolving the
    initial guesser. The supplied candidiate plate level parameters
    and the guessed bs are returned by the imaginiary neighbour guesser.

    """
    eval_kwargs = args.get("eval_kwargs")
    plate_lvl = candidate[:-1]
    b_guess = candidate[-1]

    plate = eval_kwargs["plate"]
    model = eval_kwargs["model"]
    imag_neigh_params = eval_kwargs["imag_neigh_params"]

    # Use candidate b_guess and plate level parameters in imaginary
    # neighbour guess.
    imag_neigh_params[-2:] = np.array([b_guess*1.5, b_guess])
    params, guesser = fit_imag_neigh(plate, model,
                                     area_ratio=None,
                                     C_ratio=None,
                                     imag_neigh_params=imag_neigh_params,
                                     plate_lvl=plate_lvl)

    # Now fit with grad method starting with guessed parameters.
    plate.set_rr_model(model, params)
    plate_lvl_bounds = np.array([[param]*2 for param in plate_lvl])
    b_bounds = eval_kwargs["b_bounds"]
    bounds = np.concatenate((plate_lvl_bounds, b_bounds))
    est = plate.fit_model(model, param_guess=params, bounds=bounds,
                          rr=True, minimizer_opts={"disp": False})
    # candidate.fitted_params = est.x   # Cannot add attribute to a list.
    return est.fun


# # @inspyred.ec.utilities.memoize(maxlen=100)    # cache up to last 100 return values.
# @inspyred.ec.evaluators.evaluator
# def evaluate_with_grad_fit(candidate, args):
#     """Gradient fitting using a candidate initial guess.

#     For multiprocessing, args must be
#     pickleable. SwigPyObject/RoadRunner objects are not pickleable so
#     I have to create new Plate objects and set the roadrunner
#     attribute each time (or rewrite Plate so that the RoadRunner
#     object is never an attribute). This has a low overhead compared to
#     the minimization and is a lot easier than finding ways to pickle
#     the objects/methods.

#     """
#     eval_kwargs = args.get("eval_kwargs")
#     plate = Plate(**eval_kwargs["plate_kwargs"])

#     # Necessary for multiprocessing as Models cannot be pickled.
#     models = [CompModel(), CompModelBC()]    # potential models.
#     model = next((m for m in models if m.name == eval_kwargs["model"]))
#     plate.set_rr_model(model, candidate)

#     # Now need to fit using.
#     bounds = eval_kwargs["bounds"]
#     est = plate.fit_model(model, param_guess=candidate, bounds=bounds,
#                           rr=True, minimizer_opts={"disp": False})
#     # candidate.fitted_params = est.x   # Cannot add attribute to a list.
#     return est.fun


def evolver(generator, evaluator, bounds, args, random,
            pop_size=100, max_evals=1000,
            tau=None, tau_prime=None, epsilon=0.00001):
    """Run an evolutionary strategy using serial processing."""
    es = inspyred.ec.ES(random)
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
                          # mutation_rate=mut_rate,
                          # Other arguments for generator and evaluator.
                          **args)
    return final_pop


def es_mp_evolver(generator, evaluator, bounds, args, random,
                  cpus=4, pop_size=100, max_evals=100,
                  tau=None, tau_prime=None, epsilon=0.00001):
    """Run an evolutionary strategy using multiprocessing."""
    pickleable(args)    # Necessary for multiprocessing.
    es = inspyred.ec.ES(random)
    es.observer = [inspyred.ec.observers.stats_observer,
                   inspyred.ec.observers.best_observer]
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


def dea_mp_evolver(generator, evaluator, bounds, args, random, cpus=4,
                   pop_size=50, max_evals=100, num_selected=2,
                   tournament_size=2, crossover_rate=1.0,
                   mutation_rate=0.1, gaussian_mean=0,
                   gaussian_stdev=1):
    """Run an differential evolutionary algorithm using multiprocessing."""
    pickleable(args)    # Necessary for multiprocessing.
    dea = inspyred.ec.DEA(random)
    dea.observer = [inspyred.ec.observers.stats_observer,
                   inspyred.ec.observers.best_observer]
    dea.terminator = [inspyred.ec.terminators.evaluation_termination,
                     inspyred.ec.terminators.diversity_termination]
    dea.replacer = inspyred.ec.replacers.plus_replacement
    final_pop = dea.evolve(generator=generator,
                          evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                          mp_evaluator=evaluator,
                          mp_num_cpus=cpus,
                          pop_size=pop_size,
                          maximize=False,
                          bounder=inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
                          max_evaluations=max_evals,
                          num_selected=num_selected,
                          tournament_size=tournament_size,
                          crossover_rate=crossover_rate,
                          mutation_rate=mutation_rate,
                          guassian_mean=gaussian_mean,
                          gaussian_stdev=gaussian_stdev,
                          # Other arguments for generator and evaluator.
                          **args)
    return final_pop





def custom_mp_evolver(generator, evaluator, bounds, args, random, cpus=4,
                      pop_size=100, num_selected=100, max_evals=1000,
                      mut_rate=1.0, crowd_dist=10):
    ea = inspyred.ec.EvolutionaryComputation(random)
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.replacer = inspyred.ec.replacers.crowding_replacement
    ea.variator = inspyred.ec.variators.gaussian_mutation
    ea.observer = [inspyred.ec.observers.stats_observer]
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    final_pop = ea.evolve(generator=generator,
                          evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                          mp_evaluator=evaluator,
                          mp_num_cpus=cpus,
                          pop_size=pop_size,
                          maximize=False,
                          bounder=inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
                          max_evaluations=max_evals,
                          num_selected=num_selected,
                          mutation_rate=mut_rate,
                          crowding_distance=crowd_dist,
                          # distance_function=,
                          **args)
    return final_pop


def custom_evolver(generator, evaluator, bounds, args, random, observer=None,
                   pop_size=100, num_selected=100, max_evals=1000,
                   mut_rate=1.0, crowd_dist=10):
    ea = inspyred.ec.EvolutionaryComputation(random)
    ea.selector = inspyred.ec.selectors.tournament_selection
    ea.replacer = inspyred.ec.replacers.crowding_replacement
    ea.variator = inspyred.ec.variators.gaussian_mutation
    # Allows us to silence internal observers in hierarchical evolvers
    # by supplying observer=[].
    if observer is None:
        ea.observer = [inspyred.ec.observers.stats_observer,
                       inspyred.ec.observers.best_observer]
    else:
        ea.observer = observer
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
                          # distance_function=,
                          **args)
    return final_pop


def get_seed_and_prng(seed_file, seed=None):
    """Return a seed and a pseudo-random number generator.

    seed_file : Path for file to save the seed.

    seed : A seed for the prng. If a seed is not supplied one is
    generatd from the system time.

    To allow reproducibility, the user should save the seed with any
    generated results. Obviously, this will not work if the evaluator
    is non-deterministic.

    """
    if seed is None:
        seed = int(time.time())
    rand = random.Random(seed)
    with open(seed_file, 'a') as f:
        f.write("{0}\n".format(seed))
    return seed, rand
