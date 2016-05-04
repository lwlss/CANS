import numpy as np
import json
import csv


import competition as comp
import inde


from cans import find_neighbourhood, mad


def fit_inde_and_comp(rows, cols, times, true_amounts):
    """Fit inde and comp models and return param estimates.

    Also add nan for the inde estimate of kn in the correct position.
    """
    inde_param_est = inde.fit_model(rows, cols, times, true_amounts)
    inde_param_est = np.insert(inde_param_est.x, 2, np.nan)
    comp_param_est = comp.fit_model(rows, cols, times, true_amounts)
    comp_param_est = comp_param_est.x
    return inde_param_est, comp_param_est


# This function is general.
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


def save_json(true_params, inde_est, comp_est, inde_devs, comp_devs,
              dir_name, sim):
    """Save true parameters and comp and inde estimates as json."""
    data = {}
    data['kn'] = true_params[2]
    data['true_params'] = true_params
    data['inde_est'] = inde_est
    data['comp_est'] = comp_est
    data['inde_devs'] = inde_devs
    data['comp_devs'] = comp_devs
    data['description'] = ("Parameters and estimates are lists of "
                           "C(t=0), N(t=0), kn, r0, r1,... "
                           "Mean absolute deviations are take for "
                           "growth rates r_i.")
    # Json requires np.ndarray to be dumped as a list.
    for k, v in data.items():
        if isinstance(v, np.ndarray):
            data[k] = v.tolist()
    with open(dir_name + 'sim_{}_data.json'.format(sim), 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
    return data


def save_all_json(all_data, kn_params, dir_name):
    """Save all of the data for every kn simulation in one json file."""
    all_data = dict(zip(map(str, kn_params), all_data))
    all_data['description'] = ("Keys are the values of kn used in simulations "
                               "with data stored in the corresponding "
                               "sub-dictionary.")
    with open(dir_name + 'all_data.json', 'w') as f:
        json.dump(all_data, f, sort_keys=True, indent=4)


def save_csv(true_params, inde_est, comp_est, inde_devs, comp_devs,
             no_cultures, dir_name, sim):
    """Save true parameters and comp and inde estimates as csv."""
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
    # Could use len(params[:3]) rather than no_cultures.
    param_names += ["r{}".format(i) for i in range(no_cultures)]
    param_vals = [list(tup) for tup in
                  zip(param_names, true_params, inde_est, comp_est)]
    param_table = [
        ["params"],
        ["param", "true", "inde est", "comp est"]
    ]
    param_table += param_vals
    outfile = dir_name + 'sim_{}_data.csv'.format(sim)
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(kn_table)
        writer.writerows(dev_table)
        writer.writerows(param_table)


def plot_fits(true_amounts, true_kn, inde_est, comp_est, times,
              rows, cols, plot_dir, sim):
    no_cultures = rows*cols
    neighbourhood = find_neighbourhood(rows, cols)
    # Now solve using estimated parameters. Do not pass kn for inde est.
    inde_amount_est = inde.solve_model(np.tile(inde_est[:2], no_cultures),
                                       times, neighbourhood, inde_est[3:])
    comp_amount_est = comp.solve_model(np.tile(comp_est[:2], no_cultures),
                                       times, neighbourhood, comp_est[2:])

    # Plot truth, inde fit, and comp fit.
    comp.plot_growth(rows, cols, true_amounts, times,
                     title="Truth (kn={0})".format(true_kn),
                     filename='{0}truth_{1}.pdf'.format(plot_dir, sim))
    comp.plot_growth(rows, cols, inde_amount_est, times,
                     title="Inde Estimation (true kn={0})".format(true_kn),
                     filename='{0}inde_est_{1}.pdf'.format(plot_dir, sim))
    comp.plot_growth(rows, cols, comp_amount_est, times,
                     title="Comp Estimation (true kn={0})".format(true_kn),
                     filename='{0}comp_est_{1}.pdf'.format(plot_dir, sim))


if __name__ == '__main__':
    rows = 3
    cols = 3
    r_index = 3    # Position of first r in parameter lists.
    no_cultures = rows*cols
    neighbourhood = find_neighbourhood(rows, cols)
    times = np.linspace(0, 15, 151)
    dir_name = "results/comp_sim_fits_vary_kn_3x3/"
    plot_dir = dir_name + "plots/"
    # Vary kn for each plate simulation
    # kn_params = [0.0, 0.1, 0.2]
    kn_params = np.linspace(0, 0.2, 11)
    init_amounts = comp.gen_amounts(no_cultures)
    # Have random rs but the same for each kn
    r_params = inde.gen_params(no_cultures)
    all_data = []
    for sim in range(len(kn_params)):
        params = np.append(kn_params[sim], r_params)
        true_params = np.append(init_amounts[:2], params)
        true_amounts = comp.solve_model(init_amounts, times,
                                        neighbourhood, params)

        # Fit comp and inde models to estimate parameters
        inde_param_est, comp_param_est = fit_inde_and_comp(rows, cols,
                                                           times, true_amounts)

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
