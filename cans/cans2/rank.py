"""Plot correlations in b value rank between two estimates (or true if sim)."""
# Coefficient of variation.
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import rankdata
from matplotlib.cm import coolwarm


def rank_bs(est):
    rank_data(est)


def correlate_ests(genes, *ests):
    """Plot correlations for multiple estimates and label with gene name.

    genes : A list of gene names.

    *ests : Corresponding parameter estimates. Each a tuple of
    estimate label and list of values.

    """
    labels = [est[0] for est in ests]

    ranked = np.array([rankdata(est[1]) for est in ests])
    ranks = np.array([ranked[:, i] for i in range(len(genes))])
    print(ranks)

    fig = plt.figure(facecolor="white")
    ax = plt.axes(frameon=False)
    ax.get_xaxis().tick_bottom()
    cols = coolwarm(np.linspace(0, 1, len(genes)))

    for gene_ranks, col in zip(ranks, cols):
        plt.plot(gene_ranks, color=col)


#
    for gene, col, rh_rank, in zip(genes, cols, ranks[:, -1]):
        plt.text(len(labels)-1, rh_rank, gene.lower()+"$\Delta$",
                 color=col, style="italic")

    plt.xticks(range(len(ests)), labels)
    ax.yaxis.set_visible(False)
    plt.ylabel("Rank")

    plt.show()
