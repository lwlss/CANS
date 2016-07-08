import time
import json
import numpy as np
import inspyred

import cans2.genetic2 as genetic
import cans2.genetic_kwargs as kwargs


from cans2.cans_funcs import dict_to_numpy
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter


model = kwargs.PickleableCompModelBC()    # Pickleable for multiprocessing.
plotter = Plotter(model)

# Generate and save a random seed.
seed_file = "data/seeds.txt"
seed, random = genetic.get_seed_and_prng(seed_file)

# load plate data from json.
with open("data/sim_and_est_data_3x3.json", 'r') as f:
    # data = dict_to_numpy(json.load(f))
    data = dict_to_numpy(json.load(f))

true_plate = Plate(**kwargs._get_plate_kwargs(data))
true_plate.sim_amounts = data["sim_amounts"]
true_plate.sim_params = data["sim_params"]
true_plate.set_rr_model(model, data["sim_params"])
no_cultures = data["rows"]*data["cols"]

# Check we have the correct parameters for the data.
# plotter.plot_est_rr(true_plate, data["sim_params"], sim=False)

# Prepare args.
b_bounds = np.array([np.array([0.0, 100]) for i in range(no_cultures)])
c_evolver_kwargs = {
    "generator": genetic.gen_random_uniform,
    "evaluator": genetic.eval_b_candidates,
    "observer": [],    # Internal observer.
    # "observer": [inspyred.ec.observers.stats_observer,
    #              inspyred.ec.observers.best_observer],
    "bounds": b_bounds,
    # "args": None,    # To be set inside plate_level eval
    "random": random,
    "pop_size": 20,
    "num_selected": 20,
    "max_evals": 10000,
    "mut_rate": 1.0,
    "crowd_dist": 10,    # Must be integer.
    }
c_evolver = kwargs.package_evolver(genetic.custom_evolver, **c_evolver_kwargs)
plate_lvl_bounds = data["bounds"][:model.b_index]
args = {
    "gen_kwargs": {"bounds": plate_lvl_bounds},
    "eval_kwargs": kwargs.make_eval_plate_lvl_kwargs(data, model, c_evolver),
    }


# Now call plate lvl parallel evolver.
final_pop = genetic.custom_mp_evolver(generator=genetic.gen_random_uniform_log_C,
                                      evaluator=genetic.eval_plate_lvl,
                                      bounds=plate_lvl_bounds,
                                      args=args,
                                      random=random,
                                      cpus=4,
                                      pop_size=20,
                                      num_selected=20,
                                      max_evals=100,
                                      mut_rate=1.0,
                                      crowd_dist=10)    # Must be integer.

print(final_pop)

best = min(final_pop)
est_plate_lvl = best.candidate[:model.b_index]

print("best", est_plate_lvl)
print("true", data["sim_params"])

# Concatenate est with true. Should really get the parameters back
# from the best eval
est_params = np.concatenate((est_plate_lvl, data["sim_params"][-no_cultures:]))

plotter.plot_est_rr(true_plate, est_params, sim=False,
                    title="Best Candidate Using Evolution Strategy")


best = max(final_pop)
est_plate_lvl = best.candidate[:model.b_index]

print("best", est_plate_lvl)
print("true", data["sim_params"])

# Concatenate est with true. Should really get the parameters back
# from the best eval
est_params = np.concatenate((est_plate_lvl, data["sim_params"][-no_cultures:]))

plotter.plot_est_rr(true_plate, est_params, sim=False,
                    title="Best Candidate Using Evolution Strategy")
