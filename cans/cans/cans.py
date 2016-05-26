import numpy as np
import matplotlib.pyplot as plt
import random
import copy


from scipy.integrate import odeint
from scipy.optimize import minimize
from functools import partial


def add_noise(data, sigma=0.02):
    """Return data with added random noise as np.ndarray."""
    if not isinstance(data, np.ndarray):
        noisey = np.asarray(copy.deepcopy(data), dtype=np.float64)
    else:
        noisey = copy.deepcopy(data)
    for x in np.nditer(noisey, op_flags=['readwrite']):
        x[...] = x + random.gauss(0, sigma)
    np.maximum(0, noisey, out=noisey)
    return noisey


# Going to place general functions in here for now but should probably
# move and rename module sooner rather than later.
def mad(a, b):
    """Return mean absolute deviation."""
    return np.mean(np.abs(a - b))


def gauss_list(n, mean=1.0, var=1.0, negs=False):
    """Return a list of n random gaussian numbers.

    If negs is False (default), negative values are round to zero.
    """
    vals = [random.gauss(mean, var) for i in range(n)]
    if negs:
        return vals
    else:
        return [max(0, v) for v in vals]


def find_neighbourhood(rows, cols):
    """Return a list of tuples of neighbour indices for each culture."""
    no_cultures = rows*cols
    neighbourhood = []
    for i in range(no_cultures):
        neighbours = []
        if i // cols:
            # Then not in first row.
            neighbours.append(i - cols)
        if i % cols:
            # Then not in first column.
            neighbours.append(i - 1)
        if (i + 1) % cols:
            # Then not in last column.
            neighbours.append(i + 1)
        if i < (rows - 1 )*cols:
            # Then not in last row.
            neighbours.append(i + cols)
        neighbourhood.append(tuple(neighbours))
    return neighbourhood


# Specific cans
def make_cans_model(params, neighbourhood):
    """Return a function for running the cans model.

    Args
    ----
    params : list
        Model parameters
    neighbourhood : list
        A list of tuples of neighbour indices for each culture.
    """
    # Separate out plate and culture level parameters.
    kn = params[0]
    ks = params[1]
    b = params[2]
    a = params[3]
    r_params = params[4:]
    # odeint requires times argument in cans_growth function.
    def cans_growth(amounts, times):
        """Return cans rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # Amounts of nutrients and signal.
        nutrients = amounts[1::3]
        signal = amounts[2::3]
        # Sums of nutrient and signal diffusion for each culture.
        N_diffusions = [sum([nutrient - nutrients[j] for j in neighbourhood[i]])
                        for i, nutrient in enumerate(nutrients)]
        S_diffusions = [sum([sig - signal[j] for j in neighbourhood[i]])
                        for i, sig in enumerate(signal)]
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(r_params, N_diffusions, S_diffusions, *[iter(amounts)]*3)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for r, Ndiff, Sdiff, C, N, S in vals for rate
                 in (r*N*C - b*S*C, -r*N*C - kn*Ndiff, a*C - ks*Sdiff)]
        return rates
    return cans_growth


def solve_model(init_amounts, times, neighbourhood, params):
    """Solve ODEs return amounts of C, N, and S.

    Args
    ----
    params : list
        Model parameters.
        kn, ks, b, a, r0, r1,...
    """
    # init_amounts should be an array of length 3*no_cultures.
    growth_func = make_cans_model(params, neighbourhood)
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)


# May choose just to have gen_params
def gen_amounts(no_cultures):
    """Return a list of initial amounts for a plate of cultures.

    C0(t=0), N0(t=0), S0(t=0), C1(t=0), N1(t=0), S1(t=0), ...
    """
    # Init amounts
    C = 0.1
    N = 1.0
    S = 0.0
    init_amounts = np.array([C, N, S]*no_cultures)
    return init_amounts


def gen_params(no_cultures):
    """Return a list of parameters for a plate of cultures.

    kn, ks, b, a, r0, r1,...
    """
    # Plate level
    kn = 0.1    # Nutrient diffusion
    ks = 0.1    # Signal diffusion
    b = 0.05    # Signal on cells effect constant
    a = 0.05    # Signal secretion constant
    # Culture level
    # Growth rate constant
    r_mean = 1.0
    r_var = 1.0
    r_params = [max(0.0, random.gauss(r_mean, r_var)) for i in range(no_cultures)]
    params = np.array([kn, ks, b, a] + r_params)
    return params


def obj_func(no_cultures, times, c_meas, neighbourhood, params):
    """Objective function for fitting model."""
    # Could do tiling later in solve_model if faster.
    init_amounts = np.tile(params[: 3], no_cultures)
    params = params[3:]
    # Now find the amounts from simulations using the parameters.
    amounts_est = solve_model(init_amounts, times, neighbourhood, params)
    c_est = np.array([amounts_est[:, i*3] for i in range(no_cultures)]).flatten()
    err = np.sqrt(sum((c_meas - c_est)**2))
    return err


def guess_params(no_cultures):
    """Return an initial parameter guess."""
    # C(t=0), N(t=0), S(t=0)
    amounts_guess = [0.2, 0.2, 0.0]
    # kn, ks
    kn_ks_guess = [0.05, 0.15]
    # b, a
    ba_guess = [0.05, 0.05]
    # r
    r_guess = [1.0]
    # Initial guess: C(t=0), N(t=0), S(t=0), kn, ks, r0, b0, a0, r1, b1, a1, ...
    init_guess = np.array(amounts_guess + kn_ks_guess +
                          ba_guess + r_guess*no_cultures)
    return init_guess


if __name__ == '__main__':
    from cans_plot import plot_growth
    rows = 3
    cols = 3
    no_cultures = rows*cols
    neighbourhood = find_neighbourhood(rows, cols)
    params = gen_params(no_cultures)
    init_amounts = gen_amounts(no_cultures)
    times = np.linspace(0, 20, 201)
    true_amounts = solve_model(init_amounts, times, neighbourhood, params)
    plot_growth(rows, cols, true_amounts, times)
    # # Fitting
    # c_meas = [true_amounts[:, i*3] for i in range(no_cultures)]
    # c_meas = np.array(c_meas).flatten()
    # obj_f = partial(obj_func, no_cultures, times, c_meas, neighbourhood)
    # # Initial parameter guess
    # init_guess = guess_params(no_cultures)
    # # All values non-negative.
    # bounds = [(0.0, None) for i in range(len(init_guess))]
    # # S(t=0) = 0.
    # bounds[2] = (0.0, 0.0)
    # est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
    #                       bounds=bounds, options={'disp': True})
    # est_amounts = solve_model(np.tile(est_params.x[: 3], no_cultures),
    #                           times, neighbourhood, est_params.x[3 :])
    # plot_growth(rows, cols, true_amounts, times, filename='true_func.pdf')
    # plot_growth(rows, cols, est_amounts, times, filename='est_func.pdf')
