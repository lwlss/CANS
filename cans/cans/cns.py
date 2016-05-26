import numpy as np
import matplotlib.pyplot as plt


from random import gauss
from scipy.integrate import odeint
from scipy.optimize import minimize
from functools import partial


def make_cns_model(params, neighbourhood):
    """Return a function for running the cns model.

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
    # odeint requires times argument in cns_growth function.
    def cns_growth(amounts, times):
        """Return cns rates given current amounts and times."""
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
    return cns_growth


def solve_model(init_amounts, times, neighbourhood, params):
    """Solve ODEs return amounts of C, N, and S.

    Args
    ----
    params : list
        Model parameters.
        kn, ks, b, a, r0, r1,...
    """
    # init_amounts should be an array of length 3*no_cultures.
    growth_func = make_cns_model(params, neighbourhood)
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)


# May choose just to have gen_params
def gen_amounts(no_cultures):
    """Return a list of initial amounts for a plate of cultures.

    C0(t=0), N0(t=0), S0(t=0), C1(t=0), N1(t=0), S1(t=0), ...
    """
    # Init amounts
    C = 0.01
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
    r_params = [max(0.0, gauss(r_mean, r_var)) for i in range(no_cultures)]
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


def plot_growth(rows, cols, amounts, times, title='CNS Growth', filename=None):
    """Plot a grid of timecourses of C, N, and S for each culture.

    Uses AxesGrid from mpl_loolkits.axes_grid1.
    """
    ymax = np.amax(amounts)
    ymax = np.ceil(ymax*10)/10
    fig = plt.figure()
    fig.suptitle(title, fontsize=20)
    # http://stackoverflow.com/a/36542971
    # Add big axes and hide frame.
    fig.add_subplot(111, frameon=False)
    # Hide tick and tick label of the big axes.
    plt.tick_params(labelcolor='none', top='off',
                    bottom='off', left='off', right='off')
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Amount', fontsize=18)
    grid = AxesGrid(fig, 111, nrows_ncols=(rows, cols),
                    axes_pad=0.1, aspect=False, share_all=True)

    for i, ax in enumerate(grid):
        ax.set_ylim(0.0, ymax)
        ax.plot(times, amounts[:, i*3], 'b', label='cells')
        ax.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
        ax.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
        ax.grid()
        if i + 1 > (rows - 1)*cols:
            # Then in last row.
            plt.setp(ax.get_xticklabels()[-1], visible=False)
            # pass
        if not i % cols:
            # Then in first column.
            plt.setp(ax.get_yticklabels()[-1], visible=False)
            # pass

    # grid[-1].legend(loc='best')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


if __name__ == '__main__':
    from cans import find_neighbourhood, mad
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
