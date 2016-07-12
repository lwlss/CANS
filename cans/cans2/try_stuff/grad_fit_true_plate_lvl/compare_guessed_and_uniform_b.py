import json
import numpy as np
import time
import sys


from cans2.cans_funcs import dict_to_numpy, est_to_json
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
b_guesses = b_mean*B_FACTRS

for b_guess in b_guesses[0:2]:
    exp_name = "sim_{0}_b_guess_{1}_{2}".format(sim, b_guess, guessing)
    outfile = results_dir + exp_name + ".json"
    plot_file = results_dir + "plots/" + exp_name + ".pdf"

    if guessing == "uniform":
        param_guess = np.concatenate((plate_lvl,
                                      np.repeat(50.0, plate.no_cultures)))
    elif guessing == "imag_neigh":
        imag_neigh_params = [kn, kn, 0.0, b_guess*1.5, b_guess]
        t0 = time.time()
        param_guess, guesser = fit_imag_neigh(plate, model,
                                              area_ratio=None,
                                              C_ration=None,
                                              imag_neigh_params=imag_neigh_params,
                                              plate_lvl=plate_lvl)
        t1 = time.time()

    t2 = time.time()
    plate.est = plate.fit_model(model, param_guess, bounds,
                                rr=True, minimizer_opts={"disp": True})
    t3 = time.time()

    # Get data
    est_data = est_to_json(plate, model, plate.est.x, plate.est.fun,
                           t3-t2, bounds, param_guess, sim=True)
    est_data["guess_method"] = guessing
    est_data["b_guess"] = b_guess
    est_data["data_path"] = data_path
    if guessing == "imag_neigh":
        est_data["guess_time"] = t1 - t0
        est_data["total_time"] = t3 - t0
        est_data["imag_neigh_params"] = imag_neigh_params

    with open(outfile, "w") as f:
        json.dump(est_data, f, indent=4, sort_keys=True)

    title = "Fix true plate level params and grad fit (sim {0}; b_guess {1}; {2})."
    title.format(sim, b_guess, guessing)
    plotter.plot_est_rr(plate, plate.est.x, title, sim=True,
                        filename=plot_file)
