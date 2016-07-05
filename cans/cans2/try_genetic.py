import json
import numpy as np


from cans2.genetic2 import gen_imag_neigh_guesses, evaluate_with_grad_fit
from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.cans_funcs import dict_to_numpy, pickleable


# load plate data from json.
with open("temp_sim_and_est_data.json", 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))
data["empties"] = []
data["bounds"][4:] = np.array([0.0, 150])


# Just use evolutionary strategy to get bs and supply true C_0, N_0
# NE_0, and kn.
rows = data["rows"]
cols = data["cols"]
no_culture = rows*cols
plate_lvl = data["sim_params"][:-no_cultures]
bounds = bounds[:-no_cultures]


def gen_plate_kwargs(dct):
    """Create plate making kwargs from a dict.

    dct : A dictionary containing, possibly amongst other things, key
    value pairs required for instantiating a Plate object.

    The returned "plate_kwargs" of use in multiprocessing. If the
    Plate cannot be pickled, it must be created inside each process
    from some passed arguments.

    """
    try:
        data["empties"]
    except KeyError:
        data["empties"] = []
    plate_kwargs = {
        "rows": data["rows"],
        "cols": data["cols"],
        "data": {
            "times": data["times"],
            "c_meas": data["c_meas"],
            "empties": data["empties"],
        },
    }
    return plate_kwargs

evolve(gen_random_uniform, eval_fit
