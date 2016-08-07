"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json


from scipy.stats import variation


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

full_plate_obj_funs = []
for plate, data in zip(plates, fit_data):
    plate.est_params = data["comp_est"]
    full_plate_obj_funs.append(data["obj_fun"])
est_params = [plate.est_params for plate in plates]
est_bs = [p.est_params[-p.no_cultures:] for p in plates]


def obj_fun(a, b):
    assert len(a) == len(b)
    return np.sqrt(np.sum((a - b)**2))

def get_outer_indices(rows, cols, depth):
    """Get the indices of cultures at the edge.

    depth : How many rows/cols in. E.g. one for just the very outer
    indices. Two for the 1st and 2nd outers.

    """
    assert 0 < depth < min(rows, cols)/2.0
    indices = np.arange(rows*cols)
    indices.shape = (rows, cols)
    inner = indices[depth:-depth, depth:-depth]
    outer = [n for n in indices.flatten() if n not in inner.flatten()]
    return outer


depth_1_inds = get_outer_indices(plates[0].rows, plates[0].cols, 1)
depth_2_inds = get_outer_indices(plates[0].rows, plates[0].cols, 2)

depth_1_bs = [bs[depth_1_inds] for bs in est_bs]
b_covs = [variation(bs) for bs in depth_1_bs]
print("b_covs", b_covs)

# Now need to find depth 1 and depth 2 c_meas and similar for simulated cells.
c_meas = [np.reshape(p.c_meas, (len(p.times), p.no_cultures)) for p in plates]
depth_1_c_meas = [cs[:, depth_1_inds].flatten() for cs in c_meas]
depth_2_c_meas = [cs[:, depth_2_inds].flatten() for cs in c_meas]
internal_c_meas = [cs[:, p.internals].flatten() for p, cs in zip(plates, c_meas)]    # i.e inside of depth1

# Simulate for full plate amounts.
for p, m in zip(plates, models):
    p.set_rr_model(m, p.est_params)
full_plate_amounts = [p.rr_solve() for p in plates]

# Find total obj_funs
full_plate_est_c = [a[:, :p.no_cultures].flatten() for p, a in zip(plates, full_plate_amounts)]
obj_funs_all = [obj_fun(p.c_meas, est_c) for p, est_c in zip(plates, full_plate_est_c)]
print("all_obj_fun", full_plate_obj_funs, obj_funs_all)

# from cans2.fitter import Fitter
# fitters = [Fitter(m) for m in models]

print(depth_1_inds)
print(len(depth_1_inds))
print([(p.no_cultures, len(p.internals)) for p in plates])

depth_1_est_c = [a[:, depth_1_inds].flatten() for a in full_plate_amounts]
depth_2_est_c = [a[:, depth_2_inds].flatten() for a in full_plate_amounts]
internal_est_c = [a[:, p.internals].flatten() for a in full_plate_amounts]

internal_obj_funs = [obj_fun(c, est_c) for c, est_c in zip(internal_c_meas, internal_est_c)]
print("internal ojb_fun", internal_obj_funs)

# Now find the objective function between depth_1_ests
depth_1_obj_funs = [obj_fun(c, est_c) for c, est_c in zip(depth_1_c_meas, depth_1_est_c)]
depth_2_obj_funs = [obj_fun(c, est_c) for c, est_c in zip(depth_2_c_meas, depth_2_est_c)]
print(depth_1_obj_funs)

# Check that the sums are equal
for d1_fun, int_fun, full_fun in zip(depth_1_obj_funs, internal_obj_funs, obj_funs_all):
    print(np.isclose((d1_fun**2 + int_fun**2), full_fun**2))
    print(d1_fun**2 + int_fun**2)
    print(full_fun**2)

# Find the obj_fun for the edges and internals for each.
for p, full_fun, d1_fun in zip(plates, full_plate_obj_funs, depth_1_obj_funs):
    print("total least squares", full_fun**2)
    avg_internal = (full_fun**2 - d1_fun**2)/len(p.internals)
    print("avg internal least squares", avg_internal)
    avg_edge = d1_fun**2/len(p.edges)
    print("avg edge least squares", avg_edge)
    avg_int_percent = ((full_fun**2 - d1_fun**2) / full_fun**2)/len(p.internals)*100
    avg_edge_percent = (d1_fun**2/full_fun**2)/len(p.edges)*100
    print("average contribution to error of internal", avg_int_percent)
    print("average contribution to error of edge", avg_edge_percent)

# Normalize by the number of cultures and total obj_fun.
norm_funs = []
for p, full_fun, d1_fun in zip(plates, full_plate_obj_funs, depth_1_obj_funs):
    no_outers = float(len(depth_1_inds))
    d1_norm = d1_fun**2/no_outers/full_fun**2
    internal_norm = (full_fun**2 - d1_fun**2)/(p.no_cultures - no_outers)
    norm_funs.append((d1_norm, internal_norm))
print(norm_funs)


# depth_0_bs = [get_ring(bs, p.rows, p.cols, 0) for bs, p in zip(est_bs, plates)]
# depth_1_bs = [get_ring(bs, p.rows, p.cols, 1) for bs, p in zip(est_bs, plates)]

# # Now need to get c_meas for all of the edges. And depth 1. Can use zoning.

# second_b = [get_ring(est, p.est_params[-]   # In one from the edges
# for plate in plates:
#     bs = plate.est_params[-plate.no_cultures:]
#     bs.shape = (plate.rows, plate.cols)
#     bs = bs[1:-1, 1:-1]
#     dummy_plate = Plate(*bs.shape)
#     bs = bs.flatten()
#     bs = bs[dummy_plate.edges]
#     second_b.append(edges)

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
