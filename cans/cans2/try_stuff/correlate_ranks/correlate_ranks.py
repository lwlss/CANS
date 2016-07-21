import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs, write_stats


from cans2.parser import get_genes
from cans2.process import find_best_fits


genes = get_genes("data/p15/ColonyzerOutput.txt")[:384]

best_no_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel/*.json",
                                     num=1, key="obj_fun"))
best_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC/*.json",
                                  num=1, key="obj_fun"))

log_path = "data/Logistic/argv_10_b_guess_40.json"
with open(log_path, "r") as f:
    log_guess = json.load(f)["init_guess"][4:]


log_ests = [log_guess]
# log_ests = []

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

gene_set = set(genes)
for gene in list(gene_set):
    # correlate_ests(genes, gene,
    #                "results/variances/tops_and_log/top_ests_and_log_eq_b_{0}_var.png".format(gene),
    #                *ests)
    correlate_ests(genes, gene,
                   "".format(gene),
                   *ests)


# correlate_avgs(genes, "top_two_comp_p15_correlations.png", *ests)

# write_stats(genes, "results/top_two_comp_model_bc_comp_model.csv", *ests)
