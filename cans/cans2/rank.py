"""Plot correlations in b value rank between two estimates (or true if sim)."""
# Coefficient of variation.
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import rankdata
from matplotlib.cm import coolwarm


def _get_repeats(genes):
    """Return a dictionary of gene name and list of indices for each gene.

    Returns
    -------
    :obj:`dict` of str : :obj:`list` of :obj:`int`
        A dictionary with keys gene name and values list of indices of repeats.

    """
    uniques = set(genes)
    return {u: [i for i, g in enumerate(genes) if g == u] for u in uniques}


def get_repeat_stats(genes, *ests):
    """Return a list of mean and standard diviation for each gene.

    Args
    ----
    genes : :obj:`list` of :obj:`str`:
        A list of genes.

    *ests : :obj:`list` of :obj:`float`
        Set of parameter estimates for each gene.

    """
    repeats = _get_repeats(genes)
    ests = np.array(ests)
    return [{gene: [np.mean(est[reps]), np.std(est[reps])]
             for gene, reps in repeats.items()} for est in ests]


def correlate_avgs(genes, *ests):
    """Plot correlations in rank of averaged parameter values.

    Averages are taken for repeats on the same plate.

    genes : A list of gene names.

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    print(ests[0][0])
    gene_stats = get_repeat_stats(genes, *[est[1] for est in ests])
    averages = [np.array(est.values())[:, 0] for est in gene_stats]
    labels = [est[0] for est in ests]
    gene_set = gene_stats[0].keys()
    labelled_avgs = [(lab, avgs) for lab, avgs in zip(labels, averages)]
    correlate_ests(gene_set, *labelled_avgs)


def correlate_ests(genes, *ests):
    """Plot correlations in rank of parameter values.

    genes : A list of gene names.

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    labels = [est[0] for est in ests]
    print(ests)
    print(genes)
    ranked = np.array([rankdata(est[1]) for est in ests])
    ranks = np.array([ranked[:, i] for i in range(len(genes))])
    print(ranks)

    fig = plt.figure(facecolor="white")
    ax = plt.axes(frameon=False)
    ax.get_xaxis().tick_bottom()
    cols = coolwarm(np.linspace(0, 1, len(genes)))

    for gene_ranks, col in zip(ranks, cols):
        plt.plot(gene_ranks, color=col)

    for gene, col, rh_rank, in zip(genes, cols, ranks[:, -1]):
        plt.text(len(labels)-1, rh_rank, gene.lower()+"$\Delta$",
                 color=col, style="italic")

    plt.xticks(range(len(ests)), labels)
    ax.yaxis.set_visible(False)
    plt.ylabel("Rank")

    plt.show()


if __name__ == "__main__":
    import string
    from random import shuffle


    # Make some "genes" with repeats.
    genes = list(string.ascii_lowercase[:5]*2)
    shuffle(genes)
    # Generate random ests with different scales.
    ests = np.array([np.random.uniform(0, i+1, len(genes)) for i in range(3)])

    averages = get_repeat_stats(genes, *ests)
    correlate_ests(averages[0].keys(),
                   *[("est_{0}".format(i), np.array(a.values())[:, 0])
                     for i, a in enumerate(averages)])
