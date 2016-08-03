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
from cans2.process import find_best_fits, remove_edges


barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False, "name": "Empty"},
    {"barcode": "K000347_027_022", "ignore_empty": True, "name": "Filled"},    # Filled stripes do not have correct gene names.
])

# Make raw data plates.
data_path = "../data/stripes/Stripes.txt"

empty_bc = [bc["barcode"] for bc in barcodes if bc["name"] == "Empty"][0]
empty_plate = Plate(**get_plate_data2(data_path, empty_bc))
filled_bc = [bc["barcode"] for bc in barcodes if bc["name"] == "Filled"][0]
filled_plate = Plate(**get_plate_data2(data_path, filled_bc))
data_plates = [empty_plate, filled_plate]

result_paths = [bc["barcode"] + "/results/*.json" for bc in barcodes]

# Pick which of the top 5 estimates to compare.
picks = (0, 0)    # Pick 1st best stripe and 1st best filled.


best_paths = []
for pick, path in zip(picks, result_paths):
    best_paths.append(find_best_fits(path, 5, "obj_fun")[pick])

results = []
for bc, path in zip(barcodes, best_paths):
    with open(path[0], "r") as f:
        results.append(dict_to_numpy(json.load(f)))

best_plates = []
for r in results:
    plate = Plate(**_get_plate_kwargs(r))
    plate.est_params = r["est_params"]
    best_plates.append(plate)

plotter = Plotter(CompModelBC(), font_size=32.0, title_font_size=36.0,
                  lw=3.0, ms=10.0, mew=2.0)
plot_title = "Validation of Comp Model Using Stripes Data"
#plot_title = "Best {0} {1} (obj_fun: {2:})"
# plot_title = plot_title.format(model.name, barcode["name"],
#                                best_fits[0]["obj_fun"])
# plotter.plot_est_rr(best_plate, best_plate.est_params,
#                     plot_title, vis_ticks=False, lw=2.0)

# Plot validation for a zone
coords = (8, 9)
rows, cols = 3, 3

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


# Print the plate level parmeters and average b value for both estimates.
genes = empty_plate.genes
# Boolean array for non-empties
stripes_bool = genes != "EMPTY"

stripes_bool = remove_edges(stripes_bool, empty_plate.rows, empty_plate.cols)
for bc, plate in zip(barcodes, best_plates):
    plate_lvl = plate.est_params[:-plate.no_cultures]
    b_ests = plate.est_params[-plate.no_cultures:]
    b_ests = remove_edges(b_ests, empty_plate.rows, empty_plate.cols)
    b_ests = np.extract(stripes_bool, b_ests)
    b_mean = np.mean(b_ests)
    print(bc["name"])
    print(np.append(plate_lvl, b_mean))


# Could check the objective function for all of the below.
# # Use nutrients of gaps estimate for both.
# for params in plot_params:
#     params[[1, 2]] = plate_lvl[[1,2]]

# # Use nutrients and kn of gaps estimate for both.
# for params in plot_params:
#     params[[1, 2, 3]] = plate_lvl[[1, 2, 3]]

# # Only share kn? Poor.
# for params in plot_params:
#     params[2] = plate_lvl[3]

# # Use stripes plate_lvl estimate for both.
# for params in plot_params:
#     params[:4] = plate_lvl[:4]

plot_title = "Attempted validation of the Competition Model across two plates"
plotter.plot_zone_est(data_plates, ["Stripes", "Filled"], plot_params,
                      models, coords, rows, cols, legend=False,
                      title=plot_title, plot_types=["Est.", "Sim."])
