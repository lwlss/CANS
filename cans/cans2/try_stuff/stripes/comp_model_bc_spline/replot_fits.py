"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json
# import csv


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
barcode = barcodes[0]    # Choose which plate to look at.

fit_path = barcode["barcode"] + "/results/*.json"
data_path = "../data/stripes/Stripes.txt"

# Plate with no fit data.
raw_plate = Plate(**get_plate_data2(data_path, barcode["barcode"]))

best_paths = np.array(find_best_fits(fit_path, num=5, key="obj_fun"))

best_fits = []
for est in best_paths:
    with open(est[0], "r") as f:
        best_fits.append(json.load(f))

best_plate = Plate(**_get_plate_kwargs(best_fits[0]))
best_plate.est_params = best_fits[0]["est_params"]

models = [CompModel(), CompModelBC()]
model_name = best_fits[0]["model"]
model = next((m for m in models if m.name == best_fits[0]["model"]), None)

plotter = Plotter(model)
plot_title = "Best {0} {1} (obj_fun: {2:})"
plot_title = plot_title.format(model.name, barcode["name"],
                               best_fits[0]["obj_fun"])
plotter.plot_est_rr(best_plate, best_plate.est_params,
                    plot_title, vis_ticks=False, lw=2.0)


from can2.parser import get_plate_zone, get_zone_amounts

coords = (5, 5)
rows, cols = 5, 5
zone = get_plate_zone(best_plate, coords, rows, cols)
zone.est_amounts = get_zone_amounts(best_plate, model,
                                    best_plate.est_params,
                                    coords, rows, cols)

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
plotter.plot_est_rr(zone, zone.sim_params, ms=10.0, mew=1.5, lw=2.5, vis_ticks=True)



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
