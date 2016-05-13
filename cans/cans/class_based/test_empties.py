import numpy as np


from plate import Plate
from model import CompModel, IndeModel
from plotter import Plotter

# Instantiate both model types
inde_model = IndeModel()
comp_model = CompModel()

times = np.linspace(0, 5, 21)
kns = [{'kn': 0.1}]    # Could use a list of dicts to store several
                        # sets of custom params.

# Define plate
# plate1 = Plate(2, 2)
# plate1.times = times    # Set obs times
# plate1.set_sim_data(comp_model, r_mean=1.0, r_var=1.0, custom_params=kns[0])

# Want a plate with an empty site. May have to give empties in
# instantiation.
emp_plate = Plate(3, 3)
emp_plate.empties = (0, 2, 5)
emp_plate.times = times
emp_plate.set_sim_data(comp_model, r_mean=2.0, r_var=2.0, custom_params=kns[0])

culture_ests = emp_plate.est_from_cultures()
emp_plate.inde_est = emp_plate.fit_model(inde_model, culture_ests)
# Add kn=0.0 to inde_est to form an initial guess. init_guess0 is used
# so that if we loop the comp_fitter and update the init_guess every
# time we still can print it at the bottom.
init_guess0 = np.insert(emp_plate.inde_est.x, comp_model.no_species, 0.0)
emp_plate.comp_est = emp_plate.fit_model(comp_model, init_guess0)

inde_plotter = Plotter(inde_model)
inde_plotter.plot_estimates(emp_plate, emp_plate.inde_est.x, sim=True)

comp_plotter = Plotter(comp_model)    # No different to inde_plotter in this case.
comp_plotter.plot_estimates(emp_plate, emp_plate.comp_est.x, sim=True)
comp_plotter.plot_estimates(emp_plate, emp_plate.comp_est.x, sim=False)



print(emp_plate.sim_params)
print(culture_ests)
print(emp_plate.inde_est)
print(emp_plate.comp_est)
print(emp_plate.sim_amounts)

# # Make culture estimates then make full plate independent estimate.
# culture_ests = plate1.est_from_cultures()
# plate1.inde_est = plate1.fit_model(inde_model, culture_ests)

# # Add kn to inde_estimates then make a competition fit
# init_guess0 = np.insert(plate1.inde_est.x, comp_model.no_species, 0.0)
# init_guess = init_guess0
# fun = np.inf
# success = False
