import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs


from cans2.parser import get_genes
from cans2.process import find_best_fits


genes = get_genes("data/p15/ColonyzerOutput.txt")[:384]

best_no_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel/*.json",
                                     num=0, key="obj_fun"))
best_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC/*.json",
                                  num=1, key="obj_fun"))

log_path = "data/Logistic/argv_10_b_guess_40.json"
with open(log_path, "r") as f:
    log_guess = json.load(f)["init_guess"][4:]

log_ests = [log_guess]

bc_ests = []
for est in best_bc:
    with open(est[0], "r") as f:
        bc_ests.append(json.load(f)["comp_est"][4:])

no_bc_ests = []
for est in best_no_bc:
    with open(est[0], "r") as f:
        no_bc_ests.append(json.load(f)["comp_est"][3:])


bc_ests = [("CompModelBC_{0}".format(i), est) for i, est in enumerate(bc_ests)]
no_bc_ests = [("CompModel_{0}".format(i), est) for i, est in enumerate(no_bc_ests)]
log_ests = [("Logistic_{0}".format(i), est) for i, est in enumerate(log_ests)]
ests = bc_ests + no_bc_ests + log_ests

correlate_avgs(genes, *ests)
