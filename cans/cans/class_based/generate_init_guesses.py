import numpy as np
import json


from plate import Plate
from model import CompModel
from plotter import Plotter
from cans_funcs import add_noise

rand_rs_dir = 'data/init_guess/16x24_rs_mean_5_var_3/'
comp_model = CompModel()
times = np.linspace(0, 5, 21)

custom_params = {
    'C_0': 0.0001,
    'N_0': 1.0,
    'kn': 0.1,
}

custom_params['kn'] = 0.2
# What N_0 and C_0?

# Generate 100 sets or random rs.
for i in range(100):
    plate1 = Plate(16, 24)
    plate1.times = times
    plate1.set_sim_data(comp_model, r_mean=5.0, r_var=3.0,
                        custom_params=custom_params)

    rand_rs = plate1.sim_params[3:]
    rand_rs = rand_rs.tolist()
    assert len(rand_rs) == plate1.no_cultures

    data = {
        'rand_rs': rand_rs,
        'mean': 5,
        'var': 3,
        'no_cultures': 384
    }
    with open(rand_rs_dir + '16x24_rs_{}.json'.format(i), 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

# comp_plotter = Plotter(comp_model)
# comp_plotter.plot_est(plate1, plate1.sim_params, sim=True)


# We want to check that we can succesfully fit a full comp plate given
# a certain amount of information that we will not necessarily have
# for real data.

# We are just saving the parameters here and will generate a different
# random comp simulation later to which we could also add noise. We
# should also try fitting with initial guesses using different mean
# and variance as we will not know what these will be in the real data
# until we have fitted.

# Save a meta file containing, dims,
# r_mean and r_var.


# Save 10 sets of random parameters to use as initial guesses.
#for i in range(10):


# plate1.comp_est = plate1.fit_model(comp_model, param_guess=None,
#                                    custom_options=None)

# comp_plotter.plot_est(plate1, plate1.comp_est.x, sim=True)

# print(plate1.comp_est.x)
