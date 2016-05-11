import numpy as np


from plate import Plate
from model import CompModel, IndeModel
from plotter import Plotter

# Instantiate both model types
inde_model = IndeModel()
comp_model = CompModel()

# Define plate
plate1 = Plate(3, 3)
plate1.times = np.linspace(0, 5, 21)    # Set obs times

# Give the plate some data
kns = [{'kn': 0.00}]    # Could use a list of dicts to store several kns
plate1.set_sim_data(comp_model, r_mean=2.0, r_var=2.0, custom_params=kns[0])
print(plate1.sim_params)


# Make culture estimates then make full plate independent estimate.
culture_ests = plate1.est_from_cultures()
plate1.inde_est = plate1.fit_model(inde_model, culture_ests)


# Test plotting
inde_plotter = Plotter(inde_model)
inde_plotter.plot_estimates(plate1, plate1.inde_est.x, sim=True)
