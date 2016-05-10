import numpy as np

from plate import Plate
from fitter import Fitter
from model import CompModel, IndeModel



comp_model = CompModel()
inde_model = IndeModel()

obs_times = np.linspace(0, 15, 16)

a_plate = Plate(2, 2)
a_plate.times = obs_times
a_plate.sim_params = comp_model.gen_params(a_plate, mean=1.0, var=1.0)
a_plate.sim_amounts = comp_model.solve(a_plate, a_plate.sim_params)
print(a_plate.sim_amounts)
print("")
#print([ data in a_plate.sim_amounts.flatten()]

# Now add these amounts to Cultures on the plate and fit independent
# model and save estimates.
cells = []
nuts = []

culture_data = []

for i in range(a_plate.no_cultures):
    cells.append(a_plate.sim_amounts[:, i*2])
    nuts.append(a_plate.sim_amounts[:, i*2+1])
    culture_data.append(a_plate.sim_amounts[:, i*no_species:(i+1)*no_species])
print(cells[0])
print(nuts[0])
print(culture_data[0])
