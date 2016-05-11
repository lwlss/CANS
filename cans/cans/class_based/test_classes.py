import numpy as np

from plate import Plate
from fitter import Fitter
from model import CompModel, IndeModel

inde_model = IndeModel()
comp_model = CompModel()

plate1 = Plate(2, 2)
plate1.times = np.linspace(0, 15, 21)    # Set obs times

# Simulate some params and solve for amounts for the plate.
plate1.sim_params = comp_model.gen_params(plate1, mean=1.0, var=1.0)
plate1.sim_amounts = comp_model.solve(plate1, plate1.sim_params)
plate1.c_meas = plate1.sim_amounts.flatten()[::comp_model.no_species]
plate1.set_cultures()    # Set culture.c_meas and times

est = plate1.est_from_cultures()

# Now add these amounts to Cultures on the plate and fit independent
# model and return estimates
plate1.inde_est = plate1.fit_model(inde_model,
                                   plate1.est_from_cultures())

# Now use inde est for comp fit.

print("sim_params/true")
print(plate1.sim_params)
print("Culture ests")
print(est)
print("Plate ests")
print(plate1.inde_est.x)
