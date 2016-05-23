import numpy as np
from cans2.model import CompModel, GuessModel
from cans2.guesser import Guesser
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.cans_funcs import gauss_list
import matplotlib.pyplot as plt

comp_model = CompModel()
guess_model = GuessModel()
comp_guesser = Guesser(comp_model)

# generate a 2x2 plate

plate = Plate(16, 24)
plate.times = np.linspace(0, 5, 11)
true_params = {'N_0': 0.1, 'kn': 0.2}
true_params['C_0'] = true_params['N_0']/10000
plate.set_sim_data(comp_model, r_mean=50.0, r_var=25.0, custom_params=true_params)

guess = comp_guesser.make_guess(plate)

param_guess = [guess['C_0'], guess['N_0'], 0.0, 5.0]
print(param_guess)

for culture in plate.cultures:
    print(culture.no_cultures)
    culture.guess_est = culture.fit_model(guess_model, param_guess=param_guess,
                                          custom_options={'disp': False})


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
