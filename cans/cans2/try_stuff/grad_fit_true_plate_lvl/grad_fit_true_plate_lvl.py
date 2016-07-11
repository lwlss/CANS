import json
import numpy as np


from cans2.cans_funcs import dict_to_numpy, dict_to_json
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.genetic_kwargs import _get_plate_kwargs


model = CompModelBC()
plotter = Plotter(model)

# 3x3
data_path = "data/16x24_sim_plate_with_fit.json"
results_dir = "results/sim_16x24/"
exp_name = "full_plate_known_plate_lvl_uniform_b"

# # Full plate
# data_path = "data/16x24_sim_plate_with_fit.json"
# results_dir = "results/sim_16x24/"
# exp_name = "full_plate_known_plate_lvl_uniform_b"
results_file = results_dir + exp_name + ".json"
plot_file = results_dir + "plots/" + exp_name + ".pdf"

# load plate data from json.
with open(data_path, 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))

true_plate = Plate(**_get_plate_kwargs(data))
true_plate.sim_amounts = data["sim_amounts"]
true_plate.sim_params = data["sim_params"]
true_plate.set_rr_model(model, data["sim_params"])

# Put strict bounds on the plate level parameters then fit.
true_plate_lvl = true_plate.sim_params[:model.b_index]
plate_lvl_bounds = np.array([[p, p] for p in true_plate_lvl])
b_bounds = np.array([[0.0, 100.0] for i in range(true_plate.no_cultures)])
bounds = np.concatenate((plate_lvl_bounds, b_bounds))
param_guess = np.concatenate((true_plate_lvl,
                              np.repeat(50.0, true_plate.no_cultures)))

print(true_plate.sim_params)
assert False
true_plate.est = plate.fit_model(model, param_geuss, bounds, rr=True,
                                 minimizer_opts={"disp": True})

data["est_params"] = true_plate.est.x
data["obj_fun"] = true_plate.est.fun

with open("", "w") as f:
    json.dump(dict_to_json(data), f, indent=4, sort_keys=True)

plot_title = "Estimate using known plate level parameters and uniform b."

plotter.plot_est_rr(true_plate, true_plate.est.x, plot_title, sim=True,
                    filename=plot_file)
