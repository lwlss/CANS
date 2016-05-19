import numpy as np
import json
import datetime
#import argparse
from sys import argv


from cans2.zoning import get_zone_r_guess
from cans2.plate import Plate
from cans2.model import CompModel
from cans2.plotter import Plotter
from cans2.cans_funcs import calc_devs, dict_to_json


def save_as_json(true_plate, est_plate, est, factr, init_guess,
                 coords, plate_file, guess_file, out_file):

    assert np.array_equal(est_plate.sim_params, est.x)

    # Read true data from file.
    with open(plate_file, 'r') as f:
        true_data = json.load(f)

    # Calculate parameter deviations
    assert np.array_equal(true_data['model_params'], est.model.params)
    param_devs = calc_devs(true_plate.sim_params, est.model.r_index,
                           est_plate.sim_params)[0]

    data = {
        'true_params': true_plate.sim_params,
        'true_amounts': true_plate.sim_amounts,
        'c_meas': true_plate.c_meas,
        'times': true_plate.times,
        'rows': true_plate.rows,
        'cols': true_plate.cols,
        'no_cultures': true_plate.no_cultures,

        # Only for simulations
        'sim_model': true_data['model'],
        'sim_model_species': true_data['model_species'],
        'sim_model_params': true_data['model_params'],

        'fit_model': est.model.name,
        'fit_model_species': est.model.species,
        'fit_model_params': est.model.params,

        'plate_file': plate_file,
        'init_guess_file': guess_file,
        'init_guess': init_guess,
        'est_params': est_plate.sim_params,
        'param_devs': param_devs,
        'est_amounts': est_plate.sim_amounts,
        'est_c_meas': est_plate.c_meas,

        'fit_options': est.fit_options,    # Dict already jsoned.
        'ftol': est.fit_options['ftol'],
        'factr': factr,
        'machine_eps': np.finfo(float).eps,
        'fit_bounds': est.bounds,
        'fit_method': est.method,

        'obj_fun_val': est.fun,
        'fit_success': est.success,
        'reason_for_stop': str(est.message),

        # For the ftol iter and cumulative.
        'tot_fit_time': est.fit_time,
        'fit_time_tot': est.tot_fit_time,
        'nfev': est.nfev,
        'tot_nfev': est.tot_nfev,
        'nit': est.nit,
        'tot_nit': est.tot_nit,

        'date': str(datetime.date.today()),
        'coords': coords,
        'description': (
            'If smaller than a 16x24 plate, init_guesses are either',
            'the first no_cultures r values in the file, or, if',
            'coordinates are given, r values for the corresponding zone.'
        ),
    }
    data = dict_to_json(data)

    # Check not overwritting data_files.
    assert out_file.split("/")[0] == 'sim_fits'

    with open(out_file, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)


# Main
script, rows, cols, guess_no = argv

rows = int(rows)
cols = int(cols)
guess_no = int(guess_no)
model = CompModel()
true_file = "sim_data/16x24_comp_model/{0}x{1}.json".format(rows, cols)

# Define initial guess
# C_0, N_0, kn
plate_lvl_guess = [0.0001, 1.2, 0.0]


if guess_no >= 0:
    # Messy code to sort out kn = 0.0 guess
    if plate_lvl_guess[-1] == 0.0:
        out_dir = "sim_fits/{0}x{1}_comp_model_kn_guess_0/init_guess_{2}/"
        out_dir = out_dir.format(rows, cols, guess_no)
    else:
        out_dir = "sim_fits/{0}x{1}_comp_model/init_guess_{2}/"
        out_dir = out_dir.format(rows, cols, guess_no)

    guess_file = "init_guess/16x24_rs_mean_5_var_3/16x24_rs_{}.json"
    guess_file = guess_file.format(guess_no)
