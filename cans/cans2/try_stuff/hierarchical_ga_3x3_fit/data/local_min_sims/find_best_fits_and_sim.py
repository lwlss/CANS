import numpy as np
import json


from cans2.process import find_best_fits
from cans2.cans_funcs import dict_to_numpy, cans_to_json
from cans2.model import CompModelBC
from cans2.plate import Plate
# from cans2.plotter import Plotter


def read_data(path):
    with open(path, "r") as f:
        data = dict_to_numpy(json.load(f))
    return data


def sim_and_save(data, model, outfile):
    """Sim a plate from a data dictoinary and save to file."""
    # keepers = ["rows", "cols", "times", "empties"]
    # new_data = {k: v for k, v in data.iteritems if k in keepers}
    plate = Plate(data["rows"], data["cols"])
    plate.times = data["times"]
    plate.sim_params = data["comp_est"]
    plate.set_sim_data(model, noise=True)
    out_data = cans_to_json(plate, model, sim=True)
    with open(outfile, "w") as f:
        json.dump(out_data, f, indent=4, sort_keys=True)


data_path = "../../../../results/p15_fits/full_plate/CompModelBC/*.json"
best_fits = np.array(find_best_fits(data_path, num=5, key="obj_fun"))

# List of data dictionaries for each filepath.
all_data = np.vectorize(read_data)(best_fits[:, 0])
model = CompModelBC()
outfile = "sim_{0}.json"
for i, data in enumerate(all_data):
    sim_and_save(data, model, outfile.format(i))
