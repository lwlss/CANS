import json
import numpy as np


import cans2.genetic2 as genetic
from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.cans_funcs import dict_to_numpy, pickleable


# load plate data from json.
with open("temp_sim_and_est_data.json", 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))
data["bounds"][4:] = np.array([0.0, 150])

# Just use evolutionary strategy to get bs and supply true C_0, N_0
# NE_0, and kn.
rows = data["rows"]
cols = data["cols"]
no_cultures = rows*cols
plate_lvl = data["sim_params"][:-no_cultures]
# bounds = bounds[:-no_cultures]

plate_kwargs = genetic.get_plate_kwargs(data)
print(plate_kwargs)

#evolve(gen_random_uniform, eval_fit)
