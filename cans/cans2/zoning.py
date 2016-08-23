import numpy as np
import json


from cans2.plate import Plate
from cans2.cans_funcs import dict_to_json
from cans2.process import calc_b, calc_N_0, least_sq
from cans2.model import IndeModel


def _get_zone(array, coords, rows, cols):
    """Return a zone of a 2d array."""
    zone = array[coords[0]:coords[0]+rows, coords[1]:coords[1]+cols]
    return zone


def resim_zone(plate, model, coords, rows, cols, noise=True):
    """Resimulate a zone from the underlying parameters."""
    zone = Plate(rows, cols)
    zone.times = plate.times
    b_index = len(plate.sim_params) - plate.no_cultures
    plate_lvl = plate.sim_params[:b_index]
    bs = plate.sim_params[b_index:]
    zone_bs = get_zone_bs(bs, plate.rows, plate.cols, coords, rows, cols)
    zone_params = np.append(plate_lvl, zone_bs)
    zone.sim_params = zone_params
    zone.set_sim_data(model, noise=noise)
    return zone


def _get_zone_indices(plate, coords, rows, cols):
    """Return the indices of the zone on the plate.

    Probably an easier way of doing things.

    coords : (r, c) of top left culture in plate (from zero)

    row, cols : rows and columns of zone

    """
    plate_indices = np.arange(plate.no_cultures)
    plate_indices.shape = (plate.rows, plate.cols)
    zone_indices = plate_indices[coords[0]:coords[0]+rows,
                                 coords[1]:coords[1]+cols]
    return zone_indices.flatten()


def get_zone_amounts(amounts, plate, model, coords, rows, cols):
    """Return amounts of a zone from a full plate array.

    amounts : array (times, species)
    i.e.
        C_0(t0), C_1(t0), ..., N_0(t0), N_1(t0), ...
        C_0(t1), C_1(t1), ..., N_0(t1), N_1(t1), ...
    where C_0(t0) is cells at culture 0 at time t0.
    """
    zone_indices = _get_zone_indices(plate, coords, rows, cols)
    amount_indices = []
    for s in range(model.no_species):
        amount_indices.append(zone_indices + s*plate.no_cultures)
    amount_indices = np.array(amount_indices).flatten()
    zone_amounts = amounts[:, amount_indices]
    return zone_amounts


def sim_and_get_zone_amounts(plate, model, params, coords, rows, cols):
    """Get simulated amounts for a zone from full plate simulation.

    Simulates for the full plate using roadrunner and the supplied
    params and then returns just the amounts for the zone.

    """
    sim_amounts = model.rr_solve(plate, params)
    zone_amounts = get_zone_amounts(sim_amounts, plate, model,
                                    coords, rows, cols)
    return zone_amounts


# Would be good to slice and keep the same Cultures for plotting QFA R
# logistic fits or Initial guesses.
def get_plate_zone(plate, coords, rows, cols):
    """Return a plate from a zone of a larger plate.

    Coords are a tuple for the top left culture of a rectangular
    zone. rows and cols are the size of the new zone.

    """
    no_cultures = plate.no_cultures
    c_collected = [plate.c_meas[i::no_cultures] for i in range(no_cultures)]
    c_collected = np.array(c_collected)
    c_collected.shape = (plate.rows, plate.cols, len(plate.times))
    zone = _get_zone(c_collected, coords, rows, cols)
    c_meas = [zone[:, :, i] for i in range(len(plate.times))]
    c_meas = np.array(c_meas).flatten()
    assert len(c_meas) == rows*cols*len(plate.times)
    zone_indices = list(_get_zone_indices(plate, coords, rows, cols))
    zone_data = {
        "c_meas": c_meas,
        "times": plate.times,
        "empties": np.array([z_i for z_i, p_i in enumerate(zone_indices)
                             if p_i in plate.empties]),
        # "genes": np.array(plate.genes)[zone_indices],
        }
    zone_plate = Plate(rows, cols, data=zone_data)
    return zone_plate


