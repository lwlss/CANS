import time
import numpy as np
import json
import matplotlib.pyplot as plt

from cans2.plate import Plate
from cans2.model import CompModel
from cans2.guesser import Guesser
from cans2.zoning import get_plate_zone, resim_zone
from cans2.parser import get_plate_data
from cans2.plotter import Plotter
from cans2.cans_funcs import dict_to_json


code_version = 2
coords = (3, 17)
rows = 3
cols = 3

# path = "/home/dan/projects/CANS/data/p15/Output_Data/"
# plate_data = get_plate_data(path)
# real_plate = Plate(plate_data["rows"], plate_data["cols"],
#                    data=plate_data)

comp_model = CompModel()
comp_plotter = Plotter(CompModel())

# zone = get_plate_zone(real_plate, coords, rows, cols)

full_plate = Plate(16, 24)


with open("timings/comp_model/16x24_mean_30_var_15_rs.json", "r") as f:
    data = json.load(f)
full_plate.times = np.asarray(data["times"])
full_plate.sim_params = np.asarray(data["params"])
full_plate.set_sim_data(comp_model, noise=False)

# data = {
#     "params": full_plate.sim_params,
#     "amounts": full_plate.sim_amounts,
#     "times": full_plate.times,
#     "c_meas": full_plate.c_meas,
#     "r_mean": 30.0,
#     "r_var": 15.0
# }

# data = dict_to_json(data)

# with open("timings/16x24_mean_30_var_15_rs.json", "w") as f:
#     json.dump(data, f, sort_keys=True, indent=4)
# assert False

timings = []

# Time solving for full plate.
t0 = time.time()
comp_model.solve(full_plate, full_plate.sim_params)
t1 = time.time()

timings.append(t1 - t0)
print(t1 - t0)

# comp_plotter.plot_est(full_plate, full_plate.sim_params, sim=True)

resim_zone = resim_zone(full_plate, comp_model, coords, rows, cols, noise=True)

# comp_plotter.plot_est(resim_zone, resim_zone.sim_params, sim=True)

comp_guesser = Guesser(CompModel())
guess = comp_guesser.make_guess(resim_zone)
#guess = comp_guesser.make_guess(resim_zone)
param_guess = comp_guesser.nparray_guess(resim_zone, guess)
r_guess = [20.0 for i in range(resim_zone.no_cultures)]
param_guess = np.append(param_guess, [1.0])    # kn guess
param_guess = np.append(param_guess, r_guess)
bounds = comp_guesser.get_bounds(resim_zone, guess)
bounds[2] = (0.5, 10.0)    # kn bounds


# Time fitting
t0 = time.time()
resim_zone.comp_est = resim_zone.fit_model(CompModel(), param_guess=param_guess,
                                           minimizer_opts={'disp': False},
                                           bounds=bounds)
t1 = time.time()
timings.append(t1-t0)

print(timings)


comp_plotter.plot_est(resim_zone, resim_zone.comp_est.x, sim=True)

outfile = "timings/comp_model/timings.txt"
with open(outfile, "a") as f:
    f.write("\nCode Version {}\n".format(code_version))
    f.write(str(timings))

print(bounds)
print(resim_zone.comp_est.x)


comp_plotter.plot_est(resim_zone, resim_zone.comp_est.x,
                      title="Fit of resimed zone", sim=True,
                      filename="timings/comp_model/plots/resim_fit_v{}.png".format(code_version))
