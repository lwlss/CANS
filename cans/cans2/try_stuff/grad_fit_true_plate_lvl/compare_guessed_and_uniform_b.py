import json
import numpy as np
import time


from cans2.cans_funcs import dict_to_numpy, est_to_json
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.genetic_kwargs import _get_plate_kwargs


# If does not work could try increasing the accuracy of the solver.

model = CompModelBC()
plotter = Plotter(model)

# rows, cols = (3, 3)
rows, cols = (16, 24)
exp_name = "full_plate_known_plate_lvl_uniform_b"
run = "_run_2"
exp_name = exp_name + run

data_path = "data/sim_plate_with_fit_{0}x{1}.json".format(rows, cols)
results_dir = "results/sim_{0}x{1}/".format(rows, cols)
outfile = results_dir + exp_name + ".json"
plot_file = results_dir + "plots/" + exp_name + ".pdf"

# load plate data from json.
with open(data_path, 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))

plate = Plate(**_get_plate_kwargs(data))
plate.sim_amounts = data["sim_amounts"]
plate.sim_params = data["sim_params"]
plate.set_rr_model(model, data["sim_params"])

# Put strict bounds on the plate level parameters then fit.
plate_lvl = plate.sim_params[:model.b_index]
plate_lvl_bounds = np.array([[p, p] for p in plate_lvl])
b_bounds = np.array([[0.0, 100.0] for i in range(plate.no_cultures)])
bounds = np.concatenate((plate_lvl_bounds, b_bounds))
param_guess = np.concatenate((plate_lvl,
                              np.repeat(50.0, plate.no_cultures)))

t0 = time.time()
plate.est = plate.fit_model(model, param_guess, bounds,
                            rr=True, minimizer_opts={"disp": True})
t1 = time.time()

est_data = est_to_json(plate, model, plate.est.x, plate.est.fun,
                       t1-t0, bounds, param_guess, sim=True)

with open(outfile, "w") as f:
    json.dump(est_data, f, indent=4, sort_keys=True)

title = "Estimate using known plate level parameters and uniform b."
plotter.plot_est_rr(plate, plate.est.x, title, sim=True,
                    filename=plot_file)
