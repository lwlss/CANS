"""Fit independent model, stop every 50 iterations, save values, and
use parameter estimates as starting value for the next 50 iterations."""
import numpy as np
import json

import competition as comp
import inde
from fitting import calc_devs

from cans import add_noise, find_neighbourhood


dir_name = 'results/calibrate_tolerance/'

rows = 3
cols = 3
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)



# Generate random parameters
true_params = comp.gen_params(no_cultures, mean=1.0, var=1.0)

true_amounts = comp.solve_model(no_cultures, times, neighbourhood, true_params)
noisey_amounts = add_noise(true_amounts)

# c_meas = [true_amounts[:, i*2] for i in range(no_cultures)]
# c_meas = add_noise(c_meas)

# Uniform initial guess
init_guess = inde.gen_params(no_cultures).tolist()
comp.plot_growth(rows, cols, noisey_amounts, times)

no_iters = 0
success = False
while not success:
    inde_param_est = inde.fit_model(rows, cols, times, noisey_amounts,
                                    init_guess=init_guess, maxiter=49)
    est_amounts = inde.solve_model(no_cultures, times, neighbourhood,
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

    data = {
        'true_params': true_params,
        'inde_est': inde_param_est,
        'inde_devs': inde_devs,
        'no_iters': no_iters,
        'obj_fun': obj_fun,
        'nfev': nfev,
        'reason_for_stop': reason_for_stop
    }

    # Json requires np.ndarray to be dumped as a list.
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            data[k] = v.tolist()

    data_file = (dir_name + 'inde_fit_after_{}_iters.json'.format(no_iters))
    with open(data_file, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

    inde.plot_growth(rows, cols, est_amounts, times,
                     title='Inde fits after {} iterations'.format(no_iters),
                     filename=dir_name
                     + 'plots/inde_fit_after_{}_iters.pdf'.format(no_iters),
                     data=noisey_amounts)

        # Also plot fits
        # Want valus of tol after each set of iterations
