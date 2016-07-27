import numpy as np
import json
import sys
import itertools
import time


from cans2.parser import get_plate_data
from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC
from cans2.guesser import fit_imag_neigh, fit_log_eq, Guesser
from cans2.cans_funcs import dict_to_json
from cans2.plotter import Plotter


# Temporarily work with a zone while checking script runs.
# from cans2.zoning import get_plate_zone


# Process script args
method_index = int(sys.argv[1])    # 5 for ('imag_neigh', 0.0001, False)
# In total 5x2x2 = 20 sets of args.
cell_ratios = np.logspace(-3, -5, num=5)
fit_type = ["imag_neigh", "log_eq"]
zero_kn = [True, False]
guess_vars = list(itertools.product(fit_type, cell_ratios, zero_kn))
guess_var = guess_vars[method_index]

# Read in real data and make a plate.
data_path = "../../data/p15/Output_Data/"
plate_data = get_plate_data(data_path)
full_plate = Plate(plate_data["rows"], plate_data["cols"],
                   data=plate_data)
# zone = get_plate_zone(full_plate, (5,5), 3, 3)

plate_model = CompModelBC()    # Should pass another argument for CompModel()

# Errors are captured to file and iteration skipped.
error_file = "results/p15_fits/full_plate/CompModel_error_log.txt"
for b_guess in [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 95, 100, 150]:
    # User defined/selected parameters pre guessing.
    guess_kwargs = {
        "plate": full_plate,
        "plate_model": plate_model,
        "C_ratio": guess_var[1],    # Guess of init_cells/final_cells.
        "kn_start": 0.0,
        "kn_stop": 2.0,
        "kn_num": 21,
    }
    imag_neigh_only = {
        "area_ratio": 1.5,        # Guess of edge_area/internal_area.
        # Not including amounts which are guesses from final cell amounts
        # and the C_ratio argument. ['kn1', 'kn2', 'b-', 'b+', 'b'] The
        # final parameter is the guess of the CompModel parameter b. Other
        # parameters are uniquie to the imaginary neighbour model.
        "imag_neigh_params": np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess]),
        "no_neighs": None,    # Can specify or allow it to be calculated np.ceil(C_f/N_0)
    }
    log_eq_only = {
        "b_guess": b_guess,
    }

    # Get parameter guesses for fitting.
    if guess_var[0] == "imag_neigh":
        guess_kwargs.update(imag_neigh_only)
        try:
            quick_guess, quick_guesser = fit_imag_neigh(**guess_kwargs)
        except Exception as e:
            error_log = "imag guess: arg_v {0}, b_guess {1},\n".format(sys.argv[1],
                                                                       b_guess)
            with open(error_file, 'a') as f:
                f.write(error_log)
            continue
    elif guess_var[0] == "log_eq":
        guess_kwargs.update(log_eq_only)
        try:
            quick_guess, quick_guesser = fit_log_eq(**guess_kwargs)
        except Exception as e:
            error_log = "log guess: arg_v {0}, b_guess {1},".format(sys.argv[1],
                                                                   b_guess)
            with open(error_file, 'a') as f:
                f.write(error_log)
            continue
    if guess_var[2]:
        quick_guess[guess_kwargs["plate_model"].params.index("kn")] = 0.0

    full_plate.set_rr_model(plate_model, quick_guess, outfile="")

    # Make bounds for fitting.
    if guess_var[0] == "imag_neigh":
        area_ratio = guess_kwargs["area_ratio"]
    elif guess_var[0] == "log_eq":
        area_ratio = 1.0

    plate_guesser = Guesser(full_plate, guess_kwargs["plate_model"],
                            area_ratio, guess_kwargs["C_ratio"])
    bounds = plate_guesser.get_bounds(quick_guess, C_doubt=1e3,
                                      N_doubt=2.0, kn_max=10.0)    # Could also try kn_max=None.

    t0 = time.time()
    # Now fit the model to the plate and save the result and plot as
    # json and pdf.
    try:
        full_plate.est = full_plate.fit_model(guess_kwargs["plate_model"],
                                              param_guess=quick_guess,
                                              bounds=bounds, rr=True, sel=False,
                                              minimizer_opts={"disp": False})
    except Exception as e:
        error_log = "Full est: arg_v {0}, b_guess {1},\n".format(sys.argv[1],
                                                                 b_guess)
        with open(error_file, 'a') as f:
            f.write(error_log)
        continue
    t1 = time.time()

    # Set out dir/files for data and plots.
    outdir =  "results/p15_fits/full_plate/CompModelBC/"
    datafile = (outdir + "argv_{0}_b_guess_{1}.json").format(sys.argv[1],
                                                             b_guess)
    sbmlfile = (outdir + "sbml/argv_{0}_b_guess_{1}.xml").format(sys.argv[1],
                                                                 b_guess)
    plotfile = (outdir + "plots/argv_{0}_b_guess_{1}.pdf").format(sys.argv[1],
                                                                  b_guess)


    # Cannot serialize Plate and Model objects as json
    guess_kwargs = dict_to_json(guess_kwargs)
    json_guess_kwargs = {}
    for k, v in guess_kwargs.items():
        try:
            json.dumps(v)
        except TypeError:
            pass
        else:
            json_guess_kwargs[k] = v
    data = {
        'source_data': 'p15',
        'rows': full_plate.rows,
        'cols': full_plate.cols,
        'c_meas': full_plate.c_meas,
        'times': full_plate.times,
        'argv': int(sys.argv[1]),
        'guess_method_C_ratio_zero_kn': guess_var,
        'model': plate_model.name,
        'model_params': plate_model.params,
        'model_species': plate_model.species,
        'bounds': bounds,
        'init_guess': quick_guess,
        'comp_est': full_plate.est.x,
        'obj_fun': full_plate.est.fun,
        'fit_time': t1-t0,
        'guess_kwargs': json_guess_kwargs,
    }
    data = dict_to_json(data)

    with open(datafile, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

    # Need to correct. At the moment this returns the guess not the
    # est.
    sbml = full_plate.rr.getSBML()
    with open(sbmlfile, 'w') as f:
        f.write(sbml)

    # # No point to do this for a full plate.
    # plotter = Plotter(plate_model)
    # plot_title = "{0} fit of p15 (b_guess {1})".format(plate_model.name,
    #                                                    b_guess)
    # try:
    #     plotter.plot_est_rr(full_plate, full_plate.est.x, title=plot_title,
    #                         filename=plotfile)
    # except Exception as e:
    #     error_log = "Plotting: arg_v {0}, b_guess {1},\n".format(sys.argv[1],
    #                                                              b_guess)
    #     with open(error_file, 'a') as f:
    #         f.write(error_log)
    #     continue
