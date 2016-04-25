import numpy as np
import matplotlib.pyplot as plt

from random import gauss
from scipy.integrate import odeint
from scipy.optimize import minimize
from functools import partial


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
    culture_params = params[2:]
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
        vals = zip(*[iter(amounts)]*3, *[iter(culture_params)]*3,
                   N_diffusions, S_diffusions)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for C, N, S, r, b, a, Ndiff, Sdiff in vals for rate
                 in (r*N*C - b*S*C, -r*N*C - kn*Ndiff, r*N*C - ks*Sdiff)]
        return rates
    return cans_growth


def solve_model(init_amounts, times, params, neighbourhood):
    """Solve ODEs return amounts of C, N, and S.

    Args
    ----
    params : list
        Model parameters.
        kn, ks, r0, b0, a0, r1, b1, a1, ...
    """
    # init_amounts should be an array of length 3*no_cultures.
    growth_func = make_cans_model(params, neighbourhood)
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)


def plot_growth(rows, cols, amounts, times, filename=None):
    """Plot a grid of timecourses of C, N, and S for each culture."""
    fig = plt.figure()
    for i in range(rows*cols):
        fig.add_subplot(rows, cols, i+1)
        plt.plot(times, amounts[:, i*3], 'b', label='cells')
        plt.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
        plt.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
        plt.xlabel('t')
        plt.grid()
    if filename is None:
        plt.show()
    else:
        # plt.legend(loc='best')
        plt.savefig(filename)


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

    kn, ks, r0, b0, a0, r1, b1, a1,...
    """
    # Plate level
    kn = 0.1    # Nutrient diffusion
    ks = 0.1    # Signal diffusion
    # Culture level
    # Growth rate constant
    r_mean = 1.0
    r_var = 1.0
    b = 0.05    # Signal on cells effect constant
    a = 0.05    # Signal secretion constant
    rba = [val for i in range(no_cultures) for val in
           (max(0.0, gauss(r_mean, r_var)), b, a)]
    params = np.array([kn, ks] + rba)
    return params


def obj_func(no_cultures, c_meas, neighbourhood, params):
    """Objective function for fitting model."""
    # Could do tiling later in solve_model if faster.
    init_amounts = np.tile(params[: 3], no_cultures)
    params = params[3:]
    # Now find the amounts from simulations using the parameters.
    amounts_est = solve_model(init_amounts, times, params, neighbourhood)
    c_est = np.array([amounts_est[:, i*3] for i in range(no_cultures)]).flatten()
    err = np.sqrt(sum((c_meas - c_est)**2))
    return err


def guess_params(no_cultures):
    """Return an initial parameter guess."""
    # C(t=0), N(t=0), S(t=0)
    amounts_guess = [0.2, 0.2, 0.0]
    # kn, ks
    kn_ks_guess = [0.05, 0.15]
    # r, b, a
    rates_guess = [1.0, 0.05, 0.05]
    # Initial guess: C(t=0), N(t=0), S(t=0), kn, ks, r0, b0, a0, r1, b1, a1, ...
    init_guess = np.array(amounts_guess + kn_ks_guess + rates_guess*no_cultures)
    return init_guess


if __name__ == '__main__':
    rows = 2
    cols = 2
    no_cultures = rows*cols
    neighbourhood = find_neighbourhood(rows, cols)
    params = gen_params(no_cultures)
    init_amounts = gen_amounts(no_cultures)
    times = np.linspace(0, 20, 201)
    true_amounts = solve_model(init_amounts, times, params, neighbourhood)

    # Fitting
    c_meas = [true_amounts[:, i*3] for i in range(no_cultures)]
    c_meas = np.array(c_meas).flatten()
    obj_f = partial(obj_func, no_cultures, c_meas, neighbourhood)
    # Initial parameter guess
    init_guess = guess_params(no_cultures)
    # All values non-negative.
    bounds = [(0.0, None) for i in range(len(init_guess))]
    # S(t=0) = 0.
    bounds[2] = (0.0, 0.0)
    est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                          bounds=bounds, options={'disp': True})
    est_amounts = solve_model(np.tile(est_params.x[: 3], no_cultures),
                              times, est_params.x[3 :], neighbourhood)
    plot_growth(rows, cols, true_amounts, times, filename='true.pdf')
    plot_growth(rows, cols, est_amounts, times, filename='est.pdf')
