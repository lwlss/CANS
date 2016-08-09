"""Script to replot fits in matplotlib window to save manually."""
import numpy as np
import json


from scipy.stats import variation


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.process import find_best_fits, read_in_json, obj_fun, get_outer_indices
from cans2.genetic_kwargs import _get_plate_kwargs


# Take best CompModel and CompModelBC fits.
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

depth_1_inds = get_outer_indices(plates[0].rows, plates[0].cols, 1)
depth_2_inds = get_outer_indices(plates[0].rows, plates[0].cols, 2)

# Coefficient of variation for edge cultures.
depth_1_bs = [bs[depth_1_inds] for bs in est_bs]
b_covs = [variation(bs) for bs in depth_1_bs]

# Find measured cell amounts.
c_meas = [np.reshape(p.c_meas, (len(p.times), p.no_cultures)) for p in plates]
depth_1_c_meas = [cs[:, depth_1_inds].flatten() for cs in c_meas]
depth_2_c_meas = [cs[:, depth_2_inds].flatten() for cs in c_meas]
internal_c_meas = [cs[:, p.internals].flatten() for p, cs in zip(plates, c_meas)]    # i.e inside of depth1

# Simulate for full plate amounts.
for p, m in zip(plates, models):
    p.set_rr_model(m, p.est_params)
full_plate_amounts = [p.rr_solve() for p in plates]

# Find estimated cell amounts.
full_plate_est_c = [a[:, :p.no_cultures].flatten() for p, a in zip(plates, full_plate_amounts)]
depth_1_est_c = [a[:, depth_1_inds].flatten() for a in full_plate_amounts]
depth_2_est_c = [a[:, depth_2_inds].flatten() for a in full_plate_amounts]
internal_est_c = [a[:, p.internals].flatten() for a in full_plate_amounts]

# Find obj fun for internals and edges.
depth_1_obj_funs = [obj_fun(c, est_c) for c, est_c in zip(depth_1_c_meas, depth_1_est_c)]
depth_2_obj_funs = [obj_fun(c, est_c) for c, est_c in zip(depth_2_c_meas, depth_2_est_c)]
ring_2_obj_funs = [d2 - d1 for d2, d1 in zip(depth_2_obj_funs, depth_1_obj_funs)]
internal_obj_funs = [obj_fun(c, est_c) for c, est_c in zip(internal_c_meas, internal_est_c)]

# Check that the sums of squares are equal (obj fun takes square root).
for d1_fun, int_fun, full_fun in zip(depth_1_obj_funs, internal_obj_funs, full_plate_obj_funs):
    assert np.isclose((d1_fun**2 + int_fun**2), full_fun**2)

# Find the obj fun per culture for the edges and internals.
obj_fun_zip = zip(plates, full_plate_obj_funs, depth_1_obj_funs, depth_2_obj_funs)
avg_ints = [(full**2 - d1**2)/len(p.internals) for p, full, d1, d2 in obj_fun_zip]
avg_d1s = [d1**2/len(depth_1_inds) for d1 in depth_1_obj_funs]
avg_d2s = [d2**2/len(depth_2_inds) for d2 in depth_2_obj_funs]
avg_ring2 = [(d2**2 - d1**2)/(len(depth_2_inds) - len(depth_1_inds))
             for d1, d2 in zip(depth_1_obj_funs, depth_2_obj_funs)]

# Averages per cultures as a percentage of total objective function.
avg_int_pc = [(avg/full**2)*100 for avg, full in zip(avg_ints, full_plate_obj_funs)]
avg_d1_pc = [(avg/full**2)*100 for avg, full in zip(avg_d1s, full_plate_obj_funs)]
avg_ring2_pc = [(avg/full**2)*100 for avg, full in zip(avg_ring2, full_plate_obj_funs)]

# Total percentage edge contribution to ojb fun.
total_edge_pc = [avg*len(depth_1_inds) for avg in avg_d1_pc]

print([model.name for model in models])
print("Edge b COVS (HIS3)", b_covs)

print("Full plate obj fun", full_plate_obj_funs)
print("Internal ojb fun", internal_obj_funs)
print("Depth 1 obj funs", depth_1_obj_funs)

print("Avg internal obj fun", avg_ints)
print("Avg edge obj fun", avg_d1s)
print("Avg ring 2 obj fun", avg_ring2)

print("Avg percent error per culture (internal)", avg_int_pc)
print("Avg percent error per culture (edge)", avg_d1_pc)
# print("Avg d2 obj fun", avg_d2s)    # Not interesting.
print("Avg percent error per culture (ring 2)", avg_ring2_pc)

print("Total percent contribution to obj fun (edge)", total_edge_pc)

#assert False

corner_coords = [(0, 0), (0, 21), (13, 0), (13, 21)]
rows, cols = 3, 3
plotter = Plotter(CompModelBC(), lw=3.0, ms=10.0, mew=2.0, xpad=15,
                  ypad=30, legend_font_size=26.0)
plot_title = r"Best Competition Fits to Corner of \textit{cdc13-1} P15 at 27C"

assert all(plates[0].c_meas == plates[1].c_meas)

# for coords in corner_coords:
#     plotter.plot_zone_est(plates, ["(Comp.)", "(Comp. BC)"],
#                           est_params, models, coords, rows, cols,
#                           legend=True, title=plot_title,
#                           plot_types=["Est.", "Est."], vis_ticks=True)

import csv

# Use least square not obj fun with sqrt because sums are easier to
# calculate.
rows = [
    ["", "One N_0", "Two N_0"],
    ["Edge b COVS (HIS3)"] + b_covs,
    ["Full plate obj fun"] + [obj**2 for obj in full_plate_obj_funs],
    ["Internal ojb fun"] + [obj**2 for obj in internal_obj_funs],
    ["Depth 1 obj funs"] +  [obj**2 for obj in depth_1_obj_funs],
    ["Avg internal obj fun"] + avg_ints,
    ["Avg edge obj fun"] + avg_d1s,
    ["Avg ring 2 obj fun"] + avg_ring2,
    ["Avg % error per culture (internal)"] +  avg_int_pc,
    ["Avg % error per culture (edge)"] + avg_d1_pc,
# print("Avg d2 obj fun", avg_d2s)    # Not interesting.
    ["Avg % error per culture (ring 2)"] + avg_ring2_pc,
    ["Total % contribution to obj fun (edge)"] + total_edge_pc,
]

with open("corner_stats.csv", "wb") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(rows)
