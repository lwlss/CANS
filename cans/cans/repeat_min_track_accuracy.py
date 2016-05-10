"""Fit independent model, stop every 50 iterations, save values, and
use parameter estimates as starting value for the next 50 iterations."""
import numpy as np
import json

import competition as comp
import inde
from fitting import calc_devs, to_json

from cans import add_noise, find_neighbourhood


dir_name = 'results/calibrate_tolerance/'

rows = 16
cols = 24
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)
smooth_times = np.linspace(0, 15, 151)   # for plotting estimates
# sigma_noise = 0.00

# Generate random parameters
true_params = comp.gen_params(no_cultures, mean=1.0, var=1.0)
true_params[2] = 0.0
true_amounts = comp.solve_model(no_cultures, times, neighbourhood, true_params)


for sigma_noise in [0.02, 0.04, 0.1]:
    dir_name = 'results/calibrate_tolerance/var_0_0{}_16x24/'.format(int(sigma_noise*100))
    noisey_amounts = add_noise(true_amounts, sigma=sigma_noise)
    data = {
        'times': times,
        'amounts': noisey_amounts
    }

    # Uniform initial guess
    init_guess = inde.gen_params(no_cultures)
    init_guess[0] = 0.001
    init_guess[1] = 1.2
#    comp.plot_growth(rows, cols, noisey_amounts, times)

    meta = {
        'times': times,
        'true_params': true_params,
        'noisey_amounts': noisey_amounts,
        'noise_sigma': sigma_noise,
        'rows': rows,
        'cols': cols,
        'init_guess': init_guess
    }
    meta = to_json(meta)
    with open(dir_name + 'meta.json', 'w') as f:
        json.dump(meta, f)

    no_iters = 0
    success = False
    while no_iters < 200 and not success:
        inde_param_est = inde.fit_model(rows, cols, times, noisey_amounts,
                                        init_guess=init_guess, maxiter=9)
        # Only need if plotting
        est_amounts = inde.solve_model(no_cultures, smooth_times, neighbourhood,
                                       inde_param_est.x)
        # Use estimated parameters as next guess
        init_guess = inde_param_est.x

        success = inde_param_est.success
        no_iters += inde_param_est.nit

        obj_fun = inde_param_est.fun
        nfev = inde_param_est.nfev
        reason_for_stop = str(inde_param_est.message)

        inde_param_est = np.insert(inde_param_est.x, 2, np.nan)
        inde_devs = calc_devs(true_params, 3, inde_param_est)[0]

        fit_data = {
            'true_params': true_params,
            'inde_est': inde_param_est,
            'inde_devs': inde_devs,
            'no_iters': no_iters,
            'obj_fun': obj_fun,
            'nfev': nfev,
            'reason_for_stop': reason_for_stop
        }


        fit_data = to_json(fit_data)
        data_file = (dir_name + 'inde_fit_after_{}_iters.json'.format(no_iters))
        with open(data_file, 'w') as f:
            json.dump(fit_data, f, sort_keys=True, indent=4)

        # inde.plot_growth(rows, cols, est_amounts, times=smooth_times,
        #                  title='Inde fits after {} iterations'.format(no_iters),
        #                  filename=dir_name
        #                  + 'plots/inde_fit_after_{}_iters.pdf'.format(no_iters),
        #                  data=data)
