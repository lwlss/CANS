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


def evaluate_params(candidatas, args):
    # Evaluate the objective function for each set of canditate
    # parameters and return this as the fitness. Here fitter and plate
    # are defined outside the scope of the function.
    return [fitter._rr_obj(plate, cs) for cs in candidates]
