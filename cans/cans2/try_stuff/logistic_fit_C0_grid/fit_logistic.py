import numpy as np
import sys


from cans2.parser import get_plate_data
from cans2.plate import Plate
from cans2.guesser import fit_log_eq
from cans2.model import IndeModel


C_0s_index = int(sys.argv[1])

all_C_0s = np.logspace(-6, -3, 1000)
C_0s = all_C_0s[C_0s_index:C_0s_index+20]


# read in plate 15 data and make a plate.
data_path = "../../../../data/p15/Output_Data/"
plate_data = get_plate_data(data_path)
plate = Plate(plate_data["rows"], plate_data["cols"],
                   data=plate_data)

b_guess = 10.0

def fit_log_eq(plate, C_0, b_guess):
    """Fit the logistic equivalent model for a fixed C_0."""
    # Use final amounts of cells as inital guesses of nutrients
    C_fs = plate.c_meas[-plate.no_cultures:]
    guesses = [[C_0] + [N_0_guess, b_guess] for N_0_guess in C_fs]
    # For logistic equivalent bound C_0 and allow N_0 and b to
    # vary freely. It would perhaps be better to fit C_0
    # collectively but this would be much slower. [C_0, N_0, b]
    all_bounds = [[(C_0, C_0), (0.0, C_f*4), (0.0, 500)] for C_f in C_fs]
    log_eq_mod = IndeModel()
    for guess, bounds, culture in zip(guesses, all_bounds, plate.cultures):
        culture.log_est = culture.fit_model(log_eq_mod, guess, bounds)

    obj_funs = []
    params = []
    for culture in plate.cultures:
        obj_funs.append(culture.log_est.fun)
        params.append(culture.log_est.x)

    return obj_funs, params


for C_0 in C_0s:
    param_guess = []
    # C_0, N_0, b
    culture_bounds = np.array([[C_0, C_0], [, ], [, ]])
    # May have to use CompModel with kn set to zero?
    fit_log_eq(plate, IndeModel(), b_guess
    pass
