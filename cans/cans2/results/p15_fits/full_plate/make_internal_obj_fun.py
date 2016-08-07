"""Find and save the objective function for just the internal cultures.

Make sure that all of the old data is also saved.

"""
import json
import numpy as np
import glob
import os


from cans2.model import CompModel, CompModelBC
from cans2.cans_funcs import dict_to_json
from cans2.process import read_in_json, obj_fun #, get_outer_indices
from cans2.plate import Plate
from cans2.genetic_kwargs import _get_plate_kwargs


in_dirs = [
    "CompModel/*.json",
    "CompModelBC/*.json",
]

out_dirs = [
    "CompModel_2/",
    "CompModelBC_2/",
]

models = [CompModel(), CompModelBC()]

# Find all paths in a directory.
for in_dir, out_dir, model in zip(in_dirs, out_dirs, models):
    for path in glob.glob(in_dir):

        data = read_in_json(path)
        plate = Plate(**_get_plate_kwargs(data))
        plate.est_params = data["comp_est"]

        c_meas = np.reshape(plate.c_meas, (len(plate.times), plate.no_cultures))
        internal_c_meas = c_meas[:, plate.internals].flatten()

        plate.set_rr_model(model, plate.est_params)
        full_plate_amounts = plate.rr_solve()

        internal_est_c = full_plate_amounts[:, plate.internals].flatten()

        internal_obj_fun = obj_fun(internal_c_meas, internal_est_c)
        internal_least_sq = internal_obj_fun**2

        full_plate_obj_fun = data["obj_fun"]
        full_plate_least_sq = full_plate_obj_fun**2

        edge_least_sq = full_plate_least_sq - internal_least_sq

        data["est_params"] = data["comp_est"]
        data["est_amounts"] = full_plate_amounts
        data["full_plate_least_sq"] = full_plate_least_sq
        data["internal_least_sq"] = internal_least_sq
        data["edge_least_sq"] = edge_least_sq

        data = dict_to_json(data)
        out_path = out_dir + path.split("/")[-1]
        with open(out_path, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

## For each path
# Read in all data.
# simulate the amounts.
# Find the objective function of just the internals
# Save all of the data back to file in a new directories.
