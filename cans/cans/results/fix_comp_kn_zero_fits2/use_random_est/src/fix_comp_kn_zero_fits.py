import numpy as np
import json
import random

import competition as comp
import inde


from cans import find_neighbourhood
from fitting import *


rows = 3
cols = 3
r_index = 3    # Position of first r in parameter lists.
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 20, 201)    # Use plenty of points to make sure
                                   # that this is not the issue.

dir_name = "results/fix_comp_kn_zero_fits2/use_random_est/"
plot_dir = dir_name + "plots/"


# Read in ill fitted data from file then try different ways of improve fit.
with open('results/fix_comp_kn_zero_fits2/sim_0_data.json', 'r') as f:
    data = json.load(f)
    true_params = data['true_params']

# Vary kn for each plate simulation
kn_params = np.linspace(0, 0.2, 11)
no_kns = len(kn_params)

# Use three sets of random r parameters.
repeats = 3    # Number of random parameter guesses.
rand_guesses = [comp.guess_params(no_cultures, rand_r=True).tolist()
                for i in range(repeats)]
# Save metadata as json.
meta = {
    'rand_guesses' : rand_guesses,
    'times' : times,
    'kn_params' : kn_params,
    'dims' : [rows, cols],
    'rand_repeats' : repeats
}
meta = to_json(meta)
with open(dir_name + 'meta.json', 'w') as f:
    json.dump(meta, f, sort_keys=True, indent=4)

rand_guesses = np.repeat(rand_guesses, no_kns, axis=0)
all_data = []
count = 0
# Replace each kn in the sets of parameters with the approprate value
for kn, init_guess in zip(np.tile(kn_params, repeats), rand_guesses):
    # Label for saved files
    sim = 'rand_{0}_kn_{1}'.format(int(count//no_kns), count%no_kns)
    true_params[2] = kn
    init_amounts = np.tile(true_params[:2], no_cultures)
    true_amounts = comp.solve_model(init_amounts, times,
                                    neighbourhood, true_params[2:])

    print(init_guess)
    # Check plot visually.
    # comp.plot_growth(rows, cols, true_amounts, times, title="Truth")

    # Fit comp and inde models to estimate parameters
    inde_param_est, comp_param_est = fit_inde_and_comp(rows, cols,
                                                       times, true_amounts,
                                                       start=init_guess)

    inde_devs, comp_devs = calc_devs(true_params, r_index,
                                     inde_param_est, comp_param_est)

    # Save as single json file and append to all_data so that all data
    # may eventually be stored in a single file.
    data = save_json(true_params, inde_param_est, comp_param_est,
                     inde_devs, comp_devs, dir_name, sim)
    all_data.append(data)
    save_csv(true_params, inde_param_est, comp_param_est,
             inde_devs, comp_devs, no_cultures, dir_name, sim)

    # Not much point in saving plots for 16x24 because they will look
    # really ugly.
    plot_fits(true_amounts, true_params[2], inde_param_est, comp_param_est,
              times, rows, cols, plot_dir, sim)
    count += 1

# Finally save all json in one file.
save_all_json(all_data, kn_params, dir_name)
