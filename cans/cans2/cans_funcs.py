import numpy as np
import copy
import random
import json
import os
import sys
import contextlib
import pickle


from math import log10, floor


def cans_to_json(plate, model, sim=False):
    """Return standardised data for Plate and Model instances.

    Returns a dictionary suitable for saving as json.

    """
    data = {
        "rows": plate.rows,
        "cols": plate.cols,
        "times": plate.times,
        "c_meas": plate.c_meas,
        "empties": plate.empties,
        "model": model.name,
        "species": model.species,
        "params": model.params,
        }
    if sim:
        sim_data = {
            "sim_params": plate.sim_params,
            "sim_amounts": plate.sim_amounts,
            }
        data.update(sim_data)
    return dict_to_json(data)


def est_to_json(plate, model, est_params, obj_fun, time, bounds,
                param_guess, sim=False):
    """Return standardised data for a fit.

    Returns a dictionary suitable for saving as json.

    sim : Also save simulation data plate.sim_params and
    plate.sim_amounts.

    """
    data = cans_to_json(plate, model, sim)
    est_data = {
        "est_params": est_params,
        "obj_fun": obj_fun,
        "fit_time": time,
        "bounds": bounds,
        "param_guess": param_guess,
        }
    data.update(dict_to_json(est_data))
    return data


def round_sig(x, sig=2):
    if x != 0:
        """http://stackoverflow.com/a/3413529"""
        return round(x, sig-int(floor(log10(x)))-1)
    else:
        return x


def get_mask(neighbourhood):
    """Return an boolean array of neighbour indices.

    Each row is a culture; each column is an index.
    1 if neighbour 0 if not.
    """
    # Make an nxn array
    mask = np.zeros([len(neighbourhood)]*2)
    # Find coords in mask from neighbour indices.
    places = []
    [[places.append((i, val)) for val in tup]
     for i, tup in enumerate(neighbourhood)]
    # 1 if culture of row has neighbour w/ index of column.
    for place in places:
        mask[place] = 1
    return mask


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
    vals = np.random.normal(loc=mean, scale=np.sqrt(var), size=n)
    if negs:
        return vals
    else:
        return vals.clip(min=0.0)


def dict_to_json(dct):
    """Convert np.ndarrays in a dict to lists.

    Json requires np.ndarray to be dumped as a list.
    """
    for k, v in dct.items():
        if isinstance(v, np.ndarray):
            dct[k] = v.tolist()
    return dct


def dict_to_numpy(dct):
    """Convert lists of numbers to np.ndarrays of dtype np.float64.

    Return the dictionary with other items untouched.

    """
    for k, v in dct.items():
        if isinstance(v, list):
            try:
                dct[k] = np.array(v, dtype=np.float64)
            except ValueError:
                # e.g. For lists of strings.
                continue
    return dct


def add_noise(data, var=0.02):
    """Return data with added random noise as np.ndarray.

    Also clip negative values to zero.
    """
    noise = np.random.normal(0.0, np.sqrt(var), len(data))
    noisey = np.asarray(data, dtype=np.float64) + noise
    return noisey.clip(min=0.0)


def frexp_10(x):
    """Return the mantissa and decimal exponent in base 10.

    Operates on an array and returns a tuple of mantissa and exponent
    arrays.

    http://www.gossamer-threads.com/lists/python/python/867169#867169

    """
    exp = np.floor(np.log10(x))
    return x/10.0**exp, exp


def pickleable(dct, k=[]):
    """Recursively try to pickle values in a nested dict.

    Raise TypeError for the first unpickleable value found and print
    the key. Has no effect if dct is pickleable.

    k : A dictionary key. An empty list, invalid as a dictionary key,
    is used as a default argument so that we can still print a useful
    error message when the supplied object is not a dictionary.

    """
    try:
        for key, val in dct.items():
            pickleable(val, key)
    except AttributeError:
        try:
            pickle.dumps(dct)
        except TypeError:
            if isinstance(k, list):
                raise TypeError, "{0} object cannot be pickled".format(type(dct))
            else:
                raise TypeError, "Value for '{0}' cannot be pickled".format(k)
