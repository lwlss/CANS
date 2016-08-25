"""Plot correlations in b value rank between two estimates (or true if sim)."""
# Coefficient of variation.
import numpy as np
import matplotlib.pyplot as plt
import csv


from scipy.stats import rankdata, variation
from matplotlib.cm import coolwarm, cool, rainbow, brg, hsv


def mdr(r, K, C_0, v=1.0):
    """Return maximum doubling rate."""
    return (r*v)/np.log(1.0 - (2.0**v-1)/((2.0**v)*(C_0/K)*v - 1.0))


def mdp(K, C_0):
    """Return maximum doubling potential."""
    return np.log(K/C_0)/np.log(2.0)


def mdrmdp(r, K, C_0, v=1.0):
    """Return maximum doubling rate times maximum doubling potential."""
    return mdr(r, K, C_0, v)*mdp(K, C_0)


def _get_repeats(genes):
    """Return a dictionary of gene name and list of indices for each gene.

    Returns
    -------
    :obj:`dict` of str : :obj:`list` of :obj:`int`
        A dictionary with keys gene name and values list of indices of repeats.

    """
    uniques = set(genes)
    return {u: [i for i, g in enumerate(genes) if g == u] for u in uniques}


def get_c_of_v(genes, *ests):
    repeats = _get_repeats(genes)
    ests = np.array(ests)
    c_of_v = [{gene: variation(est[reps]) for gene, reps in repeats.items()}
              for est in ests]
    return c_of_v


def get_repeat_stats(genes, avg, *ests):
    """Return mean, std, and coeffieint of variation for each gene.

    Args
    ----
    genes : :obj:`list` of :obj:`str`:
        A list of genes.

    *ests : :obj:`list` of :obj:`float`
        Set of parameter estimates for each gene.

    avg : ("median" or "mean") How to calculate averages for each
    gene.

    Returns
    -------
    list
        A list of dictionaries; one for each estimate. Keys are gene names
        and values are tuples of mean, standard deviation, and coefficient
        of vairation.

    """
    repeats = _get_repeats(genes)
    ests = np.array(ests)
    if avg == "median":
        return [{gene: [np.median(est[reps]), np.std(est[reps]), variation(est[reps])]
                 for gene, reps in repeats.items()} for est in ests]
    elif avg == "mean":
        return [{gene: [np.mean(est[reps]), np.std(est[reps]), variation(est[reps])]
                 for gene, reps in repeats.items()} for est in ests]


