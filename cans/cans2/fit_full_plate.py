import numpy as np
import json
import sys
import itertools

from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC
from cans2.guesser import fit_imag_neigh, fit_log_eq

# Process script args
method_index = sys.argv[1]
# In total 5x2x2 = 20 sets of args.
cell_ratios = np.logspace(-4, -6, num=5)
fit_type = ["imag_neigh", "log_eq"]
zero_kn = [True, False]
guess_vars = list(itertools.product(fit_type, cell_ratios, zero_kn)))
guess_var = guess_var[method_index]

# Choose a model to use for fitting
model = CompModelBC()

# User defined parameters pre guessing.
b_guess = 45.0    # Approximate expected value of b params.
quick_fit_kwargs = {
    "plate": plate,
    "plate_model": model,
    "C_ratio": guess_var[1],    # Guess of init_cells/final_cells.
    "kn_start": 0.0,
    "kn_stop": 2.0,
    "kn_num": 21,
    # Imaginary neighbour model only.
    "area_ratio": 1.5        # Guess of edge_area/internal_area.
    # Not including amounts which are guesses from final cell amounts
    # and the C_ratio argument. ['kn1', 'kn2', 'b-', 'b+', 'b'] The
    # final parameter is the guess of the CompModel parameter b. Other
    # parameters are uniquie to the imaginary neighbour model.
    "imag_neigh_params": np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess]),
    "no_neighs": None,    # Can specify or allow it to be calculated np.ceil(C_f/N_0)
    # Logistic equivalent model only.
    "b_guess": b_guess,
}


# Get parameter guesses for fitting.
if guess_var[0] == "imag_neigh":
    quick_guess, quick_guesser = fit_imag_neigh(**quick_fit_kwargs)
elif guess_var[0] == "log_eq":
    quick_guess, quick_guesser = fit_log_eq(**quick_fit_kwargs)

if guess_var[2]:
    quick_guess[model.params.index("kn")] = 0.0


# Now fit the model to the plate and save the result and plot as json and png.
