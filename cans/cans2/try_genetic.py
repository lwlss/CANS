import json
import numpy as np


from cans2.genetic2 import get_plate_kwargs, mp_evolver, gen_random_uniform, evaluate_b_candidate
from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.cans_funcs import dict_to_numpy, pickleable
from cans2.fitter import Fitter



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

bounds = data["bounds"][-no_cultures:]

# model = CompModelBC()
gen_kwargs = {
    "bounds": bounds,
}
eval_kwargs = {
    "plate_kwargs": get_plate_kwargs(data),
    "plate_lvl": data["sim_params"][:-no_cultures],
    "fitter": Fitter(),
    "model": CompModelBC().name,
    "plate": Plate(**get_plate_kwargs(data)),
#    "model": CompModelBC(),
}

args = {
    "gen_kwargs": gen_kwargs,
    "eval_kwargs": eval_kwargs,
}
pickleable(args)

# final_pop = mp_evolver(gen_random_uniform, evaluate_b_candidate, bounds, args,
#                        cpus=4, pop_size=100, max_evals=1000, mut_rate=0.25)


class PickleableSWIG(object):
    # http://stackoverflow.com/a/9325185
    def __setstate__(self, state):
        print(state)
        self.__init__(*state['args'])

    def __getstate__(self):
        return {'args': self.args}


class PickleableCompModelBC(CompModelBC, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        CompModelBC.__init__(self)


class PickleablePlate(Plate, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        Plate.__init__(self, **self.args[0])


pickleable_model = PickleableCompModelBC()
pickleable(pickleable_model)

plate = PickleablePlate(get_plate_kwargs(data))    # Must send as an arg not **kwargs.
plate.set_rr_model(pickleable_model, data["sim_params"])

import pickle
import roadrunner
class PickleableRoadRunner(roadrunner.RoadRunner,  PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.RoadRunner.__init__(self)

class PickleableRRModel(roadrunner.RoadRunner,  PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.RoadRunner.__init__(self)

rr = plate.rr
print(rr)
pickleable_rr = PickleableRoadRunner()   # Give it some sbml and see if the integrator is not NUll
rr = pickle.loads(pickle.dumps(pickleable_rr))
print(rr)
# pickle.dumps(rr)
plate.rr = rr
sol = plate.rr_solve()
print(sol)

dump = pickle.dumps(plate)
# print(dump)
pickleable(plate)
