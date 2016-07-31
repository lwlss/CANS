import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs, write_stats, mdr, mdp, mdrmdp, get_repeat_stats, get_c_of_v, plot_c_of_v
from cans2.cans_funcs import dict_to_numpy
from cans2.parser import get_genes, get_mdrmdp, get_genes
from cans2.process import find_best_fits, remove_edges


genes = np.array(get_genes("data/p15/ColonyzerOutput.txt")[:384])

best_comp = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel/*.json",
                                    num=0, key="obj_fun"))
best_comp_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC/*.json",
                                       num=1, key="obj_fun"))
log_path = "../logistic_fit_C0_grid/results2/log_eq*.json"
best_log_eq = np.array(find_best_fits(log_path, num=1, key="obj_funs_internals"))

# Read in MDR*MDP from QFA R output.
qfa_R_data = "data/p15/P15_QFA_GeneralisedLogisticFitnesses.txt"
gen_log_mdr_mdp = get_mdrmdp(qfa_R_data)
gen_log_ests = [gen_log_mdr_mdp]
assert all(genes == get_genes(qfa_R_data))

rows, cols = 16, 24

log_eq_ests = []
log_eq_rs = []
log_eq_Ks = []
log_eq_mdrmdps = []
for est in best_log_eq:
    with open(est[0], "r") as f:
        # Get bs
        data = dict_to_numpy(json.load(f))
        log_eq_ests.append(data["culture_est_params"][:, -1])
        log_eq_rs.append(data["logistic_rs"])
        log_eq_Ks.append(data["logistic_Ks"])
        C_0 = data["plate_lvl_C_0"]
        rows = data["rows"]
        cols = data["cols"]
        print(data.keys())
        print(data["plate_lvl_C_0"])
        log_eq_mdrmdps.append([mdrmdp(r, K, C_0) for r, K in zip(log_eq_rs[-1], log_eq_Ks[-1])])
log_eq_ests = log_eq_mdrmdps
# log_eq_ests = log_eq_rs

comp_bc_ests = []
for est in best_comp_bc:
    with open(est[0], "r") as f:
        comp_bc_ests.append(json.load(f)["comp_est"][4:])

comp_ests = []
for est in best_comp:
    with open(est[0], "r") as f:
        comp_ests.append(json.load(f)["comp_est"][3:])

# Removees HIS3 edge cultures (other internal HIS3 exist)
genes = remove_edges(genes, rows, cols)
comp_ests = [remove_edges(np.array(est), rows, cols) for est in comp_ests]
comp_bc_ests = [remove_edges(np.array(est), rows, cols) for est in comp_bc_ests]
log_eq_ests = [remove_edges(np.array(est), rows, cols) for est in log_eq_ests]
gen_log_ests = [remove_edges(np.array(est), rows, cols) for est in gen_log_ests]

# Currently format does nothing but we may with to compare multiple
# fits of the same model.
comp_ests = [["Compe".format(i), est] for i, est in enumerate(comp_ests)]
comp_bc_ests = [["Comp BC".format(i), est] for i, est in enumerate(comp_bc_ests)]
log_eq_ests = [["Log. Eq.".format(i), est] for i, est in enumerate(log_eq_ests)]
gen_log_ests = [["Gen. Log.", est] for est in gen_log_ests]

ests = comp_ests + comp_bc_ests + gen_log_ests + log_eq_ests

# # Plot all genes
# gene_set = set(genes)
# for gene in list(gene_set):
#     # correlate_ests(genes, gene,
#     #                "results/variances/tops_and_log/top_ests_and_log_eq_b_{0}_var.png".format(gene),
#     #                *ests)
#     correlate_ests(genes, gene, "", *ests)

# # Plot avgs
# correlate_avgs(genes, "best_comp_bc_and_log_eq_cor.pdf", *ests)
correlate_avgs(genes, "", *ests)

#assert False
# Now get the coefficient of variation for best bc_est and log_eq_est
plot_c_of_v(genes, *ests)

# write_stats(genes, "results/top_two_comp_model_bc_comp_model.csv", *ests)
