import numpy as np
import json


# from cans2.rank import correlate_ests, correlate_avgs, write_stats


# from cans2.parser import get_genes
from cans2.cans_funcs import dict_to_json
from cans2.process import read_in_json, find_best_fits, remove_edges
from cans2.plotter import Plotter
from cans2.plate import Plate
from cans2.model import IndeModel
from cans2.genetic_kwargs import _get_plate_kwargs


log_eq_model = IndeModel()

# genes = get_genes("data/p15/ColonyzerOutput.txt")[:384]
log_path = "results/log_eq_fit_*.json"
comp_bc_path = "../../results/p15_fits/full_plate/CompModelBC/*.json"

best_logs = np.array(find_best_fits(log_path, num=3, key="obj_fun_internals"))
best_comps = np.array(find_best_fits(comp_bc_path, num=1, key="obj_fun"))

# Remove edge cultures from obj_fun total for logistic equivalent model. Open all of the files and resave

print(best_logs[:,])


log_ests = []
for est in best_logs:
    with open(est[0], "r") as f:
        bc_ests.append(json.load(f)["comp_est"][4:])


log_data = read_in_json(best_logs[0][0])
log_plate = Plate(**_get_plate_kwargs(log_data))

print(log_data.keys())

for culture, log_est in zip(log_plate.cultures, log_data["culture_est_params"]):
    culture.log_est = log_est

plotter = Plotter(log_eq_model)
for fit in best_logs[:3]
plotter.plot_culture_fits(log_plate, log_eq_model,
                          title="Best Logistic Equivalent Fit",
                          est_name="log_est")
