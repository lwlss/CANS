import numpy as np
import csv

from cans import find_neighbourhood

import competition as comp
import inde



rows = 1
cols = 1
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)
dir_name = "results/comp_sim_fits_16x24/"

# Vary kn for each plate simulation
kn_params = np.linspace(0, 0.1, 11)
print(kn)
init_amounts = comp.gen_amouts(no_cultures)

for sim in range(11):
    r_params = inde.gen_params(no_cultures)
    params = np.append(kn_params[sim], r_params)

    true_amounts = solve_model(init_amounts, times, neighbourhood, params)

    # Fit comp and inde models to estimate parameters
    comp_param_est = comp.fit_model(rows, cols, times, true_amounts)
    inde_param_est = inde.fit_model(rows, cols, times, true_amounts)

    # Now solve using estimated parameters.
    comp_amount_est = comp.solve_model(np.tile(comp_param_est.x[:2], no_cultures),
                                       times, neighbourhood, comp_param_est.x[2:])
    inde_amount_est = inde.solve_model(np.tile(inde_param_est.x[:2], no_cultures),
                                       times, neighbourhood, inde_param_est.x[2:])

    # Plot truth, comp fit, and inde fit.
    comp.plot_growth(rows, cols, true_amounts, times,
                     title="Truth (kn={0})".format(kn[sim]),
                     filename='{0}truth_{1}.pdf'.format(dir_name, sim))
    comp.plot_growth(rows, cols, comp_amount_est, times,
                     title="Estimation (Comp kn={0})".format(kn[sim]),
                     filename='{0}comp_est_{1}.pdf'.format(dir_name, sim))
    comp.plot_growth(rows, cols, inde_amount_est, times,
                     title="Estimation (Inde kn={0})".format(kn[sim]),
                     filename='{0}inde_est_{1}.pdf'.format(dir_name, sim))


    # Save parameters and deviations
