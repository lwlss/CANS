"""Plot correlations in b value rank between two estimates (or true if sim)."""
# Coefficient of variation.
import numpy as np
import matplotlib.pyplot as plt
import csv


from scipy.stats import rankdata, variation
from matplotlib.cm import coolwarm, cool, rainbow, brg, hsv


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
    """Return mean, std, and coeffieint of variation for each gene.

    Args
    ----
    genes : :obj:`list` of :obj:`str`:
        A list of genes.

    *ests : :obj:`list` of :obj:`float`
        Set of parameter estimates for each gene.

    Returns
    -------
    list
        A list of dictionaries; one for each estimate. Keys are gene names
        and values are tuples of mean, standard deviation, and coefficient
        of vairation.

    """
    repeats = _get_repeats(genes)
    ests = np.array(ests)
    return [{gene: [np.mean(est[reps]), np.std(est[reps]), variation(est[reps])]
             for gene, reps in repeats.items()} for est in ests]


def correlate_avgs(genes, filename="", *ests):
    """Plot correlations in rank of averaged parameter values.

    Averages are taken for repeats on the same plate.

    genes : A list of gene names.

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    gene_stats = get_repeat_stats(genes, *[est[1] for est in ests])
    gene_set = gene_stats[0].keys()
    averages = [np.array(est.values())[:, 0] for est in gene_stats]
#    c_of_vs = [np.array(est.values())[:, 2] for est in gene_stats]
    labels = [est[0] for est in ests]    # est name (x label).
    labelled_avgs = [(lab, avgs) for lab, avgs in zip(labels, averages)]
    correlate_ests(gene_set, filename, *labelled_avgs)


def correlate_ests(genes, filename="", *ests):
    """Plot correlations in rank of parameter values.

    genes : A list of gene names.

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    labels, ests = zip(*ests)
    ranks = np.array([rankdata(est) for est in ests]).T

    #fig = plt.figure(facecolor="0.6")
    fig = plt.figure(figsize=(len(ests)*2, 20), dpi=100, facecolor='0.6', edgecolor='k')

    ax = plt.axes(frameon=False)
    ax.get_xaxis().tick_bottom()
    cols = coolwarm(np.linspace(0, 1, len(genes)))
    cols = rainbow(np.linspace(0, 1, len(genes)))

    for gene_ranks, col in zip(ranks, cols):
        plt.plot(gene_ranks, color=col)



    # Add gene names to right most estimate.
    for est_no in range(len(ests)):
        for gene, col, rank, in zip(genes, cols, ranks[:, est_no]):
            if gene == "EXO1":
                plt.text(est_no-0.4, rank+0.1,
                         gene.lower()+"$\Delta$", color="black",
                         style="italic", fontsize=20,
                         fontweight="bold")
            else:
                pass
                # plt.text(est_no-0.4, rank+0.1, gene.lower()+"$\Delta$",
                #          color=col, style="italic", fontsize=20)

    # if coef_of_vars:
    #     for est_no, c_of_vs in zip(range(len(ests)), coef_of_vars):
    #         for c_of_v, rank, col in zip(c_of_vs, ranks[:, est_no], cols):
    #             plt.text(est_no, rank, "{0:.3f}".format(c_of_v), color=col)


    # plt.xticks(range(len(ests)), labels, rotation="vertical", fontsize=15)
    plt.xticks(range(len(ests)), labels, rotation="horizontal", fontsize=15)
    ax.yaxis.set_visible(False)
    plt.ylabel("Rank")

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()


def write_stats(genes, filename, *ests):
    """Save gene ranks and stats for each estimate as csv file.

    genes : A list of gene names.

    filename : path for file.

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    est_names = [est[0] for est in ests]
    # List of dicts with genes as keys.
    stats = get_repeat_stats(genes, *[est[1] for est in ests])

    # Use gene rankings of first estimate as order for all.
    first_avgs = [(gene, stat[0]) for gene, stat in stats[0].items()]
    sorted_by_avg = sorted(first_avgs, key=lambda tup: tup[1], reverse=True)
    genes = np.array(sorted_by_avg)[:, 0]    # order to use.

    # Array of rankings for each estimate.
    avg_ranks = np.array([rankdata([est_stats[gene][0] for gene in genes])
                          for est_stats in stats]).T
    # An array (each index a different gene) with subarrays of [mean,
    # std, and coef_var] for each estimate.
    ordered_stats = np.array([[est_stats[gene] for est_stats in stats]
                              for gene in genes])

    # Place the ranks at the front of each set of stats.
    rank_and_stats = np.dstack((avg_ranks, ordered_stats))

    stat_labs = ["rank", "mean", "std", "coef_var"]
    est_labels = [est + " " + lab for est in est_names for lab in stat_labs]
    first_row = ["gene"] + est_labels
    with open(filename, "wb") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(first_row)
        for gene, gene_stats in zip(genes, rank_and_stats):
            row = [gene] + list(gene_stats.flatten())
            writer.writerow(row)


if __name__ == "__main__":
    import string
    from random import shuffle


    # Make some "genes" with repeats.
    genes = list(string.ascii_lowercase[:5]*2)
    shuffle(genes)
    # Generate random ests with different scales.
    ests = np.array([np.random.uniform(0, i+1, len(genes)) for i in range(3)])

    write_stats(genes, "temp.csv", *[("est_{0}".format(i), est) for i, est in enumerate(ests)])

    averages = get_repeat_stats(genes, *ests)
    correlate_ests(averages[0].keys(),
                   *[("est_{0}".format(i), np.array(a.values())[:, 0])
                     for i, a in enumerate(averages)])
