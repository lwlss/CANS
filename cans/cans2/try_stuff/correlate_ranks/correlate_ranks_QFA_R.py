import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs, write_stats, mdr, mdp, mdrmdp, get_repeat_stats, get_c_of_v, plot_c_of_v
from cans2.cans_funcs import dict_to_numpy
from cans2.parser import get_genes, get_mdrmdp, get_genes, get_qfa_R_dct
from cans2.process import find_best_fits, remove_edges

fitnesses = ["r", "MDR", "MDR*MDP"]
fitness = fitnesses[0]

genes = np.array(get_genes("data/p15/ColonyzerOutput.txt")[:384])

best_comp = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel_2/*.json",
                                    num=0, key="internal_least_sq"))
best_comp_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC_2/*.json",
                                       num=1, key="internal_least_sq"))
log_path = "../logistic_fit_C0_grid/results2/log_eq*.json"
best_log_eq = np.array(find_best_fits(log_path, num=0, key="obj_funs_internals"))

# Read in MDR*MDP from QFA R output.
qfa_R_gen_log_data = "data/p15/P15_QFA_GeneralisedLogisticFitnesses.txt"
gen_log_r = get_qfa_R_dct(qfa_R_gen_log_data)["r"]
gen_log_mdr = get_qfa_R_dct(qfa_R_gen_log_data)["MDR"]
gen_log_mdrmdp = get_qfa_R_dct(qfa_R_gen_log_data)["MDRMDP"]
gen_log_ests = [gen_log_r, gen_log_mdr, gen_log_mdrmdp]
gen_log_ests = [gen_log_ests[fitnesses.index(fitness)]]
# gen_log_ests = [gen_log_r]    # Not comparable with standard logistic r (or comp).
assert all(genes == get_genes(qfa_R_gen_log_data))

qfa_R_log_data = "data/p15/P15_QFA_LogisticFitnesses.txt"
log_r = get_qfa_R_dct(qfa_R_log_data)["r"]
log_mdr = get_qfa_R_dct(qfa_R_log_data)["MDR"]
log_mdrmdp = get_qfa_R_dct(qfa_R_log_data)["MDRMDP"]
log_ests = [log_r, log_mdr, log_mdrmdp]
#log_ests = [log_ests[fitnesses.index(fitness)]]
log_ests = log_ests[:1]
assert all(genes == get_genes(qfa_R_log_data))

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
        log_eq_mdrmdps.append([mdrmdp(r, K, C_0) for r, K in zip(log_eq_rs[-1], log_eq_Ks[-1])])
# log_eq_ests = log_eq_mdrmdps
log_eq_ests = log_eq_rs

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
# print(len(np.where(genes == "HIS3")[0])); assert False
comp_ests = [remove_edges(np.array(est), rows, cols) for est in comp_ests]
comp_bc_ests = [remove_edges(np.array(est), rows, cols) for est in comp_bc_ests]
log_eq_ests = [remove_edges(np.array(est), rows, cols) for est in log_eq_ests]
gen_log_ests = [remove_edges(np.array(est), rows, cols) for est in gen_log_ests]
log_ests = [remove_edges(np.array(est), rows, cols) for est in log_ests]

# Currently format does nothing but we may with to compare multiple
# fits of the same model.
comp_ests = [["Comp.".format(i), est] for i, est in enumerate(comp_ests)]    # Move to using just BC
comp_bc_ests = [["Competition b".format(i), est] for i, est in enumerate(comp_bc_ests)]
log_eq_ests = [["Log. Eq.".format(i), est] for i, est in enumerate(log_eq_ests)]
gen_log_ests = [["Gen. Log. {0}".format(fitness), est] for est in gen_log_ests]
log_ests = [["Logistic {0}".format(f), est] for f, est in zip(["r", "MDR"], log_ests)]

ests = comp_ests + comp_bc_ests + log_ests# + gen_log_ests + log_eq_ests
# ests = comp_ests + comp_bc_ests + log_ests# + log_eq_ests

# # Plot all genes
# gene_set = set(genes)
# for gene in list(gene_set):
#     # correlate_ests(genes, gene,
#     #                "results/variances/tops_and_log/top_ests_and_log_eq_b_{0}_var.png".format(gene),
#     #                *ests)
#     correlate_ests(genes, gene, "", *ests)

# # Plot avgs
# correlate_avgs(genes, "r_rank/comp_b_log_r.png", 0.15, *ests)
# correlate_avgs(genes, "", 0.1, *ests)

# Now get the coefficient of variation for best bc_est and log_eq_est
# c_of_v_title = "Variation in Fitness Estimates by Model"
c_of_v_title = ""
plot_c_of_v(genes, c_of_v_title, *ests)

# write_stats(genes, "results/top_two_comp_model_bc_comp_model.csv", *ests)
