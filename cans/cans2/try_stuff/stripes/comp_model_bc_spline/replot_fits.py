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
empty_plate = Plate(**get_plate_data2(data_path, empty_bc))
filled_bc = [bc["barcode"] for bc in barcodes if bc["name"] == "Filled"][0]
filled_plate = Plate(**get_plate_data2(data_path, filled_bc))
data_plates = [empty_plate, filled_plate]

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
coords = (3, 3)
rows, cols = 8, 8

comp_models = [CompModel(), CompModelBC()]
model_name = results[0]["model"]
models = [m for m in comp_models for r in results if m.name == r["model"]]

empties = empty_plate.empties

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

# Could check the objective function for all of the below.

# Use nutrients of gaps estimate for both.
for params in plot_params:
    params[[1, 2]] = plate_lvl[[1,2]]

# # Use nutrients and kn of gaps estimate for both.
# for params in plot_params:
#     params[[1, 2, 3]] = plate_lvl[[1, 2, 3]]

# # Only share kn? Poor.
# for params in plot_params:
#     params[2] = plate_lvl[3]

# # Use gaps plate_lvl estimate for both.
# for params in plot_params:
#     params[:4] = plate_lvl[:4]

plotter.plot_zone_est(data_plates, plot_params, models, coords, rows,
                      cols, legend=True)