elif guess_no == -1:
    # Messy code to sort out kn = 0.0 guess
    if plate_lvl_guess[-1] == 0.0:
        out_dir = "sim_fits/{0}x{1}_comp_model_kn_guess_0/uniform_guess/"
        out_dir = out_dir.format(rows, cols)
    else:
        out_dir = "sim_fits/{0}x{1}_comp_model/uniform_guess/"
        out_dir = out_dir.format(rows, cols)

    guess_file = 'No file: uniform guess using r_mean'
else:
    raise ValueError("Guess for guess_no {} does not exist.".format(guess_no))


# Read in true data
with open(true_file, 'r') as f:
    true_data = json.load(f)

true_plate = Plate(rows, cols)
true_plate.times = true_data['times']
true_plate.sim_params = true_data['sim_params']
true_plate.set_sim_data(model)
assert np.array_equal(true_plate.c_meas, true_data['c_meas'])


# Find coords on full plate if exist in data.
if 'coords_on_parent' in true_data.keys():
    coords = true_data['coords_on_parent']
else:
    coords = []

if guess_no >= 0:
    # Read in an initial guess for rs
    with open(guess_file, 'r') as f:
        guess_data = json.load(f)
        r_guess = guess_data['rand_rs']
    # If coords are given for a zone of a larger plate take the
    # initial guess from that zone. This may not make much of a
    # difference but is more consistant.
    if rows*cols < len(r_guess) and coords:
        r_guess =  get_zone_r_guess(r_guess, 16, 24, coords, rows, cols)
    elif rows*cols < len(r_guess) and not coords:
        r_guess = r_guess[:rows*cols]
elif guess_no == -1:
    r_guess = [true_data['r_mean']]*(rows*cols)
else:
    raise ValueError("Guess for guess_no {} does not exist.".format(guess_no))

assert len(r_guess) == rows*cols
init_guess = np.append(plate_lvl_guess,  r_guess)
assert len(init_guess) == len(true_data['sim_params'])

# Fit varying factr and save everytime.
factrs = reversed([10**i for i in range(15)])

tot_fit_time = 0
tot_nfev = 0
tot_nit = 0

# this_plate stores initial guesses for each iteration
this_plate = Plate(true_plate.rows, true_plate.cols)
this_plate.times = true_plate.times
# Sim params is actually the init_guess
this_plate.sim_params = init_guess
this_plate.set_sim_data(model)


for factr in factrs:
    power = str(int(round(np.log(factr)/np.log(10))))
    out_file = out_dir + "stop_factr_10e{}.json".format(power)

    fit_options = {
        'ftol': factr*np.finfo(float).eps,
        'disp': False,
    }

    this_plate.comp_est = true_plate.fit_model(model,
                                               this_plate.sim_params,
                                               custom_options=fit_options)

    # need to accumulate fit_times, nfev, and nit.
    tot_fit_time += this_plate.comp_est.fit_time
    tot_nfev += this_plate.comp_est.nfev
    tot_nit += this_plate.comp_est.nit
    this_plate.comp_est.tot_fit_time = tot_fit_time
    this_plate.comp_est.tot_nfev = tot_nfev
    this_plate.comp_est.tot_nit = tot_nit

    # Create estimated plate and use as next this_plate.
    est_plate = Plate(true_plate.rows, true_plate.cols)
    est_plate.times = true_plate.times
    est_plate.sim_params = this_plate.comp_est.x
    est_plate.set_sim_data(model)

    save_as_json(true_plate, est_plate, this_plate.comp_est, factr,
                 init_guess, coords, true_file, guess_file, out_file)

    this_plate = est_plate


    # Could plot if no_cultures <= 25
    if rows*cols <= 25:
        comp_plotter = Plotter(model)
        title = "factr = 10e" + power
        plot_file = out_dir + "plots/stop_factr_10e{}.pdf".format(power)

        comp_plotter.plot_est(true_plate, est_plate.sim_params,
                              title=title, sim=True,
                              filename=plot_file)
