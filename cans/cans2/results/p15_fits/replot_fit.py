"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json
import csv


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.process import find_best_fits


# Chage the four values below to plot different fits. You can change
# plot options/appearance in the plotter.plot_est function in last
# line. If sim=True, true nutrient amounts are also plotted (these are
# not used in fitting).
argv = 19
b_guess = 45

data_file = "full_plate/CompModelBC/argv_{0}_b_guess_{1}.json"
data_file = data_file.format(argv, b_guess)

result_path = "full_plate/CompModelBC/*.json"
best_fit = find_best_fits(result_path, num=1, key="obj_fun")

print(best_fit)

# Read in data from json file
with open(best_fit[0][0], 'r') as f:
    fit_data = json.load(f)

# r0 = ["argv_{0}_b_guess_{1}".format(argv, b_guess)]
# r1 = ["est_params"] + fit_data["comp_est"][:10]
# r2 = ["log_eq_guess"] + fit_data["init_guess"][:10]
# rows = [r0, r1, r2]
# outfile = "full_plate/replots/first_10_params.csv"
# with open(outfile, 'ab') as f:
#     writer = csv.writer(f, delimiter="\t")
#     for r in rows:
#         writer.writerow(r)
timing = fit_data["fit_time"]
print(timing)


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


#temp
from cans2.zoning import resim_zone
plate.sim_params = fit_data["comp_est"]
zone = resim_zone(plate, CompModelBC(), coords=(5, 5), rows=3, cols=3)
zone.set_rr_model(model, zone.sim_params)
plotter.plot_est_rr(zone, zone.sim_params, ms=10.0, mew=1.5, lw=2.5, vis_ticks=True)
assert False


plot_title = 'Best Competition Model BC Fit to p15' # (argv {0}; b_guess {1})'
plot_title = plot_title.format(argv, b_guess)
plotter.plot_est_rr(plate, fit_data["comp_est"], title=plot_title,
                    sim=False, legend=False, ms=10.0, mew=1.5, lw=2.5,
                    vis_ticks=False)

plot_title = 'Competition Model BC init guess for p15 (argv {0}; b_guess {1})'
plot_title = plot_title.format(argv, b_guess)
plotter.plot_est_rr(plate, fit_data["init_guess"], title=plot_title,
                    sim=False, legend=False, ms=10.0, mew=0.5, lw=2.5)
