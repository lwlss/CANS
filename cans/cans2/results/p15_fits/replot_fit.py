"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate


# Chage the four values below to plot different fits. You can change
# plot options/appearance in the plotter.plot_est function in last
# line. If sim=True, true nutrient amounts are also plotted (these are
# not used in fitting).
argv = 5
b_guess = 35

data_file = "full_plate/argv_{0}_b_guess_{1}.json"
data_file = data_file.format(argv, b_guess)

# Read in data from json file
with open(data_file, 'r') as f:
    fit_data = json.load(f)

plate = Plate(fit_data["rows"], fit_data["cols"])
models = [CompModel(), CompModelBC()]
model_name = fit_data["model"]
model = next((m for m in models if m.name == fit_data["model"]), None)
plotter = Plotter(model)

# Add necessary data attributes to produce plots
plate.times = fit_data['times']
plate.c_meas = fit_data['c_meas']
# plate.sim_params = fit_data['comp_est']
plate.set_rr_model(model, fit_data['comp_est'])

plot_title = 'Competition Model BC fit to p15 (argv {0}; b_guess {1})'
plot_title = plot_title.format(argv, b_guess)
# markersize, markeredgewidth, linewidth
plotter.plot_est_rr(plate, fit_data["comp_est"], title=plot_title,
                    sim=False, legend=False)
