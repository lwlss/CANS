import numpy as np
import matplotlib.pyplot as plt


from cans2.model import CompModel, GuessModel
from cans2.guesser import Guesser
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.cans_funcs import gauss_list
from cans2.zoning import get_plate_zone, resim_zone


comp_model = CompModel()
guess_model = GuessModel()
comp_guesser = Guesser(comp_model)
comp_plotter = Plotter(CompModel())

# Simulate a 16x24 plate with noise
plate1 = Plate(16, 24)
plate1.times = np.linspace(0, 5, 11)
true_params = {'N_0': 0.1, 'kn': 0.5}
true_params['C_0'] = true_params['N_0']/10000
plate1.set_sim_data(comp_model, r_mean=30.0, r_var=15.0,
                    custom_params=true_params)

# Resimulate a 5x5 zone with the same parameters and check that we can
# fit it. Also compare how it looks to the true zone A: Noticable
# differences at the edges.
test_zone = resim_zone(plate1, comp_model, (5, 5), 3, 3, noise=False)
test_guess = comp_guesser.make_guess(test_zone)
test_bounds = comp_guesser.get_bounds(test_zone, test_guess)
#test_bounds[2] = (0.5, 0.5)
r_guess = [30.0 for i in range(test_zone.no_cultures)]
test_param_guess = [test_guess["C_0"], test_guess["N_0"], 0.5] + r_guess
test_zone.test_est = test_zone.fit_model(comp_model,
                                         param_guess=test_param_guess,
                                         bounds=test_bounds)
print("true")
print(test_zone.sim_params)
print("est")
print(test_zone.test_est.x)
print("guess")
print(test_guess)
print("bounds")
print(test_bounds)
comp_plotter.plot_est(test_zone, test_zone.test_est.x,
                      title="Fit of resimulated zone.")

assert False


# Extract c_meas for a zone on the full plate simulation
zone1 = get_plate_zone(plate1, (5, 5), 5, 5)


# Guess parameters for the full plate
full_guess = comp_guesser.make_guess(plate1)
# Alternatively guess parameters for the culture.
zone_guess = comp_guesser.make_guess(zone1)

# Set bounds from full_guess and zone_guess
bounds_full = comp_guesser.get_bounds(zone1, full_guess)
bounds_zone = comp_guesser.get_bounds(zone1, zone_guess)

# Need to automate this once we have methods for guessing kn and r.
r_guess = [50.0 for i in range(zone1.no_cultures)]
full_guess = [full_guess["C_0"], full_guess["N_0"], 0.4] + r_guess
zone_guess = [zone_guess["C_0"], zone_guess["N_0"], 0.4] + r_guess

# try fitting with both bounds and guesses.
zone1.full_guess_bounds_est = zone1.fit_model(comp_model,
                                              param_guess=full_guess,
                                              bounds=bounds_full)

print("true")
print(true_params)
print("full_guess")
print(full_guess)
print("est")
print(zone1.full_guess_bounds_est.x)
comp_plotter.plot_est(zone1, zone1.full_guess_bounds_est.x,
                      title="full_guess; full_guess derived bounds")


# check that we can fit a normal 5x5 plate with these params

# guess rs
# guess kn

assert False

param_guess = [guess['C_0'], guess['N_0'], 0.0, 5.0]
print(param_guess)

for culture in plate.cultures:
    print(culture.no_cultures)
    culture.guess_est = culture.fit_model(guess_model, param_guess=param_guess,
                                          minimizer_opts={'disp': False})


# Find mean and variance. Or fit the comp model with these params to
# find kn.
rs = [culture.guess_est.x[-1] for culture in plate.cultures]
rs.sort()
print(rs)
rs_mean = np.mean(rs[:-5])    # you get some outliers
rs_var = np.var(rs[:-10])
print(rs_mean, np.sqrt(rs_var))

plt.hist(rs)

# why are the outliers so high? Is k at the bounds?
guesses = [culture.guess_est.x[-2:] for culture in plate.cultures]
guesses.sort(key = lambda x: x[-1])
print(np.array(guesses))

# So try fixing N_0 and C_0
guess_plotter = Plotter(guess_model)
guess_plotter.plot_est(plate.cultures[0], plate.cultures[0].guess_est.x)
