import numpy as np

from scipy.optimize import minimize

from plate2 import Plate, SimPlate

plate1 = SimPlate(1, 2)
times = np.linspace(0, 20, 21)
true_init_amounts = np.array(plate1.collect_init_amounts())
true_params = np.array(plate1.collect_params())

print(times)
print(true_init_amounts)
print(true_params)

# simulate some data
true_amounts = np.array(plate1.solve_model(true_init_amounts, times, true_params))
#print(true_amounts)
# plate1.plot_growth(sol, times)

#print(true_amounts)
# Measured c_vals
c_meas = np.array([true_amounts[:, i*3] for i in range(plate1.no_cultures)]).flatten()
print('c_meas')
print(c_meas)

# First need to find C, (N, and S) from a simulation using the given parameters.
def obj_func(params):
    # Could do tiling later in solve model if
    init_amounts = np.tile(params[: 3], plate1.no_cultures)
    params = params[3:]
    # Now find the amounts from simulations using the parameters.
    amounts = plate1.solve_model(init_amounts, times, params)
    c_est = np.array([amounts[:, i*3] for i in range(plate1.no_cultures)]).flatten()
    err = np.sqrt(sum((c_meas - c_est)**2))
    return err


# Initial guess: C(t=0), N(t=0), S(t=0), kn, ks, r0, b0, a0, r1, b1, a1, ...
init_guess = np.array([0.2, 0.2, 0.0, 0.05, 0.15, 1.0, 0.05, 0.05, 1.0, 0.05, 0.05])
# Bounds on parameter values. All should be greater than zero.
bounds = [(0.0, None) for i in range(len(init_guess))]
#bounds[1] = (1.0, 1.0)

res = minimize(obj_func, init_guess, method='L-BFGS-B', bounds=bounds,
               options={'disp': True})

print(init_guess)
print(np.append(true_init_amounts, true_params))
print(res.x)

# plot the true amounts and the estimated amounts.
est_amounts = plate1.solve_model(np.tile(res.x[: 3], plate1.no_cultures),
                                 times, res.x[3 :])
plate1.plot_growth(true_amounts, times, filename='true.pdf')
plate1.plot_growth(est_amounts, times, filename='est.pdf')


# Now try two cultures. Then 9.
