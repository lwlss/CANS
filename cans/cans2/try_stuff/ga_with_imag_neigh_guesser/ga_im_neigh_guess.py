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
from cans2.make_sbml import create_sbml


model = kwargs.PickleableCompModelBC()    # Pickleable for multiprocessing.
plotter = Plotter(model)

# Generate and save a random seed.
seed_file = "data/seeds.txt"
seed, random = genetic.get_seed_and_prng(seed_file)

# load plate data from json.
with open("data/sim_and_est_data_3x3.json", 'r') as f:
    data = dict_to_numpy(json.load(f))

true_plate = Plate(**kwargs._get_plate_kwargs(data))
true_plate.sim_amounts = data["sim_amounts"]
true_plate.sim_params = data["sim_params"]
true_plate.set_rr_model(model, data["sim_params"])
no_cultures = data["rows"]*data["cols"]
# # Check we have the correct parameters for the data.
# plotter.plot_est_rr(true_plate, data["sim_params"], sim=False)

gen_kwargs =  {
    "bounds": np.concatenate((data["bounds"][:model.b_index], [[0.0, 100.0]])),
}
args = {
    "gen_kwargs": gen_kwargs,
    "eval_kwargs": kwargs.make_eval_plate_lvl_im_neigh_grad_kwargs(data, model,
                                                                   [0.0, 100.0]),
}


# # Evolutionary strategy
# final_pop = genetic.es_mp_evolver(generator=genetic.gen_random_uniform,
#                                   evaluator=genetic.eval_plate_lvl_im_neigh_grad,
#                                   bounds=args["gen_kwargs"]["bounds"],
#                                   args=args,
#                                   random=random,
#                                   cpus=6,
#                                   pop_size=20,
#                                   max_evals=10*20)

print(gen_kwargs["bounds"])
# Differential Evolutionary Algorithm
final_pop = genetic.dea_mp_evolver(generator=genetic.gen_random_uniform,
                                   evaluator=genetic.eval_plate_lvl_im_neigh_grad,
                                   bounds=args["gen_kwargs"]["bounds"],
                                   args=args,
                                   random=random,
                                   cpus=7,
                                   pop_size=20,
                                   max_evals=40,
                                   num_selected=10,
                                   tournament_size=3,
                                   crossover_rate=1.0,
                                   mutation_rate=0.1,
                                   gaussian_mean=0,
                                   gaussian_stdev=1)    # Might this have to be different for each of the params unless we scale?

print(final_pop)
best = max(final_pop)    # Always max even if you are minimizing objective function.
est_plate_lvl = best.candidate[:model.b_index+1]

print("best", est_plate_lvl, best.fitness)
print("true", data["sim_params"])

# Concatenate est with true bs removing b_guess. Should really get the parameters back
# from the best eval
est_params = np.concatenate((est_plate_lvl[:-1], data["sim_params"][-no_cultures:]))

plotter.plot_est_rr(true_plate, est_params, sim=False,
                    title="Best Candidate Using Evolution Strategy")
