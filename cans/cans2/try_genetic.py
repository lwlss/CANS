import time
import json
import numpy as np


from cans2.cans_funcs import dict_to_numpy
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.genetic2 import evolver, custom_evolver, mp_evolver, gen_random_uniform, gen_random_uniform_log_C, eval_candidates, eval_b_candidate, eval_b_candidates
from cans2.genetic_kwargs import PickleableCompModelBC, make_eval_candidates_kwargs, make_eval_b_candidate_kwargs, make_eval_b_candidates_kwargs, _get_plate_kwargs

model = PickleableCompModelBC()
plotter = Plotter(model)

# load plate data from json.
with open("temp_sim_and_est_data.json", 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))

true_plate = Plate(**_get_plate_kwargs(data))
true_plate.sim_amounts = data["sim_amounts"]
true_plate.sim_params = data["sim_params"]
true_plate.set_rr_model(model, data["sim_params"])
no_cultures = data["rows"]*data["cols"]

# Check we have the correct parameters for the data.
# plotter.plot_est_rr(true_plate, data["sim_params"], sim=False)

### Just bs ###
# # Just use evolutionary strategy to get bs and supply true C_0, N_0
# plate_lvl = data["sim_params"][:-no_cultures]


# bounds = np.array([[0.0, 100.0] for i in range(no_cultures)])

# args = {
#     "gen_kwargs": {"bounds": bounds},
#     "eval_kwargs": make_evaluate_b_candidates_kwargs(data, model, plate_lvl),
# }
# # Standard genetic strategy.
# final_pop = evolver(gen_random_uniform, evaluate_b_candidates, bounds, args,
#                     pop_size=100, max_evals=100000)# , mut_rate=1.0)
# Custom strategy with tournement selection and crowding replacement.
# final_pop = custom_evolver(gen_random_uniform, evaluate_b_candidates,
#                            bounds, args, pop_size=20, num_selected=20,
#                            max_evals=10000, mut_rate=1.0)
# best = max(final_pop)
# est_params = np.concatenate((plate_lvl, best.candidate[:no_cultures]))

### All params ###
bounds = data["bounds"]
bounds[-no_cultures:] = np.array([0.0, 100.0])

args = {
    "gen_kwargs": {"bounds": bounds},
    "eval_kwargs": make_eval_candidates_kwargs(data, model),
}

# Can also try gen_random_uniform_log_C.
final_pop = custom_evolver(gen_random_uniform_log_C, eval_candidates,
                           bounds, args, pop_size=100, num_selected=100,
                           max_evals=100000, mut_rate=1.0)
best = max(final_pop)
est_params = best.candidate
print("best", est_params)
print("true", data["sim_params"])

plotter.plot_est_rr(true_plate, est_params, sim=False,
                    title="Best Candidate Using Evolution Strategy")
# plotter.plot_est_rr(true_plate, est_params, sim=True,
#                     title="Best Candidate Using Evolution Strategy")