def correlate_avgs(genes, avg, filename="", eps=0.12, *ests):
    """Plot correlations in rank of averaged parameter values.

    Averages are taken for repeats on the same plate.

    genes : A list of gene names.

    avg : "median" or "mean"

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    gene_stats = get_repeat_stats(genes, avg, *[est[1] for est in ests])
    gene_set = gene_stats[0].keys()
    averages = [np.array(est.values())[:, 0] for est in gene_stats]
#    c_of_vs = [np.array(est.values())[:, 2] for est in gene_stats]
    labels = [est[0] for est in ests]    # est name (x label).
    labelled_avgs = [(lab, avgs) for lab, avgs in zip(labels, averages)]
    correlate_ests(gene_set, None, filename, eps, *labelled_avgs)


def correlate_ests(genes, query_gene, filename="", eps=0.15, *ests):
    """Plot correlations in rank of parameter values.

    genes : A list of gene names.

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    eps : Gap in x in start- and end-points of lines to avoid overlap
    with gene names.

    # tightness : How close together are the rows of gene names.

    """
    labels, ests = zip(*ests)
    ranks = np.array([rankdata(est) for est in ests]).T

    #fig = plt.figure(facecolor="0.6")
    fig = plt.figure(figsize=(len(ests)*6, 30), dpi=500,
                     facecolor='0.6', edgecolor='k')

    ax = plt.axes(frameon=False)
    ax.get_xaxis().tick_bottom()
    cols = coolwarm(np.linspace(0, 1, len(genes)))
    cols = rainbow(np.linspace(0, 1, len(genes)))

    for gene_ranks, col in zip(ranks, cols):
        pairs = [gene_ranks[i:i+2] for i in range(len(gene_ranks)-1)]
        positions = [[i, i+1] for i in range(len(gene_ranks)-1)]
        for pair, pos in zip(pairs, positions):
            plt.plot([pos[0]+eps, pos[1]-eps],
                      pair, color=col, lw=2.0)

    for est_no in np.arange(len(ests)):
        for gene, col, rank, in zip(genes, cols, ranks[:, est_no]):
            if gene == query_gene:
                plt.text(est_no-eps, rank,
                         gene.lower()+"$\Delta$", color="black",
                         style="italic", fontsize=20,
                         fontweight="bold")
            else:
                # continue
                if est_no == 0:
                    alignment = "right"
                    x_pos = est_no + eps
                elif est_no == len(ests)-1:
                    alignment = "left"
                    x_pos = est_no - eps
                else:
                    alignment = "center"
                    x_pos = est_no
                if gene == "HIS3":
                    plt.text(x_pos, rank-0.25, gene.lower()+"$\Delta$",
                             color="k", style="italic", fontweight="bold",
                             fontsize=30,
                             horizontalalignment=alignment)
                else:
                    plt.text(x_pos, rank-0.25, gene.lower()+"$\Delta$",
                             color=col, style="italic", fontsize=30,
                             horizontalalignment=alignment)

    # # Add coef of variation label
    # if coef_of_vars:
    #     for est_no, c_of_vs in zip(range(len(ests)), coef_of_vars):
    #         for c_of_v, rank, col in zip(c_of_vs, ranks[:, est_no], cols):
    #             plt.text(est_no, rank, "{0:.3f}".format(c_of_v), color=col)


    # plt.xticks(np.arange(len(ests)), labels, rotation="vertical", fontsize=26)
    plt.xticks(np.arange(len(ests)), labels,
               rotation="horizontal", fontsize=40)
    ax.yaxis.set_visible(False)
    plt.ylabel("Rank")

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()


def plot_c_of_v(genes, avg, title, *ests):
    """Plot coefficient of variation.

    http://matplotlib.org/examples/pylab_examples/barchart_demo.html

    avg : ("median" or "mean") Orders by the rank of average
    estimates for the first argument in ests.

    """
    est_names = [est[0] for est in ests]
    # List of dicts with genes as keys.
    stats = get_repeat_stats(genes, avg, *[est[1] for est in ests])

    # Use gene rankings of first estimate as order for all.
    first_avgs = [(gene, stat[0]) for gene, stat in stats[0].items()]
    sorted_by_avg = sorted(first_avgs, key=lambda tup: tup[1], reverse=True)
    ordered_genes = np.array(sorted_by_avg)[:, 0]    # order to use.

    c_of_vs = get_c_of_v(genes, *[est[1] for est in ests])
    ordered_c_of_vs = [[cvs[gene] for gene in ordered_genes] for cvs in c_of_vs]

    fig, ax = plt.subplots()
    bar_width = 0.8 / float(len(est_names))
    opacity = 0.6
    x_vals = np.arange(len(ordered_genes))

    colors = ["b", "r", "y", "g", "m"]

    plot_zip = zip(est_names, colors, ordered_c_of_vs)
    for i, (name, col, c_of_vs) in enumerate(plot_zip):
        plt.bar(x_vals + i*bar_width, c_of_vs, bar_width,
                alpha=opacity, label=name, color=col)

    italic_genes = [gene.lower()+"$\Delta$" for gene in ordered_genes]

    plt.xlabel('Deletion (ordered by competition b rank)', fontsize=28)
    plt.ylabel('Coefficient of Variation', fontsize=28)
    plt.title(title, fontsize=34)
    plt.xticks(x_vals + bar_width, italic_genes, rotation="vertical",
               style="italic", fontweight="bold", fontsize=22)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
    plt.legend(loc=2, fontsize=28)

    plt.tight_layout()
    plt.show()


def write_stats(genes, filename, avg, *ests):
    """Save gene ranks and stats for each estimate as csv file.

    genes : A list of gene names.

    filename : path for file.

    avg : "median" or "mean" to use for average for repeats of genes

    *ests : Estimated parameter values corresponding to the genes in
    genes. Each a tuple containing a label for the estimate and list
    of estimated values.

    """
    est_names = [est[0] for est in ests]
    # List of dicts with genes as keys.
    stats = get_repeat_stats(genes, avg, *[est[1] for est in ests])

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

    stat_labs = ["rank", avg, "std", "coef_var"]
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
