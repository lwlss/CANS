import numpy as np
import json


from cans2.plotter import Plotter


# Parse in a number for an initial guess.
guess_no = 0

rows = 2
cols = 1

# Read in true data
true_file = "sim_data/16x24_comp_model/2x1_zone.json"
with open(true_file, 'r') as f:
    true_data = json.load(f)


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
init_guess_0 = plate_lvl_guess + r_guess
assert len(init_guess) == len(true_data['sim_params'])


# Fit varying factr and save everytime.

init_guess = copy.deepcopy(init_guess_0)
timings = []

factrs = reversed([10**i for i in range(20)])    # could make 15


for factr in factrs:
    fit_options = {
        'ftol': factr*np.finfo(float).eps
    }

    emp_plate.comp_est = emp_plate.fit_model(comp_model, init_guess,
                                             custom_options=fit_options)
    timing = emp_plate.fit_time

    init_guess = emp_plate.comp_est.x


    # Need to save all of the attributes we have assigned to the
    # estimate and anything else we need.

    # comp_plotter = Plotter(comp_model)
    # comp_plotter.plot_estimates(emp_plate, emp_plate.comp_est.x,
    #                             title="factr = 10e"+str(np.log(factr)/np.log(10)), sim=True)
