import numpy as np
from cans2.model import CompModel, GuessModel
from cans2.guesser import Guesser
from cans2.plate import Plate


comp_model = CompModel()
guess_model = GuessModel()
comp_guesser = Guesser(comp_model)

# generate a 2x2 plate

plate = Plate(2, 2)
plate.times = np.linspace(0, 5, 11)
true_params = {'N_0': 0.1, 'kn': 0.2}
true_params['C_0'] = true_params['N_0']/10000
plate.set_sim_data(comp_model, r_mean=50.0, r_var=25.0, custom_params=true_params)

guess = comp_guesser.make_guess(plate)

param_guess = [guess['C_0'], guess['N_0'], 0.0, 2.0]
print(param_guess)

for culture in plate.cultures:
    print(culture.no_cultures)
    culture.guess_est = culture.fit_model(guess_model, param_guess=param_guess,
                                          custom_options={'disp': True})


print(plate.sim_params[3:])
for culture in plate.cultures:
    print(culture.guess_est.x)

# So try fixing N_0 and C_0
