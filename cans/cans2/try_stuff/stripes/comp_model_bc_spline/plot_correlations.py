"""Plot correlation of fitness estimates between plates with Spearmans'."""
import numpy as np
import json


from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter#, plot_scatter
from cans2.parser import get_plate_data2, get_qfa_R_dct
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
comp_K = [np.repeat(calc_K(p_lvl[0], p_lvl[1]), len(rs))
          for p_lvl, rs in zip(plate_lvl, comp_r)]
comp_C_0 = [np.repeat(p_lvl[0], len(rs)) for rs in comp_r]

comp_mdr = [mdr(r, K, C_0) for r, K, C_0 in zip(comp_r, comp_K, comp_C_0)]

comp_mdrmdp = [mdrmdp(r, K, C_0) for r, K, C_0 in zip(comp_r, comp_K, comp_C_0)]


# Now also get r values from the QFA R fits
qfa_R_path = "../data/stripes/Stripes_FIT.txt"

# Use pandas to extract the r values that I want
log_r = np.array(get_qfa_R_dct(qfa_R_path)["r"])
log_mdr = np.array(get_qfa_R_dct(qfa_R_path)["MDR"])
log_bc = np.array(get_qfa_R_dct(qfa_R_path)["Barcode"])
log_bc = np.split(log_bc, 2)
assert len(log_bc[0]) == len(log_bc[1])
assert all(log_bc[0] != log_bc[1])
# Need to remove edge cultures from QFA R data. They count rows and
# colums from zero.
log_rows = np.array(get_qfa_R_dct(qfa_R_path)["Row"])
log_cols = np.array(get_qfa_R_dct(qfa_R_path)["Column"])
log_r = np.array([r for i, j, r in zip(log_rows, log_cols, log_r)
                  if i not in [1, 16] and j not in [1, 24]])
log_r = np.split(log_r, 2)
log_mdr = np.array([mdr for i, j, mdr in zip(log_rows, log_cols, log_mdr)
                    if i not in [1, 16] and j not in [1, 24]])
log_mdr = np.split(log_mdr, 2)
assert len(log_r[0]) == len(comp_r[0])

# Check that we are slicing QFA R and compeition model estimates to
# get the same gene order.
comp_genes = stripes_genes
qfa_R_genes = np.array(get_qfa_R_dct(qfa_R_path)["Gene"])
qfa_R_genes = np.array([gene for i, j, gene in zip(log_rows, log_cols, qfa_R_genes)
                        if i not in [1, 16] and j not in [1, 24]])
qfa_R_genes = np.split(qfa_R_genes, 2)
assert all(comp_genes == qfa_R_genes[0])
assert all(qfa_R_genes[0] == qfa_R_genes[1])

# Check QFA R initial C_0s which they call g
g = np.array(get_qfa_R_dct(qfa_R_path)["g"])
g = np.split(g, 2)
tally = 0
for g1, g2 in zip(g[0], g[1]):
    tally += int(g1 == g2)
print("Fraction of g the same", tally/float(len(g[0])))


plotter = Plotter(CompModelBC(), font_size=30, title_font_size=30,
                  legend_font_size=26, labelsize=18, xpad=0, ypad=0,
                  ms=10, mew=2, lw=3.0)
plotdir = "plots/"
# # Plot comp b
# plot_scatter(ests[0][1], ests[1][1],
#              title="Correlation of b estimates from competition model fits to Stripes and Filled plates",
#              xlab="Stripes b", ylab="Filled b",
#              outfile=plotdir + "comp_b_correlation.png")

# # plot comp r
# plot_scatter(comp_r[0], comp_r[1],
#              title="Correlation of r estimates from competition model fits to Stripes and Filled plates",
#              xlab="Stripes r", ylab="Filled r",
#              outfile=plotdir + "comp_r_correlation.png")
# # plot comp mdr
# plot_scatter(comp_mdr[0], comp_mdr[1],
#              title="Correlation of mdr estimates from competition model fits to Stripes and Filled plates",
#              xlab="Stripes mdr", ylab="Filled mdr",
#              outfile=plotdir + "comp_mdr_correlation.png")

# # plot comp mdr*mdp
# plot_scatter(comp_mdrmdp[0], comp_mdrmdp[1],
#              title="Correlation of mdr*mdp estimates from competition model fits to Stripes and Filled plates",
#              xlab="Stripes mdr*mdp", ylab="Filled mdr*mdp",
#              outfile=plotdir + "comp_mdrmdp_correlation.png")


### Plot correlations of same model between plates ###
# Make format strings for plots.
format_titles = {
    "xlab": "Stripes {0}",
    "ylab": "Filled {0}",
    "title": "A) Correlation of {0} estimates between plates for each model",
    }
format_labels = ["Logistic Model", "Competition Model"]

# plot both rs
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
print(titles)
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r[0], comp_r[0]], [log_r[1], comp_r[1]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "new/r_correlations_between_plates_0.png")


### Plot correlations of different models for each plate ###
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "B) Correlation of {0} estimates between models for each plate",
    }
format_labels = ["Stripes Plate", "Filled Plate"]
# plot both rs
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
print(titles)
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r[0], log_r[1]], [comp_r[0], comp_r[1]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "new/r_correlations_between_models_0.png")

# # plot both MDRs
# f_meas = "MDR"
# titles = {k: v.format(f_meas) for k, v in format_titles.items()}
# labels = [lab.format(f_meas) for lab in format_labels]
# plotter.plot_scatter([log_mdr[0], comp_mdr[0]], [log_mdr[1], comp_mdr[1]],
#                      labels, title=titles["title"], xlab=titles["xlab"],
#                      ylab=titles["ylab"], ax_multiples=[2, 2],
#                      legend=True, corrcoef=True,)
#                      # outfile=plotdir + "log_mdr_correlation.png")
