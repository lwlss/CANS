import numpy as np
import json
import datetime


from cans2.plate import Plate
from cans2.model import CompModel
#from cans2.plotter import Plotter
from cans2.funcs import calc_devs, dict_to_json


def save_as_json(true_plate, est_plate, est, factr, init_guess, model,
                 plate_file, init_guess_file, outfile):

    assert all(est_plate.sim_params == est)

    # Calculate parameter deviations
    assert all(true_data['params'] == model['params'])
    param_devs = calc_devs(true_plate.sim_params, model.r_index,
                           est_plate.sim_params)

    # Read true data from file.
    with open(plate_file, 'r') as f:
        true_data = json.load(f)

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

        'fit_model': model.name,
        'fit_model_species': model.species,
        'fit_model_params': model.params,

        'plate_file': plate_file,
        'init_guess_file': init_guess_file,
        'init_guess': init_guess,
        'est_params': est_plate.sim_params,
        'param_devs': param_devs,
        'est_amounts': est_plate.sim_amounts,
        'est_c_meas': est_plate.c_meas,

        'fit_bounds': est.bounds,
        'fit_options': est.fit_options,    # Dict already jsoned.
        'ftol': est.fit_options['ftol'],
        'factr': factr,
        'machine_eps': np.finfo(float).eps,
        'fit_method': est.method,

        'obj_fun_val': est.fun,
        'fit_success': est.success,
        'reason_for_stop': est.message,

        # These should be tallied for the loop instead/as well.
        'fit_time': est.fit_time,
        'fit_time_accumulated':,
        'nfev': est.nfev,
        'nfev_accumulated':,
        'nit': est.nit,
        'nit_accumulated':,

        'date': datetime.date.today(),
        'description': '',
    }
    data = dict_to_json(data)

    # with open(outfile, 'w') as f:
    #     json.dump(data, f, sort_keys=True, indent=4)



# Parse in a number for an initial guess.
guess_no = 0


rows = 2
cols = 1
model = CompModel()

# Read in true data
true_file = "sim_data/16x24_comp_model/2x1_zone.json"
with open(true_file, 'r') as f:
    true_data = json.load(f)

true_plate = Plate(rows, cols)
true_plate.times = true_data['times']
true_plate.sim_params = true_data['sim_params']
true_plate.set_sim_data(model)
assert all(true_plate.c_meas == true_data['c_meas'])


# MAKE GUESS. Just use a slice of 16x24 random rs for smaller
# arrays. Could also have done for sim params but not if we have also
# simed amounts.
guess_file = "init_guess/16x24_rs_mean_5_var_3/16x24_rs_{}.json"
guess_file = guess_file.format(guess_no)

# C_0, N_0, kn
plate_lvl_guess = [0.00001, 1.2, 0.0]

# Read in an initial guess for rs
with open(guess_file, 'r') as f:
    guess_data = json.load(f)
r_guess = guess_data['rand_rs'][:rows*cols]
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


    est_plate = Plate(true_plate.rows, true_plate.cols)
    est_plate.times = true_plate.times
    est_plate.sim_params = this_plate.comp_est.x
    est_plate.set_sim_data(model)

    save_as_json(true_plate, est_plate, est, factr,)

    this_plate = est_plate


    # Could plot if no_cultures <= 25
    # comp_plotter = Plotter(model)
    # comp_plotter.plot_estimates(emp_plate, emp_plate.comp_est.x,
    #                             title="factr = 10e"+str(np.log(factr)/np.log(10)), sim=True)
