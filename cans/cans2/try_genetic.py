import time
import json
import numpy as np


from cans2.cans_funcs import dict_to_numpy
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.genetic2 import evolver, mp_evolver, gen_random_uniform, evaluate_b_candidate, evaluate_b_candidates
from cans2.genetic_kwargs import PickleableCompModelBC, make_evaluate_b_candidate_kwargs, make_evaluate_b_candidates_kwargs, _get_plate_kwargs



# load plate data from json.
with open("temp_sim_and_est_data.json", 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))

# Just use evolutionary strategy to get bs and supply true C_0, N_0
# NE_0, and kn.
rows = data["rows"]
cols = data["cols"]
no_cultures = rows*cols
plate_lvl = data["sim_params"][:-no_cultures]


bounds = np.array([[0.0, 80.0] for i in range(no_cultures)])

model = PickleableCompModelBC()
args = {
    "gen_kwargs": {"bounds": bounds},
    "eval_kwargs": make_evaluate_b_candidates_kwargs(data, model, plate_lvl),
}

final_pop = evolver(gen_random_uniform, evaluate_b_candidates, bounds, args,
                    pop_size=500, max_evals=100000)

best = max(final_pop)
print(best)
est_params = np.concatenate((plate_lvl, best.candidate[:no_cultures]))
print(est_params)

true_plate = Plate(**_get_plate_kwargs(data))
true_plate.sim_amounts = data["sim_amounts"]
true_plate.sim_params = data["sim_params"]
true_plate.set_rr_model(model, data["sim_params"])

plotter = Plotter(model)
plotter.plot_est_rr(true_plate, est_params, sim=True,
                    title="Best Candidate Using Evolution Strategy")
