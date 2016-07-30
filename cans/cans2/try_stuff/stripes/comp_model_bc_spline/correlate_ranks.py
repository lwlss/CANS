import numpy as np
import json


from cans2.rank import correlate_ests, correlate_avgs, write_stats, mdr, mdp, mdrmdp, get_repeat_stats, get_c_of_v, plot_c_of_v
from cans2.cans_funcs import dict_to_numpy
from cans2.parser import get_plate_data2
from cans2.process import find_best_fits, remove_edges
from cans2.plate import Plate
from cans2.model import CompModelBC


def add_missing_genes(plate):
    """Correct Colonyzer output for filled plate.

    First column is HIS3. Other columns are repeats of the left.
    """
    genes = np.copy(plate.genes)
    genes.shape = (plate.rows, plate.cols)
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

rows, cols = plates[0].rows, plates[0].cols

# Stripes genes
genes = plates[0].genes

# Boolean array for non-empties
stripes_bool = genes != "EMPTY"
stripes_bool = remove_edges(stripes_bool, rows, cols)
genes = remove_edges(genes, rows, cols)
stripes_genes = np.extract(stripes_bool, genes)
filled_plate_genes = add_missing_genes(plates[1])

result_paths = [bc["barcode"] + "/results/*.json" for bc in barcodes]

best_paths = []
for p in result_paths:
    best_paths += find_best_fits(p, 1, "obj_fun")

results = []
for bc, path in zip(barcodes, best_paths):
    with open(path[0], "r") as f:
        results.append(dict_to_numpy(json.load(f)))

no_cultures = plates[0].no_cultures

# For cross-plate correlations
b_ests = [data["est_params"] for data in results]

# Removes edge cultures, usually HIS3 (internal HIS3 also exist).
b_ests = [remove_edges(np.array(bs), rows, cols) for bs in b_ests]

# Remove the empties from both b_est lists.
ests = []
for bc, est in zip(barcodes, b_ests):
    est_name = bc["name"] + " " + bc["model"].name
    ests.append([est_name, np.extract(stripes_bool, est)])

# See if there are any repeats so we can calculate coefficient of
# variation.
gene_counts = np.unique(stripes_genes, return_counts=True)
rep_genes = gene_counts[0][gene_counts[1] > 1]
rep_counts = gene_counts[1][gene_counts[1] > 1]
print("Genes with repeats", rep_genes, rep_counts)

outfile = "best_stripes_and_filled_correlations.pdf"
correlate_ests(stripes_genes, None, "", *ests)

# # Plot all genes spreads
# gene_set = set(stripes_genes)
# for gene in list(gene_set):
#     # correlate_ests(stripes_genes, gene,
#     #                "results/variances/tops_and_log/top_ests_and_log_eq_b_{0}_var.png".format(gene),
#     #                *ests)
#     correlate_ests(stripes_genes, gene, "", *ests)

# write_stats(genes, "results/top_two_comp_model_bc_comp_model.csv", *ests)

# Now get the coefficient of variation for best bc_est and log_eq_est
# plot_c_of_v(stripes_genes, *ests)
