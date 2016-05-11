import numpy as np

from plate import Plate
from fitter import Fitter
from model import CompModel, IndeModel

inde_model = IndeModel()
comp_model = CompModel()

plate1 = Plate(3, 3)
plate1.times = np.linspace(0, 15, 21)    # Set obs times

custom_params = {'kn': 0.001}    # Using a list we could store kn for several plates
plate1.set_sim_data(comp_model, custom_params=custom_params)

culture_ests = plate1.est_from_cultures()
plate1.inde_est = plate1.fit_model(inde_model, plate1.est_from_cultures())

# Fit comp model using full plate inde estimate. Need to add a kn
inde_plate_est = plate1.inde_est.x
init_guess = np.insert(inde_plate_est, 2, 0.0)    # issue with inserting. How to make general?
print(init_guess)
plate1.comp_est = plate1.fit_model(comp_model, init_guess)


print("sim_params/true")
print(plate1.sim_params)
print("Culture ests")
print(culture_ests)
print("Plate inde ests")
print(plate1.inde_est.x)
print("Plate comp ests")
print(plate1.comp_est.x)
