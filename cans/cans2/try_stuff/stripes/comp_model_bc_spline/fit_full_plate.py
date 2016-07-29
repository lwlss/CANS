import numpy as np
import json
import sys
import time


from cans2.parser import get_plate_data2
from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.guesser import fit_imag_neigh, Guesser
from cans2.cans_funcs import dict_to_json
from cans2.make_sbml import create_sbml


barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False},
    {"barcode": "K000347_027_022", "ignore_empty": True},    # Filled stripes do not have correct gene names.
])
barcode = barcodes[int(sys.argv[2])]

plate_model = CompModelBC()

cell_ratios = np.logspace(-1, -7, num=10)
C_ratio = cell_ratios[int(sys.argv[1])]

# Read in real data and make a plate.
data_path = "../../../../../data/stripes/Stripes.txt"
full_plate = Plate(**get_plate_data2(data_path, **barcode))
# For the filled plate, the genes are not labelled properly. I could
# add the correct gene names here, but there is not reason to do so
# until we analyse the results. First column is "HIS3". Other columns
# are repeated in pairs.
barcode = barcode["barcode"]

# # Temporarily work with a zone while checking script runs.
# from cans2.zoning import get_plate_zone
# full_plate = get_plate_zone(full_plate, (5,5), 5, 5)    ###### ZONE ######

# Make a spline of c_meas with 15 time_points.
full_plate.make_spline(time_points=15)

# Plot spline
# from cans2.plotter import Plotter
# plotter = Plotter(plate_model)
# plotter.plot_spline(full_plate)

# Errors are captured to file and iteartion skipped.
error_file = "error_logs/" + barcode + "_CompModelBC_error_log.txt"
b_guesses = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 95, 100, 150]
for b_guess in b_guesses[int(sys.argv[3])::2]:
    # User defined/selected parameters pre guessing.
    guess_kwargs = {
        "plate": full_plate,
        "plate_model": plate_model,
        "C_ratio": C_ratio,    # Guess of init_cells/final_cells.
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
    # Parameter guesses for fitting.
    guess_kwargs.update(imag_neigh_only)

    try:
        t0 = time.time()
        quick_guess, quick_guesser = fit_imag_neigh(**guess_kwargs)
        t1 = time.time()
    except Exception as e:
        error_log = "imag guess: C_ratio index {0}, b_guess {1},\n".format(sys.argv[1],
                                                                            b_guess)
        with open(error_file, 'a') as f:
            f.write(error_log)
        continue


    # Removed kn setting zero here as did not provide the best fits for p15.
    full_plate.set_rr_model(plate_model, quick_guess, outfile="")

    # Make bounds for fitting.
    area_ratio = guess_kwargs["area_ratio"]
    plate_guesser = Guesser(full_plate, guess_kwargs["plate_model"],
                            area_ratio, guess_kwargs["C_ratio"])
    bounds = plate_guesser.get_bounds(quick_guess, C_doubt=1e3,
                                      N_doubt=2.0, kn_max=10.0)

    t0 = time.time()
    # Now fit the model to the plate and save the result and plot as
    # json and pdf.
    try:
        full_plate.est = full_plate.fit_spline(guess_kwargs["plate_model"],
                                               param_guess=quick_guess,
                                               bounds=bounds,
                                               minimizer_opts={"disp": False})
    except Exception as e:
        error_log = "Full est: C_ratio index {0}, b_guess {1},\n".format(sys.argv[1],
                                                                         b_guess)
        with open(error_file, 'a') as f:
            f.write(error_log)
        continue
    t1 = time.time()

    # Set out dir/files for data and plots.
    datafile = (barcode + "/results/C_ratio_i_{0}_b_guess_{1}.json").format(sys.argv[1],
                                                                            b_guess)
    sbmlfile = (barcode + "/sbml/C_ratio_i_{0}_b_guess_{1}.xml").format(sys.argv[1],
                                                                        b_guess)
    # plotfile = (barcode + "/plots/argv_{0}_b_guess_{1}.pdf").format(sys.argv[1],
    #                                                                    b_guess)

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
        'c_meas_spline': full_plate.c_spline,
        't_spline': full_plate.t_spline,
        'c_meas_obj_spline': full_plate.c_meas_obj_spline,
        'source_data': data_path,
        'barcode': barcode,
        'rows': full_plate.rows,
        'cols': full_plate.cols,
        'c_meas': full_plate.c_meas,
        'times': full_plate.times,
        'argv': int(sys.argv[1]),
        'guess_C_ratio': C_ratio,
        'model': plate_model.name,
        'model_params': plate_model.params,
        'model_species': plate_model.species,
        'bounds': bounds,
        'init_guess': quick_guess,
        'est_params': full_plate.est.x,
        'obj_fun': full_plate.est.fun,
        'fit_time': t1-t0,
        'guess_kwargs': json_guess_kwargs,
    }
    data = dict_to_json(data)

    with open(datafile, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

    create_sbml(full_plate, plate_model, full_plate.est.x, outfile=sbmlfile)

    # # No point to plot for a full plate. Slow and not producing good plots.

    # plot_title = "{0} fit of p15 (b_guess {1})".format(plate_model.name,
    #                                                    b_guess)
    # try:
    # plotter.plot_est_rr(full_plate, full_plate.est.x, title=plot_title)#,
                        # filename=plotfile)
    # except Exception as e:
    #     error_log = "Plotting: arg_v {0}, b_guess {1},\n".format(sys.argv[1],
    #                                                              b_guess)
    #     with open(error_file, 'a') as f:
    #         f.write(error_log)
    #     continue
