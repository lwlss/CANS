"""Plot correlation of fitness estimates between models for P15."""
import numpy as np
import json


from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter#, plot_scatter
from cans2.parser import get_plate_data2, get_qfa_R_dct
from cans2.process import find_best_fits, remove_edges
from cans2.cans_funcs import dict_to_numpy
from cans2.rank import correlate_ests, mdr, mdp, mdrmdp


# Read in QFA r for P15

# Read in b for comp model and conver to r

# Remove all edge cultures

barcodes = np.array([
    {
        "barcode": "DLR00012733",
        "name": "P15",
        "model": CompModelBC(),
    },
])

data_path = "data/p15/ColonyzerOutput.txt"
plates = [Plate(**get_plate_data2(data_path)) for bc in barcodes]

rows, cols = plates[0].rows, plates[0].cols

# Stripes genes
genes = plates[0].genes
genes = remove_edges(genes, rows, cols)

# Just use fits of the two N_0 model.
result_paths = ["../../results/p15_fits/full_plate/CompModelBC_2/*.json"]

best_paths = []
for p in result_paths:
    best_paths += find_best_fits(p, 1, "internal_least_sq")

results = []
for bc, path in zip(barcodes, best_paths):
    with open(path[0], "r") as f:
        results.append(dict_to_numpy(json.load(f)))

no_cultures = plates[0].no_cultures

# For cross-plate correlations
b_ests = [data["comp_est"][-rows*cols:] for data in results]

# Removes edge cultures, usually HIS3 (internal HIS3 also exist).
b_ests = [remove_edges(np.array(bs), rows, cols) for bs in b_ests]

# Remove the empties from both b_est lists.
ests = []
for bc, est in zip(barcodes, b_ests):
    est_name = bc["name"] + " " + bc["model"].name
    ests.append([est_name, est])

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


# Get logistic QFA R r values and remove edges
qfa_R_path = "data/p15/P15_QFA_LogisticFitnesses.txt"
qfa_R_dct = get_qfa_R_dct(qfa_R_path)
log_r = [remove_edges(np.array(qfa_R_dct["r"]), rows, cols)]
log_mdr = [remove_edges(np.array(qfa_R_dct["MDR"]), rows, cols)]
qfa_R_genes = remove_edges(np.array(qfa_R_dct["Gene"]), rows, cols)
assert len(log_r[0]) == len(comp_r[0])
# Check that we are slicing QFA R and compeition model estimates to
# get the same gene order.
assert all(genes == qfa_R_genes)

# Find mean and medians for each gene

gene_set = list(set(genes))
print(gene_set)
means = []
medians = []

def get_avgs(vals, genes, gene_set, avg="median"):
    """Get the mean for each gene and return with the order of genes.

    vals: list of values

    genes : a list of genes

    gene_set : genes in order

    avg : "median" or "mean"

    """
    avgs = []
    if avg == "mean":
        for gene in gene_set:
            mean = np.mean([vals[i] for i in np.where(genes == gene)[0]])
            avgs.append(mean)
    elif avg == "median":
        for gene in gene_set:
            median = np.median([vals[i] for i in np.where(genes == gene)[0]])
            avgs.append(median)
    return avgs, gene_set

log_r_means = [get_avgs(rs, genes, gene_set, "mean")[0] for rs in log_r]
log_r_medians = [get_avgs(rs, genes, gene_set, "median")[0] for rs in log_r]
comp_r_means = [get_avgs(rs, genes, gene_set, "mean")[0] for rs in comp_r]
comp_r_medians = [get_avgs(rs, genes, gene_set, "median")[0] for rs in comp_r]


log_mdr_means = [get_avgs(mdrs, genes, gene_set, "mean")[0] for mdrs in log_mdr]
log_mdr_medians = [get_avgs(mdrs, genes, gene_set, "median")[0] for mdrs in log_mdr]
comp_mdr_means = [get_avgs(mdrs, genes, gene_set, "mean")[0] for mdrs in comp_mdr]
comp_mdr_medians = [get_avgs(mdrs, genes, gene_set, "median")[0] for mdrs in comp_mdr]

# Check that we get the expected gene ranks based on previous work.
# print([(r, gene) for (r, gene) in sorted(zip(comp_r_medians[0], gene_set))])

# Check QFA R initial C_0s (they call g)
log_C_0 = qfa_R_dct["g"]
from collections import Counter
print("QFA_R_C_0_counter", Counter(log_C_0))

