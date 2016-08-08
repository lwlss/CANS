"""Plot correlation of fitness estimates between plates with Spearmans'."""
import numpy as np
import json


from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter, plot_scatter
from cans2.parser import get_plate_data2
from cans2.process import find_best_fits, remove_edges
from cans2.cans_funcs import dict_to_numpy
from cans2.rank import correlate_ests, mdr, mdp, mdrmdp


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


# Now convert to r and plot again. r = b(N_0 + C_0). We
# have removed edge cultures so there should be no NE_0.
plate_lvl = [data["est_params"][:-no_cultures] for data in results]

def calc_r(C_0, N_0, b):
    return (C_0 + N_0)*b

def calc_K(C_0, N_0):
    return C_0 + N_0

comp_r = [calc_r(bs[1], p_lvl[0], p_lvl[1])
          for bs, p_lvl in zip(ests, plate_lvl)]
comp_K = [calc_K(p_lvl[0], p_lvl[1]) for p_lvl in plate_lvl]

comp_mdr =

comp_mdrmdp = []


# Now also get r values from the QFA R fits

# Plot comp b
plot_scatter(ests[0][1], ests[1][1],
             title="Filled b vs Stripes b Comp Model BC",
             xlab="Stripes b", ylab="Filled b")

# plot comp r
plot_scatter(comp_r[0], comp_r[1],
             title="Correlation of r estiamtes from Comp Model BC fit to Stripes and Filled plates",
             xlab="Stripes r", ylab="Filled r")
