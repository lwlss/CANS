import numpy as np

from scipy.optimize import minimize

from plate2 import SimPlate

plate1 = SimPlate(1, 1)
times = np.linspace(0, 15, 16)
true_init_amounts = plate1.collect_init_amounts()
true_params = plate1.collect_params()

print(times)
print(true_init_amounts)
print(true_params)

# simulate some data
true_amounts = np.array(plate1.solve_model(true_init_amounts, times, true_params))
# plate1.plot_growth(sol, times)

#print(true_amounts)
# Measured c_vals
c_meas = true_amounts[:, 0]
print(c_meas)

# First need to find C, (N, and S) from a simulation using the given parameters.
def obj_func(params):
    init_amounts = params[: 3*plate1.no_cultures]
    params = params[3*plate1.no_cultures:]
    # Now find the amounts from simulations using the parameters.
    amounts = plate1.solve_model(init_amounts, times, params)
    c_est = amounts[:, 0]
    err = np.sqrt(sum((c_meas - c_est)**2))
    return err

# Initialization
# Initial guess at parameter values

init_guess = true_init_amounts + [plate1.kn, plate1.ks] + [1.0] + true_params[3:]
#init_guess = np.array(
print(init_guess)
res = minimize(obj_func, init_guess, method='BFGS', options={'disp': True})
print(res.x)
print(true_params)
