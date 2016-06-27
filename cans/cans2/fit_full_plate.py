import numpy as np
import json
import sys
import itertools


from cans2.parser import get_plate_data
from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC
from cans2.guesser import fit_imag_neigh, fit_log_eq, Guesser

# Temporarily work with a zone while checking script runs.
from cans2.zoning import get_plate_zone


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

zone = get_plate_zone(full_plate, (5,5), 3, 3)

plate_model = CompModelBC()    # Should pass another argument for CompModel()

# User defined/selected parameters pre guessing.
b_guess = 45.0    # Approximate expected value of b params.
fit_kwargs = {
    "plate": zone,
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
    fit_kwargs.update(imag_neigh_only)
    quick_guess, quick_guesser = fit_imag_neigh(**fit_kwargs)
elif guess_var[0] == "log_eq":
    fit_kwargs.update(log_eq_only)
    quick_guess, quick_guesser = fit_log_eq(**fit_kwargs)
if guess_var[2]:
    quick_guess[fit_kwargs["plate_model"].params.index("kn")] = 0.0
zone.set_rr_model(plate_model, quick_guess, outfile="")
print("Guesses made")


# Make bounds for fitting.
if guess_var[0] == "imag_neigh":
    area_ratio = fit_kwargs["area_ratio"]
elif guess_var[0] == "log_eq":
    area_ratio = 1.0
plate_guesser = Guesser(zone, fit_kwargs["plate_model"],
                        area_ratio, fit_kwargs["C_ratio"])
bounds = plate_guesser.get_bounds(quick_guess, C_doubt=1e3,
                                  N_doubt=2.0, kn_max=10.0)    # Could also try kn_max=None.

# Now fit the model to the plate and save the result and plot as json and pdf.
est = zone.fit_model(fit_kwargs["plate_model"], param_guess=quick_guess,
                     bounds=bounds, rr=True, sel=False,
                     minimizer_opts={"disp": True})
print(est.x)

# Set out dir/files for data and plots.
outdir =  "results/p15_fits/full_plate/"
datafile = (outdir + "full_plate_method_{0}.json").format(method_index)
plotfile = (outdir + "/plots/full_p15_fit_method_{0}.pdf").format(method_index)
