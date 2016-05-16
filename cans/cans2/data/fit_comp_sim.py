import numpy as np
import json


# Parse in a number for an initial guess.
guess_no = 0


rows = 2
cols = 1

# Read in true data
true_file = "sim_data/{0}x{1}_comp_model/mean_5_var_3.json".format(rows, cols)
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
init_guess = plate_lvl_guess + r_guess
assert len(init_guess) == len(true_data['sim_params'])
