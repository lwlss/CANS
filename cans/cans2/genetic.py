import numpy as np
import json


from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.guesser import fit_imag_neigh
from cans2.plotter import Plotter
from cans2.cans_funcs import dict_to_json


# Simulate a small 3x3 plate with noise using CompModelBC or CompModel.
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
# bounds = guesser.get_bounds(guess, C_doubt=1e3, N_doubt=2.0, kn_max=10.0)
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
# data = dict_to_json(data)
# with open("temp_sim_and_est_data.json", 'w') as f:
#     json.dump(data, f)

with open("temp_sim_and_est_data.json", 'r') as f:
    data = json.load(f)

# Unpack saved sim and fit data.
exp_data = {"c_meas": data["c_meas"], "times": data["times"], "empties": []}
plate = Plate(data["rows"], data["cols"], exp_data)
plate.sim_params = data["sim_params"]
plate.set_amounts = data["sim_amounts"]
plate.grad_est_x = data["grad_est"]
bounds = data["bounds"]
guess = data["guess"]
model = CompModelBC()


# Construct a genetic algorithm to fit and compare with the current
# gradient method.
from random import Random
from time import time
from inspyred import ec
from inspyred.ec import terminators
from cans2.fitter import Fitter

fitter = Fitter(model)

def generete_params(random, args):
    # Need to generate parameter solutions. We want to mate things.
    pass


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
bound_params.lower_bound = (l for l, h in bounds)
bound_params.upper_bound = (h for l, h in bounds)

# Can we use the decorator @inspyred.ec.evaluator for this and maybe
# parallize? Alternatively, we could use each candidate as an initial
# guess for gradient fitting or generate each candidate from gradient
# fits.
def evaluate_fit(candidatas, args):
    # Evaluate the objective function for each set of canditate
    # parameters and return this as the fitness. Here fitter and plate
    # are defined outside the scope of the function.
    return [fitter._rr_obj(plate, cs) for cs in candidates]

# Best to observe fitting by the plot of the best fit. Can use
# matplotlib.pyplot.show() to show a plot without halting
# execution. Will have to pass an option for this to Plotter. Must
# also make sure that we are closing this each time to aviod having
# huge numbers of plots open.
def fit_observer(population, num_generations, num_evaluations, args):
    pass

# Our problem is real-coded. Choose evolution strategy (ES). "The
# default for an ES is to select the entire population, use each to
# produce a child via Gaussian mutation, and then use “plus”
# replacement." - http://pythonhosted.org/inspyred/tutorial.html#id1.
rand = Random()
rand.seed(int(time()))
es = ec.ES(rand)
es.terminator = terminators.evaluation_termination

evolve_kwargs = {
    "generator": generate_params,
    "evaluator": evaluate_fit,
    "pop_size": 100,
    "maximize": False,
    "bounder": ec.bounder(0, None),    # Definately not right for us.
    "max_evaluations": 20000,
    "mutation_rate": 0.25,
}
final_pop = es.evolve(**evolve_kwargs)
final_pop.sort(reverse=True)
print(final_pop[0])
