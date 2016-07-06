import time
import numpy as np
import roadrunner
import pickle


from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC
from cans2.make_sbml import create_sbml
from cans2.cans_funcs import pickleable
from cans2.plotter import Plotter


model = CompModelBC()

plate = Plate(16, 24)
plate.times = np.linspace(0, 5, 11)
custom_params = {
    "C_0": 1e-5,
    "N_0": 0.1,
    "NE_0": 0.13,
    "kn": 2.4,
    }
plate.set_sim_data(model, b_mean=50.0, b_var=35.0, custom_params=custom_params)
t0 = time.time()
plate.set_rr_model(model, plate.sim_params)
t1 = time.time()
print(t1-t0)


print(type(plate.sim_params))
# Must give plate the data_shape attribute if not aalling ser_rr_model

t0 = time.time()
plate.rr_solve()
t1 = time.time()
print("rr_solve", t1-t0)


comp_model = CompModel()
plate.comp_model_params = np.delete(plate.sim_params, 2)
t0 = time.time()
comp_model.solve(plate, plate.comp_model_params, plate.times)
t1 = time.time()
print("Odeint solve", t1-t0)


t0 = time.time()
sbml = create_sbml(plate, model, plate.sim_params)
t1 = time.time()
print(t1-t0)


t0 = time.time()
rr = roadrunner.RoadRunner()
t1 = time.time()
print("Instantiate RR", t1-t0)

# print(dir(rr))


t0 = time.time()
rr.load(sbml)
t1 = time.time()
print("Load SBML", t1-t0)

rr_model = rr.model
print(rr_model.__dict__)
pickleable(rr_model)
rr_model = pickle.loads(pickle.dumps(rr_model))
print(rr_model)
