import numpy as np
import json

# Inspyred imports
import time
import random
import inspyred
# from inspyred import ec
# from inspyred.ec import terminators
from cans2.fitter import Fitter


from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.guesser import fit_imag_neigh
from cans2.plotter import Plotter
from cans2.cans_funcs import dict_to_json, dict_to_numpy, frexp_10


# # Simulate a small 3x3 plate with noise using CompModelBC or CompModel.
# rows = 3
# cols = 3
# times = np.linspace(0, 5, 11)
# model = CompModelBC()
# plate = Plate(rows, cols)
# plate.times = times

# C_ratio = 1e-4
# area_ratio = 1.4
# N_0 = 0.1
# b_guess = 45.0
# custom_params = {
#     "C_0": N_0*C_ratio,
#     "N_0": N_0,
#     "NE_0": N_0*area_ratio,
#     "kn": 1.0,
# }
# plate.set_sim_data(model, b_mean=50.0, b_var=30.0,
#                    custom_params=custom_params, noise=True)

# plotter = Plotter(model)
# plotter.plot_est_rr(plate, plate.sim_params,
#                     title="Sim timecourse", sim=False)

# # Starting guess from fits of the imaginary neighbour model.
# imag_neigh_params = np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess])

# guess, guesser = fit_imag_neigh(plate, model, area_ratio, C_ratio,
#                                 imag_neigh_params,
#                                 kn_start=0.0, kn_stop=8.0, kn_num=21)
# plotter.plot_est_rr(plate, guess, title="Imaginary Nieghbour Guess", sim=True)
# bounds = guesser.get_bounds(guess, C_doubt=1e2, N_doubt=2.0, kn_max=10.0)
# print(bounds)

# # Fit using gradient method.
# minimizer_opts = {"disp": True}
# plate.grad_est = plate.fit_model(model, guess, bounds=bounds, rr=True,
#                                  minimizer_opts=minimizer_opts)
# plotter.plot_est_rr(plate, plate.grad_est.x, title="Gradient Fit", sim=True)


# # Save data so that we do not have to run the above code every time
# # and debugging the genetic algorithm is quicker.
# data = {
#     "rows": rows,
#     "cols": cols,
#     "times": times,
#     "sim_params": plate.sim_params,
#     "c_meas": plate.c_meas,
#     "sim_amounts": plate.sim_amounts,
#     "guess": guess,
#     "bounds": bounds,
#     "grad_est": plate.grad_est.x,
#     }
# with open("temp_sim_and_est_data.json", 'w') as f:
#      json.dump(dict_to_json(data), f)



# Construct a genetic algorithm to fit and compare with the current
# gradient method.


def gen_random_uniform(random, args):
    """Generate random parameters between the bounds.

    random : A numpy RandomState object seeded with current system
    time upon instatiation.

    bounds : Contained in the args dict. A 2d array of lower and upper
    bounds for each parameter in the model.

    For all parameters values are sampled from a uniform distribution
    in linear space.

    """
    bounds = args.get("bounds")
    params = [random.uniform(l, h) for l, h in zip(bounds[:, 0], bounds[:, 1])]
    print(len(params))
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
    params = random.uniform(low=bounds[:, 0], high=bounds[:, 1])
    C_0_mantissa, C_0_exp = frexp_10(bounds[0])
    exponent = random.uniform(low=C_0_exp[0], high=C_0_exp[1])
    params[0] = C_0_matissa[0]*10.0**exponent
    return params


# Define C ranges to sample from.
# C_ratio = 1e-4
# C_doubt = 1e3
# b_guess = 45    # Arbitrary placeholder b_guess for imag_neigh_params[-2:].
# # Create args needed for below function (to be passed in args).
# guess_kwargs = {
#     "plate": plate,
#     "plate_model": model,
#     "C_ratio": C_ratio,    # Guess of init_cells/final_cells.
#     "kn_start": 0.0,
#     "kn_stop": 2.0,
#     "kn_num": 21,
#     "area_ratio": 1.5,    # Initial dummy val.
#     # ['kn1', 'kn2', 'b-', 'b+', 'b']
#     "imag_neigh_params": np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess]),
#     "no_neighs": None,    # If None calculated as np.ceil(C_f_max/N_0_guess).
# }
# area_range = np.array([1.0, 2.0])
# C_range = np.array([C_ratio/C_doubt, C_ratio*C_doubt])
# b_range = np.array([0.0, 200.0])
def generete_params_from_guesses(random, args):
    """Generate parameters from imaginary neighbour guesses.

    These guesses are obtained from "quick" fits of a simplified
    "imaginary neighbour" model. The quick fits also also require
    starting guesses for the ratio of starting to final cell
    concentration, the ratio of edge to internal culture area, and an
    approximate magnitude of growth parameter b. These are sampled
    randomly from uniform distributions between the bounds. For the
    case of cell ratios samples are taken from the logspace.

    """
    # Random area_ratio and C_ratio.
    area_range = args.get("area_range")
    C_range = args.get("C_range")
    b_range = args.get("b_range")
    area_ratio = random.uniform(low=area_range[0], high=area_range[1])
    C_0_mantissa, C_0_exp = frexp_10(C_range)
    exponent = random.uniform(low=C_0_exp[0], high=C_0_exp[1])
    C_ratio = C_0_matissa[0]*10.0**exponent
    # Random uniform. We could use N(50, 50) (clipped above zero) and
    # could also randomize the mean and variance.
    b_guess = random.uniform(low=b_range[0], high=b_range[1])

    guess_kwargs = args.get("guess_kwargs")    # Obviously do not unpack.
    guess_kwargs["area_ratio"] = area_ratio
    guess_kwargs["C_ratio"] = C_ratio
    guess_kwargs["imag_neigh_params"][-2:] = [b_guess*1.5, b_guess]

    guess, guesser = fit_imag_neigh(**guess_kwargs)
    return guess


