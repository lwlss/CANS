import json
import glob
import os
import Bio.Cluster
import numpy as np


from math import log10, floor


# http://stackoverflow.com/a/3413529
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)


def find_best_fits(path, num=None, key="obj_fun"):
    """Return the best num fits by ranking key.

    path : filename will be searched for in glob.glob(path). Use
    "*.json" to return all json files in the current directory.

    num : Index to slice to. The default None returns the whole list.

    Returns a list of (filename, key) tuples.

    """
    obj_funs = []
    for filename in glob.glob(path):
        with open(filename, 'r') as f:
            data = json.load(f)
        obj_funs.append((filename, data[key]))

    obj_funs = sorted(obj_funs, key=lambda tup: tup[0])
    obj_funs = sorted(obj_funs, key=lambda tup: tup[1])

    return obj_funs[:num]


def test_bounds(ests, bounds, depth=None):
    """Test if any estimates are at a boundary.

    depth : compare for the first depth elements. Default (None) tests
    for all.

    Returns a list of True or False for each comparison.

    """
    bools = []
    for est, bs in zip(ests[:depth], bounds[:depth]):
        bools.append(est in bs)
    return bools


def spearmans_rho(mat):
    """Calculate Spearman's rho elementwise for a matrix.

    Uses r_sb which includes a tie correction.

    Returns the distance d_s = 1 - r_sb.

    """
    spearmans = Bio.Cluster.distancematrix(mat, dist="s")
    distances = [1 - row for row in spearmans]
    return distances


def mad_tril(vec):
    """MADs for all combinations of vectors in an array.

    Returns lower triangle.
    """
    mads = []
    for v1 in vec:
        row = []
        for v2 in vec:
            row.append(np.mean(np.abs(v1 - v2)))    # MAD
        mads.append(row)
    return np.tril(mads)
