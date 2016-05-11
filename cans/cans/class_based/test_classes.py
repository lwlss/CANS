import numpy as np


from plate import Plate
from fitter import Fitter
from model import CompModel, IndeModel


# Instantiate both model types
inde_model = IndeModel()
comp_model = CompModel()

# Define plate
plate1 = Plate(2, 2)
plate1.times = np.linspace(0, 5, 21)    # Set obs times

# Give the plate some data
kns = [{'kn': 0.02}]    # Could use a list of dicts to store several kns
plate1.set_sim_data(comp_model, r_mean=1.0, r_var=1.0, custom_params=kns[0])


# Make culture estimates then make full plate independent estimate.
culture_ests = plate1.est_from_cultures()
plate1.inde_est = plate1.fit_model(inde_model, culture_ests)

# Add kn to inde_estimates then make a competition fit
init_guess0 = np.insert(plate1.inde_est.x, comp_model.no_species, 0.0)
init_guess = init_guess0
fun = np.inf
success = False

# By printing fun and parameter devs every 50 iters, we can see how
# small fun should be to give a certain accuracy. We would like kn to
# be accurate to 0.001 and rates to be accurate to 0.01. We need to
# set this up for full plate fits. This will depend on the amount of
# noise in the data. If there is more noise parameters will be more
# accurate for a larger value of fun. Perhaps we should first look at
# the case where there is no noise to find a minimum value for fun.

# ftol has replaced factr in scipy.optimize.minimize (not correct in the
# documentation) ftol = factr*epsmch. eps.mch can be found using
# eps = np.finfo(float).eps.
# very accurate minimum would be ftol = 10.0*eps.
while fun > 0.001 and not success:
    plate1.comp_est = plate1.fit_model(comp_model, init_guess, maxiter=50)
    init_guess = plate1.comp_est.x
    fun = plate1.comp_est.fun
    success = plate1.comp_est.success


print("sim_params/true")
print(plate1.sim_params)
print("Culture ests")
print(plate1.avg_culture_ests)
print("Plate inde ests")
print(plate1.inde_est.x)
print("init comp guess")
print(init_guess0)
print("Plate comp ests")
print(plate1.comp_est.x)
