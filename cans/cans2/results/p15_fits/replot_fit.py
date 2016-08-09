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

result_path = "full_plate/CompModelBC_2/*.json"
best_fit = find_best_fits(result_path, num=1, key="internal_least_sq")
print(best_fit)

# # Check that not CompModel fit is better than CompModelBC
# result_path_2 = "full_plate/CompModel_2/*.json"
# best_fit_2 = find_best_fits(result_path_2, num=1, key="internal_least_sq")
# print(best_fit_2)
# assert best_fit[0][1] < best_fit_2[0][1]

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

# Add necessary data attributes to produce plots
plate.times = fit_data['times']
plate.c_meas = fit_data['c_meas']
# plate.sim_params = fit_data['comp_est']
plate.set_rr_model(model, fit_data['comp_est'])
plate.sim_params = fit_data["comp_est"]

# Do not want to resimulate a zone but zoom.
# from cans2.zoning import resim_zone
# zone = resim_zone(plate, CompModelBC(), coords=(5, 5), rows=3, cols=3)
# zone.set_rr_model(model, zone.sim_params)
# plotter.plot_est_rr(zone, zone.sim_params, vis_ticks=True,
#                     title=plot_title)

# coords = (4, 17)
# rows, cols = 3, 3
# plotter = Plotter(model, lw=3.0, ms=10.0, mew=2.0, xpad=15, ypad=30)
# plot_title = r"Best Competition Model BC Fit to \textit{cdc13-1} P15 at 27C (R5, C18)"
# plotter.plot_zone_est([plate], [""],
#                       [plate.sim_params], [CompModelBC()], coords,
#                       rows, cols, legend=True, title=plot_title,
#                       plot_types=["Est."], vis_ticks=True)


# rows, cols = 12, 20
# coords = (2, 2)
# plot_title = r'Best Competition Model BC Fit to \textit{cdc13-1} P15 at 27C' # (R2, C2) 12x20'
# plotter = Plotter(model, lw=3.0, ms=10.0, mew=2.0, xpad=-5, ypad=-8)
# plotter.plot_zone_est([plate], [""],
#                       [plate.sim_params], [CompModelBC()], coords,
#                       rows, cols, legend=False, title=plot_title,
#                       plot_types=["Est."], vis_ticks=False)



# plotter = Plotter(model, lw=3.0, ms=10.0, mew=2.0, xpad=-5, ypad=-8,
#                   units=["", ""])
# plot_title = 'Best Competition Model BC Fit to P15' # (argv {0}; b_guess {1})'
# plot_title = r'Best Competition Model BC Fit to \textit{cdc13-1} P15 at 27C' # (argv {0}; b_guess {1})'
# #plot_title = plot_title.format(argv, b_guess)
# plotter.plot_est_rr(plate, fit_data["comp_est"], title=plot_title,
#                     sim=False, legend=False, vis_ticks=False)


coords = (4, 17)
rows, cols = 3, 3
# rows, cols = 12, 20
# coords = (2, 2)
plot_title = r'Comp Model BC Simulation from Imaginary Neighbour Guess' # for \textit{cdc13-1} P15 at 27C (R5, C18)'
plotter = Plotter(model, lw=3.0, ms=10.0, mew=2.0, xpad=15, ypad=30)
plotter.plot_zone_est([plate], [""], [fit_data["init_guess"]],
                      [CompModelBC()], coords, rows, cols,
                      legend=True, title=plot_title,
                      plot_types=["Sim."], vis_ticks=True)
