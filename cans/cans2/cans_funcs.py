import numpy as np
import copy
import random
import json


def mad(a, b):
    """Return mean absolute deviation."""
    return np.mean(np.abs(a - b))


def calc_devs(true_params, r_index, *ests):
    """Return deviations of estimated parameters from true.

    For r return mean absolute deviation. Requires index of first
    r_value. Lists should be of equal length.
    """
    true_plate_lvl = true_params[:r_index]
    true_rs = true_params[r_index:]
    devs = []
    for est in ests:
        assert len(true_params) == len(est)
        dev = np.abs(true_plate_lvl - est[:r_index])
        dev = np.append(dev, mad(true_rs, est[r_index:]))
        devs.append(dev)
    return devs


def gauss_list(n, mean=1.0, var=1.0, negs=False):
    """Return a list of n random gaussian distributed numbers.

    If negs is False (default), negative values are round to zero.
    """
    vals = [random.gauss(mean, var) for i in range(n)]
    if negs:
        return vals
    else:
        return [max(0, v) for v in vals]


def dict_to_json(dct):
    """Convert np.ndarrays in a dict to lists.

    Json requires np.ndarray to be dumped as a list.
    """
    for k, v in dct.items():
        if isinstance(v, np.ndarray):
            dct[k] = v.tolist()
    return dct


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
