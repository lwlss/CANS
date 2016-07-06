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





import pickle

class PickleableRoadRunner(roadrunner.RoadRunner, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.RoadRunner.__init__(self)

class PickleableRRModel(roadrunner.RoadRunner, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.RoadRunner.__init__(self)


class PickleableCVODEIntegrator(roadrunner.Integrator, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.Integrator.__init__(self)


class PickleableExecutableModel(roadrunner.ExecutableModel, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.ExecutableModel.__init__(self, *args)




pic_model = PickleableCompModelBC()
pickleable(pic_model)
sbml = create_sbml(Plate(**get_plate_kwargs(data)), pic_model, data["sim_params"])


# Unpickled RR
pic_plate = PickleablePlate(get_plate_kwargs(data))    # Must send as an arg not **kwargs.
pic_plate.set_rr_model(pic_model, data["sim_params"])


print(pic_plate.rr.isModelLoaded())
print(pic_plate.rr.model)
print(pic_plate.rr.getCompiler())


exec_model = roadrunner.ExecutableModel()
print("exec model", exec_model)

# exec_model = PickleableExecutableModel()

exec_model = PickleableExecutableModel()
print(exec_model)
assert False

sol1 = pic_plate.rr_solve()
# print(pic_plate.rr)
print("sol1", sol1)

# Pickled RR
pic_rr = PickleableRoadRunner(create_sbml(pic_plate, pic_model, data["sim_params"]))
print(pic_rr.isModelLoaded())
# pic_rr.setIntegrator("CVODE")
# pic_rr.setModel()

#pic_rr = pickle.loads(pickle.dumps(pic_rr))
print(pic_rr.getCompiler())
# print(pic_rr)
# pic_rr.setIntegrator(PickleableCVODEIntegrator())
# print(pic_rr)
pic_plate.rr = pic_rr
print(pic_plate.rr.model)

t0 = time.time()
pic_plate.rr.load(sbml)
t1 = time.time()
print("load", t1-t0)

print(pic_plate.rr.model)

sol2 = pic_plate.rr_solve()

# print(sol1, sol2)
assert False





# roadrunner.CVODEIntegrator()

#pickleable_rr = pickle.loads(pickle.dumps(pickleable_rr))

print(pickleable_rr)
assert False
# pickle.dumps(rr)
plate.rr = rr
sol = plate.rr_solve()
# print(sol)

dump = pickle.dumps(plate)
# print(dump)
pickleable(plate)
