import time
import numpy as np


from cans2.plate import Plate
from cans2.model import CompModelBC

model = CompModelBC()

plate = Plate(16, 24)
plate.times = np.linspace(0, 5, 11)
plate.set_sim_data(model)
t0 = time.time()
plate.set_rr_model(model, plate.sim_params)
t1 = time.time()
print(t1-t0)

t0 = time.time()
plate.rr_solve()
t1 = time.time()
print(t1-t0)
