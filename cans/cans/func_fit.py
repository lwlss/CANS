import numpy as np
import pickle
import csv

from tabulate import tabulate

from cans import *
from cans_plot import plot_growth_grid as plot_growth


def mad(a, b):
    """Return mean absolute deviation."""
    return np.mean(np.abs(a - b))


model = 'compare_fit_results/mod1'
rows = 3
cols = 3
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
# params = gen_params(no_cultures)
# Using the same random r values for fits of different models.
with open('compare_fit_results/params3x3.pickle', 'rb') as f:
    params = pickle.load(f)
init_amounts = gen_amounts(no_cultures)
times = np.linspace(0, 20, 21)
true_amounts = solve_model(init_amounts, times, neighbourhood, params)
plot_growth(rows, cols, true_amounts, times)
# Save the paramter values to use in different models.
# with open('params3x3.pickle', 'wb') as f:
#     pickle.dump(params, f)


# Fitting
c_meas = [true_amounts[:, i*3] for i in range(no_cultures)]
c_meas = np.array(c_meas).flatten()
obj_f = partial(obj_func, no_cultures, times, c_meas, neighbourhood)
# Initial parameter guess
init_guess = guess_params(no_cultures)
# All values non-negative.
bounds = [(0.0, None) for i in range(len(init_guess))]
# S(t=0) = 0.
bounds[2] = (0.0, 0.0)
est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                      bounds=bounds, options={'disp': True})
est_amounts = solve_model(np.tile(est_params.x[: 3], no_cultures),
                          times, neighbourhood, est_params.x[3 :])
plot_growth(rows, cols, true_amounts, times, filename=model+'_true.pdf')
plot_growth(rows, cols, est_amounts, times, filename=model+'_est.pdf')


# Find error between true and estimated parameters.
true_params = np.append(init_amounts[:3], params[:])
true_plate_lvl = np.append(init_amounts[:3], params[:2])
true_rs = params[2:][::3]
true_bs = params[2:][1::3]
true_as = params[2:][2::3]

print(true_params)

est_plate_lvl = est_params.x[:5]
est_rs = est_params.x[5:][::3]
est_bs = est_params.x[5:][1::3]
est_as = est_params.x[5:][2::3]

print(est_params.x)


plate_lvl = np.abs(true_plate_lvl - est_plate_lvl)
r_mad = mad(true_rs, est_rs)
b_mad = mad(true_bs, est_bs)
a_mad = mad(true_as, est_as)


table = [
    ["C(t=0)", plate_lvl[0]], ["N(t=0)", plate_lvl[1]],
    ["S(t=0)", plate_lvl[2]], ["kn", plate_lvl[3]], ["ks", plate_lvl[4]],
    ["r (MAD)", r_mad], ["b (MAD)", b_mad], ["a (MAD)", a_mad]
]

print(tabulate(table, headers=["Parameter", "Deviation"]))
with open(model+'_devs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(table)
