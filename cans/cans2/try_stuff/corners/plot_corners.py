"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.process import find_best_fits, read_in_json
from cans2.genetic_kwargs import _get_plate_kwargs

paths = [
    "../../results/p15_fits/full_plate/CompModel/*.json",
    "../../results/p15_fits/full_plate/CompModelBC/*.json",
]
fit_data = [read_in_json(find_best_fits(p, 1, "obj_fun")[0][0]) for p in paths]
plates = [Plate(**_get_plate_kwargs(data)) for data in fit_data]
models = [CompModel(), CompModelBC()]

for plate, data in zip(plates, fit_data):
    plate.est_params = data["comp_est"]
est_params = [plate.est_params for plate in plates]

corner_coords = [(0, 0), (0, 21), (13, 0), (13, 21)]
rows, cols = 3, 3
plotter = Plotter(CompModelBC(), lw=3.0, ms=10.0, mew=2.0, xpad=15,
                  ypad=30, legend_font_size=26.0)
plot_title = r"Best Competition Fits to Corner of \textit{cdc13-1} P15 at 27C"

assert all(plates[0].c_meas == plates[1].c_meas)

for coords in corner_coords:
    plotter.plot_zone_est(plates, ["(Comp.)", "(Comp. BC)"],
                          est_params, models, coords, rows, cols,
                          legend=True, title=plot_title,
                          plot_types=["Est.", "Est."], vis_ticks=True)
