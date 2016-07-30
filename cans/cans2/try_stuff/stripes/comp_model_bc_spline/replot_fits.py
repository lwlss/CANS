"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json
# import csv


from cans2.cans_funcs import dict_to_numpy
from cans2.parser import get_plate_data2
from cans2.genetic_kwargs import _get_plate_kwargs
from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.process import find_best_fits


barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False, "name": "Empty"},
    {"barcode": "K000347_027_022", "ignore_empty": True, "name": "Filled"},    # Filled stripes do not have correct gene names.
])
barcode = barcodes[1]    # Choose which plate to look at.

# Make raw data plates.
data_path = "../data/stripes/Stripes.txt"

empty_bc = [bc["barcode"] for bc in barcodes if bc["name"] == "Empty"][0]
data_plate = Plate(**get_plate_data2(data_path, empty_bc))

result_paths = [bc["barcode"] + "/results/*.json" for bc in barcodes]

best_paths = []
for p in result_paths:
    best_paths += find_best_fits(p, 1, "obj_fun")

results = []
for bc, path in zip(barcodes, best_paths):
    with open(path[0], "r") as f:
        results.append(dict_to_numpy(json.load(f)))

best_plates = []
for r in results:
    plate = Plate(**_get_plate_kwargs(r))
    plate.est_params = r["est_params"]
    best_plates.append(plate)


plotter = Plotter(CompModelBC())
plot_title = "Validation of Comp Model Using Stripes Data"
#plot_title = "Best {0} {1} (obj_fun: {2:})"
# plot_title = plot_title.format(model.name, barcode["name"],
#                                best_fits[0]["obj_fun"])
# plotter.plot_est_rr(best_plate, best_plate.est_params,
#                     plot_title, vis_ticks=False, lw=2.0)

# Plot validation for a zone
coords = (6, 6)
rows, cols = 6, 6

comp_models = [CompModel(), CompModelBC()]
model_name = results[0]["model"]
models = [m for m in comp_models for r in results if m.name == r["model"]]

empties = data_plate.empties

plot_params = []
for bc, plate in zip(barcodes, best_plates):
    if bc["name"] == "Filled":
        # Set empty bs to zero
        params = np.copy(plate.est_params)
        params[empties - plate.no_cultures] = 0.0
        plot_params.append(params)
    else:
        plot_params.append(plate.est_params)
        plate_lvl = plate.est_params[:-plate.no_cultures]

# # Use nutrients of gaps estimate for both.
# for params in plot_params:
#     params[[1, 2]] = plate_lvl[[1,2]]

# # Use nutrients and kn of gaps estimate for both.
# for params in plot_params:
#     params[[1, 2, 3]] = plate_lvl[[1, 2, 3]]

# # Use gaps plate_lvl estimate for both.
# for params in plot_params:
#     params[:4] = plate_lvl[:4]


plotter.plot_zone_est(data_plate, plot_params, models, coords, rows,
                      cols, legend=True)
assert False





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
plotter.plot_est_rr(zone, zone.sim_params, ms=10.0, mew=1.5, lw=2.5,
                    vis_ticks=True, legend=True)



plot_title = 'Best Competition Model BC Fit to p15' # (argv {0}; b_guess {1})'
plot_title = plot_title.format(argv, b_guess)
plotter.plot_est_rr(plate, fit_data["comp_est"], title=plot_title,
                    sim=False, legend=False, ms=10.0, mew=1.5, lw=2.5,
                    vis_ticks=True)

plot_title = 'Competition Model BC init guess for p15 (argv {0}; b_guess {1})'
plot_title = plot_title.format(argv, b_guess)
plotter.plot_est_rr(plate, fit_data["init_guess"], title=plot_title,
                    sim=False, legend=False, ms=10.0, mew=0.5, lw=2.5)
from cans2.plotter import Plotte
