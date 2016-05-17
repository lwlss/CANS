import numpy as np
import json


from cans2.plate import Plate
from cans2.cans_funcs import dict_to_json


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


def get_zone_r_guess(r_guess, coords, rows, cols):
    """Return initial r guesses or a zone"""
    r_zone = np.array(r_guess, copy=True)
    r_zone.shape = (rows, cols)
    r_zone = _get_zone(r_zone, coords, rows, cols)
    r_zone = r_zone.flatten()
    return r_zone



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


def sim_zone(plate_file, model, coords, rows, cols):
    params = get_zone_params(plate_file, coords, rows, cols)
    with open(plate_file, 'r') as f:
        plate_data = json.load(f)
    times = plate_data['times']

    try:
        assert model.name == plate_data['model']
    except AssertionError:
        print("Plate model is not the same as zone model.")

    zone = Plate(rows, cols)
    zone.sim_params = params
    zone.times = times
    zone.set_sim_data(model)
    return zone


def save_zone_as_json(zone, model, coords, plate_file, outfile):
    # Plate data
    with open(plate_file, 'r') as f:
        plate_data = json.load(f)

    assert plate_data['rows']*plate_data['cols'] > zone.no_cultures

    zone_data = {
        'sim_params': zone.sim_params,
        'sim_amounts': zone.sim_amounts,
        'c_meas': zone.c_meas,
        'times': zone.times,
        'r_mean': plate_data['r_mean'],
        'r_var': plate_data['r_var'],
        'rows': zone.rows,
        'cols': zone.cols,
        'model': model.name,
        'model_params': model.params,
        'parent_plate': plate_file,
        'coords_on_parent': coords,
        'resim': True,
        'description': ('Coords start (0, 0) and refer to a parent plate '
                        'from which data is collected. If resim is True '
                        'then amounts are resimulated from zone parameters. '
                        'If resim is False then amounts are those of the '
                        'parent plate.')
    }
    zone_data = dict_to_json(zone_data)

    with open(outfile, 'w') as f:
        json.dump(zone_data, f, sort_keys=True, indent=4)
