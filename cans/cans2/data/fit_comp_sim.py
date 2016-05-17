import numpy as np
import json
import datetime


from cans2.zoning import get_zone_r_guess
from cans2.plate import Plate
from cans2.model import CompModel
#from cans2.plotter import Plotter
from cans2.funcs import calc_devs, dict_to_json


def save_as_json(true_plate, est_plate, est, factr, init_guess,
                 plate_file, guess_file, out_file):

    assert np.array_equal(est_plate.sim_params, est.x)

    # Read true data from file.
    with open(plate_file, 'r') as f:
        true_data = json.load(f)

    # Calculate parameter deviations
    assert np.array_equal(true_data['params'], est.model.params)
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
        'reason_for_stop': est.message,

        # For the ftol iter and cumulative.
        'tot_fit_time': est.fit_time,
        'fit_time_tot': est.tot_fit_time,
        'nfev': est.nfev,
        'tot_nfev': est.tot_nfev,
        'nit': est.nit,
        'tot_nit': est.tot_nit,

        'date': datetime.date.today(),
        'description': ('If smaller than a 16x24 plate init_guesses are'
                        'the first no_cultures r values in the file.'),
    }
    data = dict_to_json(data)

    with open(out_file, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)



# Parse in a number for an initial guess.
guess_no = 0
rows = 2
cols = 1
model = CompModel()
out_dir = "{0}x{1}_comp_model/init_guess_{2}/".format(rows, cols, guess_no)
true_file = "sim_data/16x24_comp_model/2x1_zone.json".format(rows, cols)

# Read in true data
with open(true_file, 'r') as f:
    true_data = json.load(f)

# Find coords on full plate if exist
if 'coords_on_parent' in true_data.keys():
    coords = true_data['coords_on_parent']
else:
    coords = []

true_plate = Plate(rows, cols)
true_plate.times = true_data['times']
true_plate.sim_params = true_data['sim_params']
true_plate.set_sim_data(model)
assert np.equal(true_plate.c_meas, true_data['c_meas'])


# MAKE GUESS
guess_file = "init_guess/16x24_rs_mean_5_var_3/16x24_rs_{}.json"   # zones
guess_file = guess_file.format(guess_no)
# C_0, N_0, kn
plate_lvl_guess = [0.00001, 1.2, 0.0]
# Read in an initial guess for rs
with open(guess_file, 'r') as f:
    guess_data = json.load(f)
r_guess = guess_data['rand_rs']
# If coords are given for a zone of a larger plate take the initial
# guess from that zone. This may not make much of a difference but is
# more consistant.
if len(r_guess) < rows*cols and coords:
    r_guess =  get_zone_r_guess(r_guess, coords, rows, cols)
elif len(r_guess) < rows*cols and not coords:
    r_guess = r_guess[:rows*cols]
assert len(r_guess) == rows*cols
init_guess = plate_lvl_guess + r_guess
assert len(init_guess) == len(true_data['sim_params'])


# Fit varying factr and save everytime.
factrs = reversed([10**i for i in range(20)])    # could make 15

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
    fit_options = {
        'ftol': factr*np.finfo(float).eps
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
                 init_guess, true_file, guess_file, out_file)

    save_fit(est_plate, this_plate.comp_est, factr, out_file)

    this_plate = est_plate


    # Could plot if no_cultures <= 25
    # comp_plotter = Plotter(model)
    # comp_plotter.plot_estimates(emp_plate, emp_plate.comp_est.x,
    #                             title="factr = 10e"+str(np.log(factr)/np.log(10)), sim=True)
