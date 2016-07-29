import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs, write_stats, mdr, mdp, mdrmdp, get_repeat_stats, get_c_of_v, plot_c_of_v
from cans2.cans_funcs import dict_to_numpy
from cans2.parser import get_plate_data2
from cans2.process import find_best_fits, remove_edges
from cans2.plate import Plate


barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False},
    {"barcode": "K000347_027_022", "ignore_empty": True},    # Filled stripes do not have correct gene names.
])

data_path = "../data/stripes/Stripes.txt"
plate1 = Plate(**get_plate_data2(data_path, **barcodes[0]))
plate2 = Plate(**get_plate_data2(data_path, **barcodes[1]))

genes = plate1.genes

# Boolean array for non-empties
stripes_bool = plate1.genes != "EMPTY"
grower_genes = np.extract(stripes_bool, plate1.genes)

print(stripes_bool)
print(grower_genes)

assert False

best_no_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel/*.json",
                                     num=0, key="obj_fun"))
best_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC/*.json",
                                  num=1, key="obj_fun"))
log_path = "../logistic_fit_C0_grid/results2/log_eq*.json"
best_logs = np.array(find_best_fits(log_path, num=1, key="obj_funs_internals"))


log_eq_ests = []
log_eq_rs = []
log_eq_Ks = []
log_eq_mdrmdps = []
for est in best_logs:
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

bc_ests = []
for est in best_bc:
    with open(est[0], "r") as f:
        bc_ests.append(json.load(f)["comp_est"][4:])

no_bc_ests = []
for est in best_no_bc:
    with open(est[0], "r") as f:
        no_bc_ests.append(json.load(f)["comp_est"][3:])

# Removees HIS3 edge cultures (other internal HIS3 exist)
genes = remove_edges(genes, rows, cols)
log_eq_ests = [remove_edges(np.array(est), rows, cols) for est in log_eq_ests]
bc_ests = [remove_edges(np.array(est), rows, cols) for est in bc_ests]
no_bc_ests = [remove_edges(np.array(est), rows, cols) for est in no_bc_ests]

bc_ests = [["Compe Model".format(i), est] for i, est in enumerate(bc_ests)]
no_bc_ests = [["CompModel_{0}".format(i), est] for i, est in enumerate(no_bc_ests)]
log_eq_ests = [["Logistic Eq. Model".format(i), est] for i, est in enumerate(log_eq_ests)]
ests = bc_ests + no_bc_ests + log_eq_ests

# # Plot all genes
# gene_set = set(genes)
# for gene in list(gene_set):
#     # correlate_ests(genes, gene,
#     #                "results/variances/tops_and_log/top_ests_and_log_eq_b_{0}_var.png".format(gene),
#     #                *ests)
#     correlate_ests(genes, gene, "", *ests)

# # Plot avgs
correlate_avgs(genes, "best_comp_bc_and_log_eq_cor.pdf", *ests)
assert False
# correlate_avgs(genes, "plots/top_two_comp_and_top_three_log_eq_p15_correlations.png", *ests)

# write_stats(genes, "results/top_two_comp_model_bc_comp_model.csv", *ests)


# Now get the coefficient of variation for best bc_est and log_eq_est
plot_c_of_v(genes, *ests)

# unlabelled_ests = [ests[0][1], ests[1][1]]
# print(get_c_of_v(genes, *unlabelled_ests))
