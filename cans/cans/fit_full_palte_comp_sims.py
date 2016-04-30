import numpy as np
import csv

from cans import find_neighbourhood, mad

import competition as comp
import inde


rows = 16
cols = 24

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


    table = [
        ["C(t=0)", plate_lvl[0]], ["N(t=0)", plate_lvl[1]],
        ["S(t=0)", plate_lvl[2]], ["kn", plate_lvl[3]], ["ks", plate_lvl[4]],
        ["r (MAD)", r_mad], ["b", plate_lvl[5]], ["a", plate_lvl[6]]
    ]

    # Save parameters and deviations
    outfile = dir_name + 'param_devs_{}.csv'.format(sim)
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([["kn", kn_params[sim]],])
        writer.writerows(table)
        writer.writerows([["True_params"],])
        writer.writerows([[val] for val in true_params])
        writer.writerows([["Est_params"],])
        writer.writerows([[val] for val in est_params.x])







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
