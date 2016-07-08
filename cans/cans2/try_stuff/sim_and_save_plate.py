"""Save a simulated Plate and imaginary neighbour guess.

Can be timesaving when developing/debugging code to recover parameters.

"""
import numpy as np
import json


from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.model import CompModelBC
from cans2.guesser import fit_imag_neigh
from cans2.cans_funcs import dict_to_json


outfile = "saved_sim_plates/16x24_sim_plate_no_fit.json"

# Simulate a small 3x3 plate with noise using CompModelBC or CompModel.
rows = 16
cols = 24
times = np.linspace(0, 5, 11)
model = CompModelBC()
plate = Plate(rows, cols)
plate.times = times

C_ratio = 1e-4
area_ratio = 1.4
N_0 = 0.1
b_guess = 45.0
custom_params = {
    "C_0": N_0*C_ratio,
    "N_0": N_0,
    "NE_0": N_0*area_ratio,
    "kn": 1.0,
}
plate.set_sim_data(model, b_mean=50.0, b_var=30.0,
                   custom_params=custom_params, noise=True)

plotter = Plotter(model)
# plotter.plot_est_rr(plate, plate.sim_params,
#                     title="Sim timecourse", sim=False)

# Starting guess from fits of the imaginary neighbour model.
imag_neigh_params = np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess])

guess, guesser = fit_imag_neigh(plate, model, area_ratio, C_ratio,
                                imag_neigh_params,
                                kn_start=0.0, kn_stop=8.0, kn_num=21)
plotter.plot_est_rr(plate, guess, title="Imaginary Nieghbour Guess", sim=True)
bounds = guesser.get_bounds(guess, C_doubt=1e2, N_doubt=2.0, kn_max=10.0)
print(bounds)

# # Fit using gradient method.
# minimizer_opts = {"disp": True}
# plate.grad_est = plate.fit_model(model, guess, bounds=bounds, rr=True,
#                                  minimizer_opts=minimizer_opts)
# plotter.plot_est_rr(plate, plate.grad_est.x, title="Gradient Fit", sim=True)


# Save data so that we do not have to run the above code every time
# and debugging the genetic algorithm is quicker.
data = {
    "rows": rows,
    "cols": cols,
    "times": times,
    "sim_params": plate.sim_params,
    "c_meas": plate.c_meas,
    "sim_amounts": plate.sim_amounts,
    "guess": guess,
    "bounds": bounds,
#    "grad_est": plate.grad_est.x,
    "empties": plate.empties,
    }
with open(outfile, 'w') as f:
     json.dump(dict_to_json(data), f)
