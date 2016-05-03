import numpy as np
import pickle
import csv

from tabulate import tabulate

from cns import *


def mad(a, b):
    """Return mean absolute deviation."""
    return np.mean(np.abs(a - b))


model = 'simulation_fits/plate_9x9_1'
rows = 9
cols = 9
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
params = gen_params(no_cultures)
# Using the same random r values for fits of different models.
# with open('compare_fit_results/params3x3_data2.pickle', 'rb') as f:        # Make sure to change pickle file with data
#     params = pickle.load(f)

# We have to splice the pickled params to take into acount that b and
# a are now plate level rather than culture level.
kn_ks = list(params[:2])
r_params = list(params[2:][::3])
b_a = list(params[3:5])
params = np.array(kn_ks + b_a + r_params)

init_amounts = gen_amounts(no_cultures)
times = np.linspace(0, 20, 21)
true_amounts = solve_model(init_amounts, times, neighbourhood, params)
plot_growth(rows, cols, true_amounts, times)
# Save the paramter values to use in different models.
# with open('compare_fit_results/params3x3_data2.pickle', 'wb') as f:
#     pickle.dump(params, f)


# Fitting
c_meas = [true_amounts[:, i*3] for i in range(no_cultures)]
c_meas = np.array(c_meas).flatten()
obj_f = partial(obj_func, no_cultures, times, c_meas, neighbourhood)
# Initial parameter guess
init_guess = guess_params(no_cultures)
# All values non-negative.
bounds = [(0.0, None) for i in range(len(init_guess))]
# S(t=0) = 0
# bounds[2] = (0.0, 0.0)
est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                      bounds=bounds, options={'disp': True})
est_amounts = solve_model(np.tile(est_params.x[: 3], no_cultures),
                          times, neighbourhood, est_params.x[3 :])
plot_growth(rows, cols, true_amounts, times,
            filename=model+'_true.pdf', title='Truth')
plot_growth(rows, cols, est_amounts, times,
            filename=model+'_est.pdf', title='Estimation')


# Find error between true and estimated parameters.
true_params = np.append(init_amounts[:3], params[:])
true_plate_lvl = np.append(init_amounts[:3], params[:4])
true_rs = params[4:]

est_plate_lvl = est_params.x[:7]
est_rs = est_params.x[7:]

plate_lvl = np.abs(true_plate_lvl - est_plate_lvl)
r_mad = mad(true_rs, est_rs)

print(true_params)
print(est_params.x)
print(true_rs)
print(est_rs)

table = [
    ["C(t=0)", plate_lvl[0]], ["N(t=0)", plate_lvl[1]],
    ["S(t=0)", plate_lvl[2]], ["kn", plate_lvl[3]], ["ks", plate_lvl[4]],
    ["r (MAD)", r_mad], ["b", plate_lvl[5]], ["a", plate_lvl[6]]
]

print(tabulate(table, headers=["Parameter", "Deviation"]))
with open(model+'_devs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(table)
    writer.writerows([["True_params"],])
    writer.writerows([[val] for val in true_params])
    writer.writerows([["Est_params"],])
    writer.writerows([[val] for val in est_params.x])
