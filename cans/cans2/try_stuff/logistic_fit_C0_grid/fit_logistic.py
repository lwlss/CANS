import numpy as np
import sys
import json
import itertools


from cans2.cans_funcs import dict_to_json, cans_to_json
from cans2.parser import get_plate_data
from cans2.plate import Plate
from cans2.guesser import fit_log_eq
from cans2.model import IndeModel
from cans2.process import remove_edges
from cans2.plotter import Plotter


def fit_log_eq(plate, C_0):
    """Fit the logistic equivalent model for a fixed C_0."""
    # Use final amounts of cells as inital guesses of nutrients.
    C_fs = plate.c_meas[-plate.no_cultures:]
    all_bounds = [[(C_0, C_0), (C_f*0.7, C_f*1.3), (0.0, 1000.0)] for C_f in C_fs]
    guesses = [[C_0] + [N_0_guess, None] for N_0_guess in C_fs]
    # Cover a range of b_guesses for each culture.
    b_guesses = np.linspace(10, 100, 19)
    log_eq_mod = IndeModel()
    obj_funs = []
    params = []
    used_b_guesses = []
    for guess, bounds, culture in zip(guesses, all_bounds, plate.cultures):
        culture_ests = []
        for b_guess in b_guesses:
            guess[-1] = b_guess
            culture_ests.append((culture.fit_model(log_eq_mod, guess, bounds),
                                 b_guess))
        best = min(culture_ests, key=lambda est: est[0].fun)
        culture.log_est = best[0]
        params.append(best[0].x)
        obj_funs.append(best[0].fun)
        used_b_guesses.append(best[1])

    return np.array(params), np.array(obj_funs), np.array(used_b_guesses)


# Plate level C_0 to use as fixed param.
C_0s_index = int(sys.argv[1])

all_C_0s = np.logspace(-7, -2, 1000)
C_0s = all_C_0s[C_0s_index:C_0s_index+20]

outpath = "results2/log_eq_fit_fixed_argv_{0}_C_0_index{1}.json"
plotpath = "plots/log_eq_fit_fixed_argv_{0}_C_0_index{1}.pdf"
error_file = "error_log.txt"

# read in plate 15 data and make a plate.
data_path = "../../../../data/p15/Output_Data/"
plate_data = get_plate_data(data_path)


for C_0_index, C_0 in enumerate(C_0s):

    plate = Plate(plate_data["rows"], plate_data["cols"],
                  data=plate_data)
   # try:
    params, obj_funs, b_guessed = fit_log_eq(plate, C_0)
    # #except Exception as e:
    #     err_msg = "Fitting: arg_v {0}, C_0_index {1},\n".format(sys.argv[1],
    #                                                             C_0_index)
    #     with open(error_file, 'a') as f:
    #         f.write(err_msg)
    #     continue

    Ks = [N_0 + C_0 for N_0 in params[:, 1]]
    rs = [b*K for b, K in zip(params[:, 2], Ks)]

    data = cans_to_json(plate, IndeModel())
    extra_data = {
        "plate_lvl_C_0": C_0,
        "culture_est_params": params,
        "obj_fun": np.sum(obj_funs),
        "obj_funs": obj_funs,
        "obj_funs_internals": remove_edges(obj_funs),
        "arg_v": sys.argv[1],
        "data": "p15",
        "b_guesses": b_guessed,
        "logistic_rs": rs,
        "logistic_Ks": Ks,
    }

    data.update(extra_data)

    try:
        with open(outpath.format(sys.argv[1], C_0_index), "w") as f:
            json.dump(dict_to_json(data), f, indent=4, sort_keys=True)
    except Exception as e:
        err_msg = "Saving: arg_v {0}, C_0_index {1}\n".format(sys.argv[1], C_0_index)
        with open(error_file, 'a') as f:
            f.write(err_msg)
        continue

    plotter = Plotter(IndeModel())
    plotter.plot_culture_fits(plate, IndeModel(),
                              title="Logistic Equivalent Fit (C_0 = {0:.2e})".format(C_0),
                              est_name="log_est")

    # plotter.plot_culture_fits(plate, IndeModel(),
    #                           title="Logistic Equivalent Fit (C_0 = {0:.2e})".format(C_0),
    #                           est_name="log_est",
    #                           filename=plotpath.format(sys.argv[1], C_0_index, int(b_guess)))