# We have bounds from Guesser.get_bounds(guess, C_doubt=1e3,
# N_doubt=2.0, kn_max=10.0) which are non_changing so we should supply
# these somewhere. Probably don't need this function but can set
# somewhere else. This is used in the example where each candidate is
# a list of tuples. Each of our candidates is a list of parameter
# values so we are not as "non-standard".
def bound_params(candidate, args):
    return [max(min(b[1], c), b[0]) for b, c in zip(bounds, canditate)]
# "The lower_bound and upper_bound attributes are added to the
# function so that the mutate_polygon function can make use of them
# without being hard-coded."
# bound_params.lower_bound = (l for l, h in bounds)
# bound_params.upper_bound = (h for l, h in bounds)

# Can we use the decorator @inspyred.ec.evaluator for this and maybe
# parallize? Alternatively, we could use each candidate as an initial
# guess for gradient fitting or generate each candidate from gradient
# fits.
def evaluate_fit(candidates, args):
    # Evaluate the objective function for each set of canditate
    # parameters and return this as the fitness. Here fitter and plate
    # are defined outside the scope of the function.
    fitter = args.get("cans_fitter")
    print(fitter)
    plate = args.get("plate")
    print(plate)
    return [fitter._rr_obj(plate, cs) for cs in candidates]

# Best to observe fitting by the plot of the best fit. Can either plot
# (time consuming) or just print the value of the objective
# function. If it takes a long time between iterations it is a good
# idea to save the plots.
def fit_observer(population, num_generations, num_evaluations, args):
    """Plot the best fit for the current iteration.

    Also print the value of the objective function. May be helpful to
    write or append the parameter values to file.

    Requires plate and plotter in args. Also plotfile if we wish to
    save.

    """
    best = max(population)
    plotter = args["plotter"]
    title = "Best fit after {0} generations and {1} evaluations."
    title = title.format(num_generations, num_evaluations)
    plotter.plot_est_rr(args["plate"], best.candidate, title=title,)
                        # filename=args["plotfile"])
    message = "Best fittness of {0} after {1} generations and {2} evaluations."
    print(message.format(best.fitness, num_generations, num_evaluations))


# Unpack saved sim and fit data.
with open("temp_sim_and_est_data.json", 'r') as f:
    data = dict_to_numpy(json.load(f))

exp_data = {"c_meas": data["c_meas"], "times": data["times"], "empties": []}
plate = Plate(data["rows"], data["cols"], exp_data)
plate.sim_params = data["sim_params"]
plate.sim_amounts = data["sim_amounts"]
plate.grad_est_x = data["grad_est"]
plate.set_rr_model(CompModelBC(), plate.sim_params)
bounds = data["bounds"]
bounds[4:] = np.array([0, 500])    # Need an upper bound for genetic algorithm
guess = data["guess"]
model = CompModelBC()

# At the moment we have b bounds as (0, None). We need an upper bound.

# Our problem is real-coded. Choose evolution strategy (ES). "The
# default for an ES is to select the entire population, use each to
# produce a child via Gaussian mutation, and then use "plus"
# replacement." - http://pythonhosted.org/inspyred/tutorial.html#id1.
seed = int(time.time())
rand = random.Random(seed)
with open("seeds.txt", 'a') as f:
    f.write("{0}\n".format(seed))
es = inspyred.ec.ES(rand)
es.observer = inspyred.ec.observers.stats_observer
es.terminator = [inspyred.ec.terminators.evaluation_termination,
                 inspyred.ec.terminators.diversity_termination]

cans_kwargs = {
    "bounds": bounds,
    "plate": plate,
    "cans_fitter": Fitter(CompModelBC()),
#    "cans_model": CompModelBC(),
}
evolve_kwargs = {
    "generator": gen_random_uniform,
    "evaluator": inspyred.ec.evaluators.parallel_evaluation_mp,
    "mp_evaluator": evaluate_fit,
    "mp_num_cpus": 4,
    "pop_size": 10,
    "maximize": False,
    "bounder": inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
    "max_evaluations": 1000,
    "mutation_rate": 0.25,
    # Need to pack args for other functions inside a dictionary called args.
}
# evolve_kwargs.update(cans_kwargs)
final_pop = es.evolve(generator=gen_random_uniform,
                      evaluator=evaluate_fit,
                      # evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                      # mp_evaluator=evaluate_fit,
                      # mp_num_cpus=4,
                      pop_size=10,
                      maximize=False,
                      bounder=inspyred.ec.Bounder(bounds[:, 0], bounds[:, 1]),
                      max_evaluations=1000,
                      mutation_rate=0.25,
                      bounds=bounds,
                      plate=plate,
                      cans_fitter=Fitter(CompModelBC()))
#final_pop = es.evolve(**evolve_kwargs)
# final_pop.sort(reverse=True)
best = max(final_pop)
best_params = best.candidate
print(best_params)
print(len(best_params))
print(plate.no_cultures)
plotter = Plotter(model)
plotter.plot_est_rr(plate, list(best_params))
