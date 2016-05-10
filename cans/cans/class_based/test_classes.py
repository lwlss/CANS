import numpy as np

from plate import Plate
from fitter import Fitter
from model import CompModel, IndeModel


comp_model = CompModel()
inde_model = IndeModel()

obs_times = np.linspace(0, 15, 21)
rows = 2
cols = 2

a_plate = Plate(rows, cols)
a_plate.times = obs_times
# Simulate some amounts for the plate
a_plate.sim_params = comp_model.gen_params(a_plate, mean=1.0, var=1.0)
a_plate.sim_amounts = comp_model.solve(a_plate, a_plate.sim_params)
# Now add these amounts to Cultures on the plate and fit independent
# model and save estimates.
a_plate.add_cultures_sim_data()
print(a_plate.sim_amounts)
print(a_plate.cultures[0].c_meas)

# Create a Fitter instance which will fit the independent model.
inde_fitter = Fitter(inde_model)

for culture in a_plate.cultures:
    culture.inde_est = inde_fitter.fit_model(culture)


# No take average of cells where cells is not the initital guess.
# Take average of nutrients where nutrients is not zero.
# Take estimated r values as start for whole plate fitting.

#init_guess =

inde_ests = [culture.inde_est for culture in a_plate.cultures]
for est in inde_ests:
    print(est.x)
    print("")

print(a_plate.sim_params)
