import numpy as np
import csv

from cans import find_neighbourhood, mad

import competition as comp
import inde


rows = 1
cols = 1
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)
dir_name = "results/comp_sim_fits_vary_kn_16x24/"

# Vary kn for each plate simulation
kn_params = np.linspace(0, 0.2, 6)
init_amounts = comp.gen_amounts(no_cultures)
# Have random rs but the same for each kn
r_params = inde.gen_params(no_cultures)

for sim in range(no_cultures):
    params = np.append(kn_params[sim], r_params)
    true_params = np.append(init_amounts[:2], params)
    assert(len(true_params) == 3 + no_cultures)
    true_amounts = comp.solve_model(init_amounts, times, neighbourhood, params)


    # Fit comp and inde models to estimate parameters
    comp_param_est = comp.fit_model(rows, cols, times, true_amounts)
    comp_param_est = comp_param_est.x
    inde_param_est = inde.fit_model(rows, cols, times, true_amounts)
    inde_param_est = np.insert(inde_param_est.x, 2, np.nan)

    # Plate level devs
    true_plate_lvl = true_params[:3]
    comp_devs = np.abs(true_plate_lvl - comp_param_est[:3])
    inde_devs = np.abs(true_plate_lvl[:3] - inde_param_est[:3])

    # r MADs
    comp_r_mad = mad(true_params[3:], comp_param_est[3:])
    inde_r_mad = mad(true_params[3:], inde_param_est[3:])


    kn_table = [
        ["kn"],
        [kn_params[sim]]
    ]

    dev_table = [
        ["deviations"],
        ["param", "comp dev", "inde dev"],
        ["C(t=0)", comp_devs[0], inde_devs[0]],
        ["N(t=0)", comp_devs[1], inde_devs[1]],
        ["kn", comp_devs[2], inde_devs[2]],
        ["r (MAD)", comp_r_mad, inde_r_mad]
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
