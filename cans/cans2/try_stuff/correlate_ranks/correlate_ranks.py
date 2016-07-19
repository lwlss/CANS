import numpy as np
import json


from cans2.rank import correlate_ests


from cans2.parser import get_genes
from cans2.process import find_best_fits


best_no_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel/*.json",
                                     num=1, key="obj_fun"))
best_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC/*.json",
                                  num=1, key="obj_fun"))


genes = get_genes("data/p15/ColonyzerOutput.txt")[:384]

bc_ests = []
for est in best_bc:
    with open(est[0], "r") as f:
        bc_ests.append(json.load(f)["comp_est"][4:])

no_bc_ests = []
for est in best_no_bc:
    with open(est[0], "r") as f:
        no_bc_ests.append(json.load(f)["comp_est"][3:])




correlate_ests(genes,
               *([("CompModelBC_{0}".format(i), est) for i, est in enumerate(bc_ests)] +
                 [("CompModel_{0}".format(i), est) for i, est in enumerate(no_bc_ests)]))
