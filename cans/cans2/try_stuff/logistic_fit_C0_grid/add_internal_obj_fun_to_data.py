"""For the log eq model we should remove edge cultures from the
objective fuction. Read in the saved data, add "obj_fun_internals"
and resave.
"""
import numpy as np
import json


from cans2.cans_funcs import dict_to_json
from cans2.process import find_best_fits, remove_edges


log_path = "results/log_eq_fit_*.json"

# Remove the edge cultures from the obj_fun and resave files.
all_fit_paths = np.array(find_best_fits(log_path, num=None, key="obj_fun"))[:, 0]

for path in all_fit_paths:
    with open(path, "r") as f:
        data = json.load(f)
    obj_fun_internals = np.sum(remove_edges(data["culture_obj_funs"],
                                            data["rows"], data["cols"]))
    data["obj_fun_internals"] = obj_fun_internals
    with open(path, "w") as f:
        json.dump(dict_to_json(data), f, sort_keys=True, indent=4)
