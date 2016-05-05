import numpy as np
import json


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
dir_name = "results/fix_comp_kn_zero_fits2/use_inde_est/"
plot_dir = dir_name + "plots/"
# Vary kn for each plate simulation
# kn_params = [0.0]
kn_params = np.linspace(0, 0.2, 11)

all_data = []
for sim in range(len(kn_params)):
    # Read in ill fitted data from file then try different ways of improve fit.
    with open('results/fix_comp_kn_zero_fits2/sim_0_data.json', 'r') as f:
        data = json.load(f)
        true_params = data['true_params']
        true_params[2] = kn_params[sim]
        init_amounts = np.tile(true_params[:2], no_cultures)

        true_amounts = comp.solve_model(init_amounts, times,
                                        neighbourhood, true_params[2:])

        # Check plot visually.
        # comp.plot_growth(rows, cols, true_amounts, times, title="Truth")

        # Fit comp and inde models to estimate parameters
        inde_param_est, comp_param_est = fit_inde_and_comp(rows, cols,
                                                           times, true_amounts,
                                                           use_inde=True)

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

# Finally save all json in one file.
save_all_json(all_data, kn_params, dir_name)
