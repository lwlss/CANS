import json
import numpy as np

from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.plotter import Plotter
from cans2.cans_funcs import dict_to_numpy

with open("temp_sim_and_est_data.json", 'r') as f:
    data = dict_to_numpy(json.load(f))

# Unpack saved sim and fit data.
exp_data = {"c_meas": data["c_meas"], "times": data["times"], "empties": []}
plate = Plate(data["rows"], data["cols"], exp_data)
plate.sim_params = data["sim_params"]
plate.sim_amounts = data["sim_amounts"]
plate.grad_est_x = data["grad_est"]
bounds = data["bounds"]
guess = data["guess"]
model = CompModelBC()

plotter = Plotter(model)
#plotter.plot_est_rr(plate, plate.sim_params, sim=True)

bounds[4:] = np.array([0, 100])


params = [ 1.3833660425295625e-07, 0.20410318660272236,
           0.28574446124381125, 1.0789892259323557,
           21.424207236658038, 23.772218037809004, 24.501446724451554,
           25.009691846826961, 32.389389573837754, 18.125418541648578,
           24.367123495065822, 24.185019867576187, 27.28879068888433]
print(bounds)
print(plate.sim_params)
bounded = [l <= p <= h for l, p, h in zip(bounds[:, 0], plate.sim_params, bounds[:, 1])]
print(bounded)

plate.set_rr_model(model, params)
est = plate.fit_model(model, param_guess=params, bounds=bounds,
                      rr=True, minimizer_opts={"disp": True})
plotter.plot_est_rr(plate, est.x)
