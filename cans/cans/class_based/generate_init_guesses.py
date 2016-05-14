import numpy as np


from plate import Plate
from model import CompModel
from plotter import Plotter
from cans_funcs import add_noise


comp_model = CompModel()

plate1 = Plate(5, 5)

# What times?
times = np.linspace(0, 5, 21)
plate1.times = times

# Could also do a set with added random noise
# What mean and var for rs

custom_params = {
    'C_0': 0.0001,
    'N_0': 1.0,
    'kn': 0.1,
}
# What N_0 and C_0?
plate1.set_sim_data(comp_model, r_mean=5.0, r_var=3.0,
                    custom_params=custom_params)

print(plate1.sim_params)yes

comp_plotter = Plotter(comp_model)
comp_plotter.plot_est(plate1, plate1.sim_params, sim=True)


plate1.comp_est = plate1.fit_model(comp_model, param_guess=None,
                                   custom_options=None)

comp_plotter.plot_est(plate1, plate1.comp_est.x, sim=True)

print(plate1.comp_est.x)
