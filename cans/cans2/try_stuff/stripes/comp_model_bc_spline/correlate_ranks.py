import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs, write_stats, mdr, mdp, mdrmdp, get_repeat_stats, get_c_of_v, plot_c_of_v
from cans2.cans_funcs import dict_to_numpy
from cans2.parser import get_plate_data2
from cans2.process import find_best_fits, remove_edges
from cans2.plate import Plate


def add_missing_genes(plate):
    """Correct Colonyzer output for filled plate.

    First column is HIS3. Other columns are repeats of the left.
    """
    genes = np.copy(plate.genes)
    genes.shape = (plate.rows, plate.cols)
    print(genes)
    genes[:, 0] = 'HIS3'
    genes[:, 2::2] = genes[:, 1:-1:2]
    return genes.flatten()


barcodes = np.array([
    {
        "barcode": "K000343_027_001",
        "ignore_empty": False,
        "name": "Stripes",
        "model": CompModelBC(),
    },
    {
        "barcode": "K000347_027_022",    # Filled stripes do not have correct gene names.
        "ignore_empty": True,
        "name": "Filled",
        "model": CompModelBC(),
    },
])

data_path = "../data/stripes/Stripes.txt"
plates = [Plate(**get_plate_data2(data_path, bc["barcode"])) for bc in barcodes]

# Stripes genes
genes = plates[0].genes

# Boolean array for non-empties
stripes_bool = genes != "EMPTY"
grower_genes = np.extract(stripes_bool, genes)
filled_plate_genes = add_missing_genes(plate[1])

best_paths = []
for p in result_paths:
    best_paths += find_best_fits(p, 1, "obj_fun")

results = []
for bc, path in zip(barcodes, best_paths):
    with open(path[0], "r") as f:
        results.append(dict_to_numpy(json.load(f)))

no_cultures = plates[0].no_cultures

# For cross-plate correlations
best_ests = []
for est in results:
    with open(est[0], "r") as f:
        best_ests.append(json.load(f)["est_params"][-no_cultures:])

# Removes edge cultures, usually HIS3 (internal HIS3 also exist).
genes = remove_edges(genes, plates[0].rows, plates[0].cols)
best_ests = [remove_edges(np.array(est), rows, cols) for est in best_ests]

ests = []
for bc, est in zip(barcodes, bets_ests):
    pack_est = [[bc["name"] +
    ests +=

stripes_ests = [["Stripes".format(i), est] for i, est in enumerate(bc_ests)]
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
