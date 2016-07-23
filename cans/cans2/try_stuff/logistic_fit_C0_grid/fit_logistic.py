import numpy as np
import sys


from cans2.parser import get_plate_data
from cans2.plate import Plate
from cans2.guesser import fit_log_eq


C_0s_index = int(sys.argv[1])

all_C_0s = np.logspace(-6, -3, 1000)
C_0s = all_C_0s[C_0s_index:C_0s_index+20]


# read in plate 15 data and make a plate.
data_path = "../../../../data/p15/Output_Data/"
plate_data = get_plate_data(data_path)
plate = Plate(plate_data["rows"], plate_data["cols"],
                   data=plate_data)


for C_0 in C_0s:

    #fit_log_eq(
    pass
