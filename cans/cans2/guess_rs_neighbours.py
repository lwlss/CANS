"""Use a fast and slow growing neighbour model to guess growth
constants for inidividual cultures.

"""
import numpy as np


from cans2.model import CompModel, NeighModel
from cans2.guesser import Guesser
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.zoning import resim_zone


comp_model = CompModel()
neigh_model = NeighModel()
comp_guesser = Guesser(comp_model)
comp_plotter = Plotter(CompModel())


# Simulate a 16x24 plate with noise
full_plate = Plate(16, 24)
full_plate.times = np.linspace(0, 5, 11)
true_params = {'N_0': 0.15, 'kn': 1.0}
true_params['C_0'] = true_params['N_0']/10000
full_plate.set_sim_data(comp_model, r_mean=20.0, r_var=15.0,
                        custom_params=true_params)


# Guess rs for resimed 3x3 zone (i.e. a plate) with noise.
resim_zone = resim_zone(full_plate, comp_model, (5, 5), 3, 3, noise=True)
resim_amount_guess = comp_guesser.make_guess(resim_zone)

# No basis for an r_guess yet so just use 20.0 (may have to make
# random guesses). Guess k = 0.0
neigh_param_guess = [resim_amount_guess["C_0"], resim_amount_guess["N_0"],
                     1.0, 1.0, 0.0, 20.0, 40.0]
# We need to bound C_0 but not N_0 in this model. We could just use
# the guess C_0 as a fixed constraint.
neigh_bounds = [(0, None) for i in range(len(neigh_model.params))]
# Try fixed constraints on C_0 and N_0 first of all
neigh_bounds[0] = (resim_amount_guess["C_0"], resim_amount_guess["C_0"])
neigh_bounds[1] = (resim_amount_guess["N_0"], resim_amount_guess["N_0"])
neigh_bounds[4] = (0.0, 0.0)    # r-
neigh_bounds[5] = (40.0, 40.0)    # r+

# Guess using the neigh model
neigh_r_ests = []
neigh_kn_ests = []
neigh_ests = []
for culture in resim_zone.cultures:
    # Fit the independent model allowing N_0 to vary and compare to
    # true rs
    culture.est = culture.fit_model(neigh_model, param_guess=neigh_param_guess,
                                    bounds=neigh_bounds,
                                    minimizer_opts={'disp': False})
    neigh_r_ests.append(culture.est.x[-1])
    neigh_kn_ests.append(culture.est.x[2:4])
    neigh_ests.append(culture.est.x)


print(resim_zone.sim_params[3:])
print(neigh_r_ests)
print(neigh_kn_ests)
# comp_plotter.plot_est(resim_zone, resim_zone.sim_params)

comp_plotter.plot_culture_fits(resim_zone, neigh_model, sim=True,
                               title="Neighbour model fits of individual cultures")
