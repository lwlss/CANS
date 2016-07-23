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

def quick_fit_log_eq(self, param_guess, bounds):
    """Guess b by fitting the logistic equivalent model.

    Returns guesses for all parameters in self.model for a
    self.model of CompModel or CompModelBC.

    Fits to individual cultures. For speed, there is no collective
    fitting of plate level parameters, e.g. initial
    amounts. Instead, an average can be taken after the individual
    fits. Individual b parameters result from fitting. Guesses for
    N_0 are infered from average final measurements and not
    updated after fitting. C_0 is guessed using C_ratio (see
    make_first_guess) and then fixed for fitting.

    b_guess : guess for b parameter. The same for all cultures.

    This N_0_guess is not used in logistic equivalent fits but
    is returned in the new_guess; logistic estimated N_0s are not
    realistic for the competition model.

    """

    # Use final amounts of cells as inital guesses of nutrients
    # because logistic equivalent growth is governed by N + C ->
    # 2C, there is no diffusion, and C_0 is assumed to be
    # relatively small.
    C_fs = self.plate.c_meas[-self.plate.no_cultures:]
    log_eq_N_0_guesses = C_fs
    log_eq_guesses = [C_0_guess + [N_0, b_guess] for N_0 in log_eq_N_0_guesses]
    # For logistic equivalent bound C_0 and allow N_0 and b to
    # vary freely. It would perhaps be better to fit C_0
    # collectively but this would be much slower. [C_0, N_0, b]
    log_eq_bounds = [[(C_0, C_0, (0.0, C_f*4), (0.0, 500)] for C_f in C_fs]
    log_eq_mod = IndeModel()
    for guess, bounds, culture in zip(log_eq_guesses, self.plate.cultures):
        culture.log_est = culture.fit_model(log_eq_mod, guess, bounds)

    for culture in plate.cultures:


for C_0 in C_0s:
    param_guess = []
    # C_0, N_0, b
    culture_bounds = np.array([[C_0, C_0], [, ], [, ]])
    # May have to use CompModel with kn set to zero?
    fit_log_eq(plate, IndeModel(), b_guess
    pass
