import numpy as np
import csv

from cans import find_neighbourhood, mad

import competition as comp
import inde


def fit_inde_and_comp(rows, cols, times, true_amounts):
    """Fit inde and comp models and return param estimates.

    Also add nan for the inde estimate of kn in the correct position.
    """
    inde_param_est = inde.fit_model(rows, cols, times, true_amounts)
    inde_param_est = np.insert(inde_param_est.x, 2, np.nan)
    comp_param_est = comp.fit_model(rows, cols, times, true_amounts)
    comp_param_est = comp_param_est.x
    return inde_param_est, comp_param_est


def calc_devs(true_params, r_index, *ests):
    """Return deviations of estimated parameters from true.

    For r return mean absolute deviation. Requires index of first
    r_value. Lists should be of equal length.
    """
    true_plate_lvl = true_params[:r_index]
    true_rs = true_params[r_index:]
    devs = []
    for est in ests:
        dev = np.abs(true_plate_lvl - est[:r_index])
        dev = np.append(dev, mad(true_rs, est[r_index:]))
        devs.append(dev)
    return devs


rows = 1
cols = 1
r_index = 3    # Position of first r in parameter lists.
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)
dir_name = "results/comp_sim_fits_vary_kn_3x3/"

# Vary kn for each plate simulation
kn_params = [0.1]
#kn_params = np.linspace(0, 0.1, 6)
init_amounts = comp.gen_amounts(no_cultures)
# Have random rs but the same for each kn
r_params = inde.gen_params(no_cultures)

for sim in range(len(kn_params)):
    params = np.append(kn_params[sim], r_params)
    true_params = np.append(init_amounts[:2], params)
    true_amounts = comp.solve_model(init_amounts, times, neighbourhood, params)

    # Fit comp and inde models to estimate parameters
    inde_param_est, comp_param_est = fit_inde_and_comp(rows, cols,
                                                       times, true_amounts)

    inde_devs, comp_devs = calc_devs(true_params, r_index,
                                     inde_param_est, comp_param_est)

    kn_table = [
        ["kn"],
        [true_params[2]]
    ]

    dev_table = [
        ["deviations"],
        ["param", "inde dev", "comp dev"],
        ["C(t=0)", inde_devs[0], comp_devs[0]],
        ["N(t=0)", inde_devs[1], comp_devs[1]],
        ["kn", inde_devs[2], comp_devs[2]],
        ["r (MAD)", inde_devs[3], comp_devs[3]]
    ]

    param_names = ["C(t=0)", "N(t=0)", "kn"]
    param_names += ["r{}".format(i) for i in range(no_cultures)]
    param_vals = [list(tup) for tup in
                  zip(param_names, true_params, comp_param_est, inde_param_est)]

    param_table = [
        ["params"],
        ["param", "true", "comp est", "inde est"]
    ]
    param_table += param_vals


    # Should also write actual values (true and estimated) not just devs.
    # Save parameters and deviations
    outfile = dir_name + 'param_devs_{}.csv'.format(sim)
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(kn_table)
        writer.writerows(dev_table)
        writer.writerows(param_table)


    # Not much point in saving plots for 16x24 because they will look
    # really ugly.

    # # Now solve using estimated parameters.
    # comp_amount_est = comp.solve_model(np.tile(comp_param_est.x[:2], no_cultures),
    #                                    times, neighbourhood, comp_param_est.x[2:])
    # inde_amount_est = inde.solve_model(np.tile(inde_param_est.x[:2], no_cultures),
    #                                    times, neighbourhood, inde_param_est.x[2:])

    # # Plot truth, comp fit, and inde fit.
    # comp.plot_growth(rows, cols, true_amounts, times,
    #                  title="Truth (kn={0})".format(kn[sim]),
    #                  filename='{0}truth_{1}.pdf'.format(dir_name, sim))
    # comp.plot_growth(rows, cols, comp_amount_est, times,
    #                  title="Estimation (Comp kn={0})".format(kn[sim]),
    #                  filename='{0}comp_est_{1}.pdf'.format(dir_name, sim))
    # comp.plot_growth(rows, cols, inde_amount_est, times,
    #                  title="Estimation (Inde kn={0})".format(kn[sim]),
    #                  filename='{0}inde_est_{1}.pdf'.format(dir_name, sim))
