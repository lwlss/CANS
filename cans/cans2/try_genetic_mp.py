import json
import numpy as np


from cans2.genetic2 import mp_evolver, gen_imag_neigh_guesses, evaluate_with_grad_fit
from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.cans_funcs import dict_to_numpy, pickleable


# load plate data from json.
with open("temp_sim_and_est_data.json", 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))
data["empties"] = []
data["bounds"][4:] = np.array([0.0, 150])

# Create plate making kwargs.
plate_kwargs = {
    "rows": data["rows"],
    "cols": data["cols"],
    "data": {
        "times": data["times"],
        "c_meas": data["c_meas"],
        "empties": data["empties"],
        },
}

model = CompModelBC()
imag_neigh_kwargs = {
    "plate": Plate(**plate_kwargs),    # Do not set rr or will not pickle.
    "plate_model": model.name,    # Cannot pickle the actual model
    "C_ratio": 1e-4,    # Guess of init_cells/final_cells.
    "kn_start": 0.0,
    "kn_stop": 2.0,
    "kn_num": 21,
    "area_ratio": np.nan,
    "imag_neigh_params": np.array([1.0, 1.0, 0.0, np.nan, np.nan]),
    "no_neighs": None,    # If None calculated as np.ceil(C_f_max/N_0_guess).
}

C_doubt = 1e3
gen_kwargs = {
    "area_range": np.array([1.0, 2.0]),
    "C_range": np.array([imag_neigh_kwargs["C_ratio"]/C_doubt,
                         imag_neigh_kwargs["C_ratio"]*C_doubt]),
    "b_range": np.array([0.0, 150.0]),
    "imag_neigh_kwargs": imag_neigh_kwargs,
}

eval_kwargs = {
    "plate_kwargs": plate_kwargs,
    "model": model.name,    # Cannot pickle the actual model.
    "bounds": data["bounds"],
}

args = {
    "gen_kwargs": gen_kwargs,
    "eval_kwargs": eval_kwargs,
}

final_pop = mp_evolver(gen_imag_neigh_guesses, evaluate_with_grad_fit,
                       data["bounds"], args, cpus=4, pop_size=4, max_evals=100,
                       mut_rate=0.25)
print(max(final_pop))