import sys
from libsbml import *

import numpy as np
from cans2.plate import Plate
from cans2.model import CompModel


# Simulate a plate with data and parameters.
plate1 = Plate(2, 2)
plate1.times = np.linspace(0, 5, 11)
params = {
    "C_0": 1e-6,
    "N_0": 0.1,
    "kn": 1.5
}
plate1.set_sim_data(CompModel(), r_mean=40.0, r_var=15.0, custom_params=params)

# writeSBMLToFile(d, filename)
