import numpy as np


from plate import Plate
from fitter import Fitter
from model import CompModel, IndeModel


# Instantiate both model types
inde_model = IndeModel()
comp_model = CompModel()

# Define plate
plate1 = Plate(3, 3)
plate1.times = np.linspace(0, 15, 21)    # Set obs times

# Give the plate some data
kns = [{'kn': 0.01}]    # Could use a list of dicts to store several kns
plate1.set_sim_data(comp_model, r_mean=1.0, r_var=1.0, custom_params=kns[0])



# Make culture estimates then make full plate independent estimate.
culture_ests = plate1.est_from_cultures()
plate1.inde_est = plate1.fit_model(inde_model, culture_ests)

# Add kn to inde_estimates then make a competition fit
init_guess = np.insert(plate1.inde_est.x, comp_model.r_index, 0.0)
plate1.comp_est = plate1.fit_model(comp_model, init_guess)


print(init_guess)
print("sim_params/true")
print(plate1.sim_params)
print("Culture ests")
print(plate._get_avg_culture_ests())
print("Plate inde ests")
print(plate1.inde_est.x)
print("Plate comp ests")
print(plate1.comp_est.x)
