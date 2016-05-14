import numpy as np
import copy
import random


def add_noise(data, sigma=0.02):
    """Return data with added random noise as np.ndarray."""
    if not isinstance(data, np.ndarray):
        noisey = np.asarray(copy.deepcopy(data), dtype=np.float64)
    else:
        noisey = copy.deepcopy(data)
    for x in np.nditer(noisey, op_flags=['readwrite']):
        x[...] = x + random.gauss(0, sigma)
    np.maximum(0, noisey, out=noisey)
    return noisey


def mad(a, b):
    """Return mean absolute deviation."""
    return np.mean(np.abs(a - b))


def gauss_list(n, mean=1.0, var=1.0, negs=False):
    """Return a list of n random gaussian distributed numbers.

    If negs is False (default), negative values are round to zero.
    """
    vals = [random.gauss(mean, var) for i in range(n)]
    if negs:
        return vals
    else:
        return [max(0, v) for v in vals]
