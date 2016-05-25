import numpy as np
#import matplotlib.pyplot as plt


from cans2.model import CompModel, GuessModel, PowerModel5
from cans2.guesser import Guesser
from cans2.plate import Plate
from cans2.plotter import Plotter
#from cans2.cans_funcs import gauss_list
from cans2.zoning import resim_zone


comp_model = CompModel()
power_model = PowerModel5()
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
power_param_guess = [resim_amount_guess["C_0"], resim_amount_guess["N_0"],
                     0.0, 0.0, 0.0, 0.0, 0.0, 30.0]
# We need to bound C_0 but not N_0 in this model. We could just use
# the guess C_0 as a fixed constraint.
power_bounds = [(0, None) for i in range(len(power_model.params))]
# Try fixed constraints on C_0 and N_0 first of all
power_bounds[0] = (resim_amount_guess["C_0"], resim_amount_guess["C_0"])
power_bounds[1] = (resim_amount_guess["N_0"], resim_amount_guess["N_0"])
power_bounds[2] = (-resim_amount_guess["N_0"]/10, resim_amount_guess["N_0"]/10)    # k1
power_bounds[3] = (-resim_amount_guess["N_0"]/10, resim_amount_guess["N_0"]/10)    # k2
power_bounds[4] = (-resim_amount_guess["N_0"]/10, resim_amount_guess["N_0"]/10)    # k3
#power_bounds[5] = (-resim_amount_guess["N_0"]/10, resim_amount_guess["N_0"]/10)    # k4
power_bounds[5] = (0.0, 0.0)
power_bounds[6] = (0.0, 0.0)
#power_bounds[6] = (-resim_amount_guess["N_0"]/100, resim_amount_guess["N_0"]/100)    # k5
power_bounds[7] = (0.0, None)    # r

# Guess using the power model
power_r_ests = []
power_k1_ests = []
power_k2_ests = []
power_ests = []
for culture in resim_zone.cultures:
    # Fit the independent model allowing N_0 to vary and compare to
    # true rs
    culture.est = culture.fit_model(power_model, param_guess=power_param_guess,
                                         bounds=power_bounds,
                                         minimizer_opts={'disp': False})
    power_r_ests.append(culture.est.x[-1])
    # power_k1_ests.append(culture.est.x[-4])
    # power_k2_ests.append(culture.est.x[-3])
    power_ests.append(culture.est.x)


print(resim_zone.sim_params[3:])
print(power_r_ests)
# print(power_k1_ests)
# print(power_k2_ests)
# comp_plotter.plot_est(resim_zone, resim_zone.sim_params)

comp_plotter.plot_culture_fits(resim_zone, power_model, sim=True,
                               title="Power series fits of individual cultures")