fig_settings = {
    "figsize" : (14, 10),
    }
plotter = Plotter(CompModelBC(), font_size=24, title_font_size=28,
                  legend_font_size=24, labelsize=18, xpad=0, ypad=0,
                  ms=10, mew=2, lw=3.0, fig_settings=fig_settings)
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
# format_titles = {
#     "xlab": "Stripes {0}",
#     "ylab": "Filled {0}",
#     "title": "A) Correlation of {0} estimates between plates for each model",
#     }
# format_labels = ["Logistic Model", "Competition Model"]
# f_meas = "r"
# titles = {k: v.format(f_meas) for k, v in format_titles.items()}
# print(titles)
# labels = [lab.format(f_meas) for lab in format_labels]
# plotter.plot_scatter([log_r[0], comp_r[0]], [log_r[1], comp_r[1]],
#                      labels, title=titles["title"], xlab=titles["xlab"],
#                      ylab=titles["ylab"], ax_multiples=[2, 2],
#                      legend=True, corrcoef=True,
#                      outfile=plotdir + "new/r_correlations_between_plates_0.png")


### Plot correlations of different models for each plate ###

# Locations r between models (locations and medians)
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of {0} estimates between models for P15",
    }
format_labels = ["Cultures", "Medians"]
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r[0], log_r_medians[0]], [comp_r[0], comp_r_medians[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "r_correlations_log_v_comp_p15_locations_and_median.png")

# Cultures r between models (locations and means)
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of {0} estimates between models for P15",
    }
format_labels = ["Cultures", "Means"]
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r[0], log_r_means[0]], [comp_r[0], comp_r_means[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "r_correlations_log_v_comp_p15_locations_and_mean.png")

# Cultures r between models (locations and means)
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of {0} estimates between models for P15",
    }
format_labels = ["Cultures", "Medians", "Means"]
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r[0], log_r_medians[0], log_r_means[0]], [comp_r[0], comp_r_medians[0], comp_r_means[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "r_correlations_log_v_comp_p15_locations_median_and_mean.png")


# Cultures r between models
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of {0} estimates between models for P15",
    }
format_labels = ["Cultures"]
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r[0]], [comp_r[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "r_correlations_log_v_comp_p15_locations.png")

# Median r between models
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of median {0} estimates between models for P15",
    }
format_labels = ["Medians P15"]
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r_medians[0]], [comp_r_medians[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "r_correlations_log_v_comp_p15_medians.png")
# Mean r between models
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of mean {0} estimates between models for P15",
    }
format_labels = ["Means P15"]
f_meas = "r"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_r_means[0]], [comp_r_means[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "r_correlations_log_v_comp_p15_means.png")


# Cultures MDR between models
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of {0} estimates between models for P15",
    }
format_labels = ["Cultures P15"]
f_meas = "MDR"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_mdr[0]], [comp_mdr[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "mdr_correlations_log_v_comp_p15_locations.png")

# Median MDR between models
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of median {0} estimates between models for P15",
    }
format_labels = ["Medians P15"]
f_meas = "MDR"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_mdr_medians[0]], [comp_mdr_medians[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "mdr_correlations_log_v_comp_p15_medians.png")

# Mean MDR between models
format_titles = {
    "xlab": "Logistic {0}",
    "ylab": "Competition {0}",
    "title": "Correlation of mean {0} estimates between models for P15",
    }
format_labels = ["Means P15"]
f_meas = "MDR"
titles = {k: v.format(f_meas) for k, v in format_titles.items()}
labels = [lab.format(f_meas) for lab in format_labels]
plotter.plot_scatter([log_mdr_means[0]], [comp_mdr_means[0]],
                     labels, title=titles["title"], xlab=titles["xlab"],
                     ylab=titles["ylab"], ax_multiples=[2, 2],
                     legend=True, corrcoef=True,
                     outfile=plotdir + "mdr_correlations_log_v_comp_p15_means.png")



# # plot both MDRs
# f_meas = "MDR"
# titles = {k: v.format(f_meas) for k, v in format_titles.items()}
# labels = [lab.format(f_meas) for lab in format_labels]
# plotter.plot_scatter([log_mdr[0], comp_mdr[0]], [log_mdr[1], comp_mdr[1]],
#                      labels, title=titles["title"], xlab=titles["xlab"],
#                      ylab=titles["ylab"], ax_multiples=[2, 2],
#                      legend=True, corrcoef=True,)
#                      # outfile=plotdir + "log_mdr_correlation.png")
