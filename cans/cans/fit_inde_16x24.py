"""Independent fit of a 16x24 comp sim with kn=0."""
import csv
import numpy as np
import json


import inde
import competition as comp
from fitting import calc_devs
from cans import find_neighbourhood


# Read in same 16x24 data as before for kn=0
# This time use stricter stopping criteria for independent model.
rows = 16
cols = 24
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)
dir_name = 'results/comp_sim_fits_vary_kn_16x24/strict_stop/'

param_file = dir_name + 'sim_0_true_params.csv'
with open(param_file, 'r') as f:
    param_reader = csv.reader(f)
    true_params = np.array([float(row[0]) for row in param_reader])

# Test params
# true_params = [0.01, 1.0, 0.0] + inde.gen_params(no_cultures)

init_amounts = np.tile(true_params[:2], no_cultures)
true_amounts = comp.solve_model(init_amounts, times,
                                neighbourhood, true_params[2:])
# comp.plot_growth(rows, cols, true_amounts, times)

for maxiter in (1000, None):
    inde_param_est = inde.fit_model(rows, cols, times, true_amounts)
    no_iters = inde_param_est.nit
    reason_for_stop = str(inde_param_est.message)
    inde_param_est = np.insert(inde_param_est.x, 2, np.nan)

    inde_devs = calc_devs(true_params, 3, inde_param_est)[0]

    data = {
        'true_params' : true_params,
        'inde_est' : inde_param_est,
        'inde_devs' : inde_devs,
        'no_iters' : no_iters,
        'reason_for_stop' : reason_for_stop
    }

    # Json requires np.ndarray to be dumped as a list.
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            data[k] = v.tolist()

    data_file = (dir_name
                 + 'inde_param_devs_0_strict_stop_{}.json'.format(maxiter))
    with open(data_file, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
