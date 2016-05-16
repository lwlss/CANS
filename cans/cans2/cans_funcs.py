import numpy as np
import copy
import random
import json


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


def dict_to_json(dct):
    """Convert np.ndarrays in a dict to lists.

    Json requires np.ndarray to be dumped as a list.
    """
    for k, v in dct.items():
        if isinstance(v, np.ndarray):
            dct[k] = v.tolist()
    return dct


def _get_zone(array, coords, rows, cols):
    """Return a zone of an array."""
    zone = array[coords[0]:coords[0]+rows, coords[1]:coords[1]+cols]
    return zone


def plate_zone(resim=True):
    """Return a plate from a zone of a larger plate.

    If resim == True, resimulate from the underlying
    parameters. Otherwise, return the c_measures from the larger
    plate.

    """
    pass


def get_zone_params(plate_file, coords, rows, cols):
    """Return params for a zone of a plate saved as json.

    Returns plate level parameters and in a flattened list.

    """
    # Read in the full plate.
    with open(plate_file, 'r') as f:
        plate_data = json.load(f)

    plate_rows = plate_data['rows']
    plate_cols = plate_data['cols']
    times = plate_data['times']
    r_index = len(plate_data['model_params']) - 1
    plate_params = plate_data['sim_params']
    plate_rs = plate_params[r_index:]

    assert coords[0] + rows <= plate_rows
    assert coords[1] + cols <= plate_cols
    assert len(plate_rs) == plate_rows*plate_cols

    # Convert the plate r parameters to an array.
    plate_array = np.array(plate_rs)
    plate_array.shape = (plate_rows, plate_cols)
    for row in range(plate_rows):
        assert all(plate_array[row, :] ==
                   plate_rs[row*plate_cols:(row+1)*plate_cols])

    # Now slice the plate array to get the required zone.
    zone = _get_zone(plate_array, coords, rows, cols)
    params = plate_params[:r_index] + zone.flatten().tolist()
    return params


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
