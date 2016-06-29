"""Try guessing rs by fitting the independent model to individual
cultures."""
import numpy as np


from cans2.model import IndeModel, CompModel
from cans2.guesser import Guesser
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.zoning import resim_zone


inde_model = IndeModel()
comp_model = CompModel()
comp_guesser = Guesser(comp_model)
inde_plotter = Plotter(IndeModel())
comp_plotter = Plotter(CompModel())

# Simulate a 16x24 plate with noise
full_plate = Plate(16, 24)
full_plate.times = np.linspace(0, 5, 11)
true_params = {'N_0': 0.1, 'kn': 0.1}
true_params['C_0'] = true_params['N_0']/1000000
full_plate.set_sim_data(comp_model, b_mean=100.0, b_var=50.0,
                        custom_params=true_params)


# Guess bs for resimed 3x3 zone (i.e. a plate) with noise.
resim_zone = resim_zone(full_plate, comp_model, (5, 5), 3, 3, noise=True)
resim_amount_guess = comp_guesser.make_guess(resim_zone)
# No basis for an r_guess yet so just use 20.0 (may have to make
# random guesses)
inde_param_guess = [resim_amount_guess["C_0"], resim_amount_guess["N_0"], 20.0]
# We need to bound C_0 but not N_0 in this model. We could just use
# the guess C_0 as a fixed constraint.
inde_bounds = [(0, None) for i in range(3)]
inde_bounds[0] = (resim_amount_guess["C_0"], resim_amount_guess["C_0"])

# Guess using the independent model
inde_b_guesses = []
inde_N_0_guess = []
for culture in resim_zone.cultures:
    # Fit the independent model allowing N_0 to vary and compare to
    # true rs
    print(inde_bounds)
    print(inde_param_guess)

    culture.est = culture.fit_model(IndeModel(), param_guess=inde_param_guess,
                                    bounds=inde_bounds,
                                    minimizer_opts={'disp': False})
    inde_b_guesses.append(culture.est.x[-1])
    inde_N_0_guess.append(culture.est.x[1])


print(resim_zone.sim_params)
print(inde_b_guesses)
print(inde_N_0_guess)
inde_plotter.plot_est(culture, culture.est.x,
                      title="Inde fit with unbounded N_0")

comp_plotter.plot_est(resim_zone, resim_zone.sim_params)

for culture in resim_zone.cultures:
    print(culture.est.x)

comp_plotter.plot_culture_fits(resim_zone, inde_model, sim=True)

for culture in resim_zone.cultures:
    print(culture.est.x)
