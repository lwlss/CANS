"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.process import find_best_fits


comp_re = "../../results/p15_fits/full_plate/CompModel/*.json"
comp_file = data_file.format(argv, b_guess)

comp_bc_re = "../../results/p15_fits/full_plate/CompModelBC/*.json"
data_file = data_file.format(argv, b_guess)

result_path = "full_plate/CompModelBC/*.json"
best_fit = find_best_fits(result_path, num=1, key="obj_fun")

print(best_fit)

# Read in data from json file
with open(best_fit[0][0], 'r') as f:
    fit_data = json.load(f)


plate = Plate(fit_data["rows"], fit_data["cols"])
models = [CompModel(), CompModelBC()]
model_name = fit_data["model"]
model = next((m for m in models if m.name == fit_data["model"]), None)

# Add necessary data attributes to produce plots
plate.times = fit_data['times']
plate.c_meas = fit_data['c_meas']
# plate.sim_params = fit_data['comp_est']
plate.set_rr_model(model, fit_data['comp_est'])
plate.sim_params = fit_data["comp_est"]


# coords = (0, 0)
# rows, cols = 3, 3
models = [CompModel(), CompModelBC()]
# plotter = Plotter(model, lw=3.0, ms=10.0, mew=2.0, xpad=15, ypad=30)
# plot_title = r"Best Competition Model BC Fit to \textit{cdc13-1} P15 at 27C (R5, C18)"
# plotter.plot_zone_est([plate], [""],
#                       [plate.sim_params], models, coords,
#                       rows, cols, legend=True, title=plot_title,
#                       plot_types=["Est."], vis_ticks=True)
