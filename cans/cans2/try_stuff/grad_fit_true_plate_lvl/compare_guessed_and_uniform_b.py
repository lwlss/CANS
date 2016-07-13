import json
import numpy as np
import time
import sys


from cans2.cans_funcs import dict_to_numpy, dict_to_json, est_to_json, mad
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.genetic_kwargs import _get_plate_kwargs
from cans2.guesser import fit_imag_neigh


# Factors to multiply b_avg to give b_guess. The best fits have b_avg
# in range (44.4, 56.4).
B_FACTRS = np.linspace(0.5, 1.5, 11)
GUESSING = ["imag_neigh", "uniform"]

sim = int(sys.argv[1])
guessing = GUESSING[int(sys.argv[2])]

data_path = "data/local_min_sims/sim_{0}.json".format(sim)
results_dir = "results/local_min_sims/"
error_file = results_dir + "error_log.txt"

# Read in sim data and make plate.
with open(data_path, 'r') as f:
    data = dict_to_numpy(json.load(f))

plate = Plate(**_get_plate_kwargs(data))
plate.sim_amounts = data["sim_amounts"]
plate.sim_params = data["sim_params"]
model = CompModelBC()
plate.set_rr_model(model, data["sim_params"])
plotter = Plotter(model)

# Put strict bounds on the plate level parameters then fit.
plate_lvl = plate.sim_params[:model.b_index]
plate_lvl_bounds = np.array([[p, p] for p in plate_lvl])

kn = plate_lvl[model.params.index("kn")]

b_bounds = np.array([[0.0, 200.0] for i in range(plate.no_cultures)])    # Could adjust upper by b_guess
bounds = np.concatenate((plate_lvl_bounds, b_bounds))

# Make b_guesses to loop through for each sim and guess type.
b_mean = np.mean(plate.sim_params[-plate.no_cultures:])
B_GUESSES = B_FACTRS*b_mean

for b_index, b_guess in enumerate(B_GUESSES):
    exp_name = "sim_{0}_b_index_{1}_{2}".format(sim, b_index, guessing)
    outfile = results_dir + exp_name + ".json"
    plot_file = results_dir + "plots/" + exp_name + ".pdf"

    if guessing == "uniform":
        param_guess = np.concatenate((plate_lvl,
                                      np.repeat(50.0, plate.no_cultures)))
    elif guessing == "imag_neigh":
        # Using 1.0 rather than the candidate plate_lvl kn. "kn1" and
        # "kn2" may take completely different values to the comp model
        # kn. Trying both shows that we produce the same estimates in
        # the same time anyway.
        imag_neigh_params = [1.0, 1.0, 0.0, b_guess*1.5, b_guess]
        try:
            t0 = time.time()
            param_guess, guesser = fit_imag_neigh(plate, model,
                                                  area_ratio=None,
                                                  C_ratio=None,
                                                  imag_neigh_params=imag_neigh_params,
                                                  plate_lvl=plate_lvl)
            t1 = time.time()
        except Exception as e:
            error_log = "Imag guess: arg_vs {0}, {1}, b_index {2},\n"
            error_log = error_log.format(sys.argv[1], sys.argv[2], b_index)
            with open(error_file, 'a') as f:
                f.write(error_log)
            continue

    try:
        t2 = time.time()
        plate.est = plate.fit_model(model, param_guess, bounds,
                                    rr=True, minimizer_opts={"disp": False})
        t3 = time.time()
    except Exception as e:
        error_log = "Full est: arg_vs {0}, {1}, b_index {2},\n"
        error_log = error_log.format(sys.argv[1], sys.argv[2], b_index)
        with open(error_file, 'a') as f:
            f.write(error_log)
        continue

    est_data = est_to_json(plate, model, plate.est.x, plate.est.fun,
                           t3-t2, bounds, param_guess, sim=True)
    est_data["guess_method"] = guessing
    est_data["b_guess"] = b_guess
    est_data["b_index"] = b_index
    est_data["B_GUESSES"] = B_GUESSES
    est_data["data_path"] = data_path
    est_data["b_MAD"] = mad(plate.est.x[-plate.no_cultures:], plate.sim_params[-plate.no_cultures:])
    if guessing == "imag_neigh":
        est_data["guess_time"] = t1 - t0
        est_data["total_time"] = t3 - t0
        est_data["imag_neigh_params"] = imag_neigh_params

    with open(outfile, "w") as f:
        json.dump(dict_to_json(est_data), f, indent=4, sort_keys=True)

    try:
        title = "Fix true plate level params and grad fit (sim {0}; b_index {1}; {2})."
        title.format(sim, b_index, guessing)
        plotter.plot_est_rr(plate, plate.est.x, title, sim=True,
                            filename=plot_file)
    except Exception as e:
        error_log = "Plotting: arg_vs {0}, {1}, b_index {2},\n"
        error_log = error_log.format(sys.argv[1], sys.argv[2], b_index)
        with open(error_file, 'a') as f:
            f.write(error_log)
        continue