def get_qfa_R_zone(plate, params, coords, rows, cols,
                   smooth_times=None):
    """Return a zone with from QFA R logistic parameters.

    Reuturned Cultures contain the attributes log_eq_params,
    est_amounts, c_est, c_smooth, and least_sq.

    The QFA R model has parameters for culture level C_0. I pass
    these values to each culture on a Plate and simulate
    individually using IndeModel (i.e. can't use a plate level
    C_0.)

    plate : A Plate object containing Cultures, each with cell
    observations and times.

    params : A dictionary of logistic model parameters, keys
    "C_0", "K", and "r" to convert to C_0, N_0, and b and store as
    attributes of each culture.

    coords : Top left coordinate of the zone (starting (0, 0))

    rows, cols : rows and columns for the zone

    smooth_times : Timepoints to use for a smooth simulation
    """
    log_C_0 = params["C_0"]
    log_N_0 = calc_N_0(**params)
    log_b = calc_b(**params)

    for C_0, N_0, b, culture in zip(log_C_0, log_N_0, log_b, plate.cultures):
        culture.log_eq_params = [C_0, N_0, b]

    log_model = IndeModel()
    for culture in plate.cultures:
        culture.est_amounts = log_model.solve(culture, culture.log_eq_params, culture.times)
        culture.c_est = culture.est_amounts[:, 0]
        culture.least_sq = least_sq(culture.c_est, culture.c_meas)

    if smooth_times is not None:
        smooth_times = np.linspace(plate.times[0], plate.times[-1], 100)
        for culture in plate.cultures:
            culture.smooth_amounts = log_model.solve(culture,
                                                     culture.log_eq_params,
                                                     smooth_times)
            culture.c_smooth = culture.smooth_amounts[:, 0]

    # Get indicies of zone and slice those cultures into a zone list.
    culture_inds = _get_zone_indices(plate, coords, rows, cols)
    zone_cultures = [culture for i, culture in enumerate(plate.cultures)
                     if i in culture_inds]

    zone = get_plate_zone(plate, coords, rows, cols)
    zone.cultures = zone_cultures
    return zone


def get_zone_bs(plate_bs, big_rows, big_cols, coords, rows, cols):
    """Return rate constants b for a zone"""
    b_zone = np.array(plate_bs, copy=True)
    b_zone.shape = (big_rows, big_cols)
    b_zone = _get_zone(b_zone, coords, rows, cols)
    b_zone = b_zone.flatten()
    return b_zone


def get_zone_params(plate_file, coords, rows, cols):
    """Return params for a zone of a plate saved as json.

    Returns plate level parameters and b values in a flattened list.

    """
    # Read in the full plate.
    with open(plate_file, 'b') as f:
        plate_data = json.load(f)

    plate_rows = plate_data['rows']
    plate_cols = plate_data['cols']
    times = plate_data['times']
    b_index = len(plate_data['model_params']) - 1
    plate_params = plate_data['sim_params']
    plate_bs = plate_params[b_index:]

    assert coords[0] + rows <= plate_rows
    assert coords[1] + cols <= plate_cols
    assert len(plate_bs) == plate_rows*plate_cols

    # Convert the plate b parameters to an array.
    plate_array = np.array(plate_bs)
    plate_array.shape = (plate_rows, plate_cols)
    for row in range(plate_rows):
        assert all(plate_array[row, :] ==
                   plate_bs[row*plate_cols:(row+1)*plate_cols])

    # Now slice the plate array to get the required zone.
    zone = _get_zone(plate_array, coords, rows, cols)
    params = plate_params[:b_index] + zone.flatten().tolist()
    return params


def sim_zone(plate_file, model, coords, rows, cols):
    """Resimulate and return a zone of a saved plate."""
    params = get_zone_params(plate_file, coords, rows, cols)
    with open(plate_file, 'b') as f:
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
    """Save data for a zone of a simulated plate read from file."""
    with open(plate_file, 'b') as f:
        plate_data = json.load(f)

    assert plate_data['rows']*plate_data['cols'] > zone.no_cultures

    zone_data = {
        'sim_params': zone.sim_params,
        'sim_amounts': zone.sim_amounts,
        'c_meas': zone.c_meas,
        'times': zone.times,
        'b_mean': plate_data['b_mean'],
        'b_var': plate_data['b_var'],
        'rows': zone.rows,
        'cols': zone.cols,
        'model': model.name,
        'model_params': model.params,
        'parent_plate': plate_file,
        'coords_on_parent': coords,
        'resim': True,
        'description': (
            'A zone of a larger plate.'
            'Coords start (0, 0) and refer to a parent plate '
            'from which data is collected. If resim is True '
            'then amounts are resimulated from zone parameters. '
            'If resim is False then amounts are those of the '
            'parent plate.'
        )
    }
    zone_data = dict_to_json(zone_data)

    with open(outfile, 'w') as f:
        json.dump(zone_data, f, sort_keys=True, indent=4)
