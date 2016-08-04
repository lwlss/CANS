"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.process import find_best_fits, read_in_json
from cans2.genetic_kwargs import _get_plate_kwargs
from cans2.zoning import get_plate_zone


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
est_bs = [p.est_params[-p.no_cultures:] for p in plates]

# 1) Obj fun for depth one and two both plates.

# 2) COV between edge HIS3.
def get_ring(array, rows, cols, depth):
    """Get a ring of values from a square array.

    array : A flat array, square-array or list.

    rows, cols : the number of rows and columns in the parent
    square array.

    depth : depth of ring (0 for edges)

    """
    assert depth < min(rows, cols)/2.0
    array = np.array(array)
    array = array.flatten()
    array.shape = (rows, cols)
    if depth > 0:
        array = array[depth:-depth, depth:-depth]
    plate = Plate(*array.shape)
    array = array.flatten()
    array = array[plate.edges]
    return array


def get_c_meas_ring(plate, depth):
    # Just figure out how to slice 3d arrays.
    pass

depth_0_bs = [get_ring(bs, p.rows, p.cols, 0) for bs, p in zip(est_bs, plates)]
depth_1_bs = [get_ring(bs, p.rows, p.cols, 1) for bs, p in zip(est_bs, plates)]

# Now need to get c_meas for all of the edges. And depth 1. Can use zoning.

second_b = [get_ring(est, p.est_params[-]   # In one from the edges
for plate in plates:
    bs = plate.est_params[-plate.no_cultures:]
    bs.shape = (plate.rows, plate.cols)
    bs = bs[1:-1, 1:-1]
    dummy_plate = Plate(*bs.shape)
    bs = bs.flatten()
    bs = bs[dummy_plate.edges]
    second_b.append(edges)

# Do the same for
assert False

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
