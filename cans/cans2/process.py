import json
import glob
import os
import Bio.Cluster
import numpy as np


from math import log10, floor


from cans2.plate import Plate
from cans2.cans_funcs import dict_to_numpy


def read_in_json(path):
    """Read in json and return a dict with list converted to numpy arrays."""
    with open(path, "r") as f:
        data = dict_to_numpy(json.load(f))
    return data


def round_sig(x, sig=2):
    # http://stackoverflow.com/a/3413529
    return round(x, sig-int(floor(log10(x)))-1)


def calc_r(C_0, N_0, b):
    """Convert CANS parameters to logistic r"""
    return (C_0 + N_0)*b


def calc_K(C_0, N_0):
    """Convert CANS parameters to logistic K"""
    return C_0 + N_0


def calc_b(r, K, C_0):
    """Convert logistic r and K to competition K"""
    return r/K


def calc_N_0(r, K, C_0):
    """Convert logistic K and C_0 (g) competition N_0"""
    return K - C_0


def least_sq(a, b):
    """Calculate and return the objective function."""
    assert len(a) == len(b)
    return np.sum((a - b)**2)


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
        obj_funs.append((filename, np.sum(data[key])))

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
            row.append(np.mean(np.abs(v1 - v2)))
        mads.append(row)
    return np.tril(mads)


def remove_edges(array, rows, cols):
    """Remove values at edge indices from a flat array."""
    empty_plate = Plate(rows, cols)
    return np.array(array)[list(empty_plate.internals)]
    # print(array)
    # # Trim top and bottom row.
    # trimmed = array[1:-1,1:-1]
    # # Trim left and right column.
    # return trimmed.flatten()


def obj_fun(a, b):
    """Calculate and return the objective function."""
    assert len(a) == len(b)
    return np.sqrt(np.sum((a - b)**2))


def get_outer_indices(rows, cols, depth):
    """Get the indices of cultures up to a certain depth.

    rows, cols : dimensions of the array (Plate).

    depth : How many rows/cols depth. (E.g. 1 for just the edges)

    """
    assert 0 < depth < min(rows, cols)/2.0
    indices = np.arange(rows*cols)
    indices.shape = (rows, cols)
    inner = indices[depth:-depth, depth:-depth]
    outer = [n for n in indices.flatten() if n not in inner.flatten()]
    return outer
