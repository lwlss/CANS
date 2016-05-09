"""Functions to make and solve the competition (CN) model."""
import numpy as np
import matplotlib.pyplot as plt


from random import gauss
from scipy.integrate import odeint
from scipy.optimize import minimize
from mpl_toolkits.axes_grid1 import AxesGrid
from functools import partial


from cans import find_neighbourhood, gauss_list


def make_comp_model(params, neighbourhood):
    """Return a function for running the competition model.

    Args
    ----
    params : list
        Model parameters
    neighbourhood : list
        A list of tuples of neighbour indices for each culture.
    """
    # Separate out plate and culture level parameters.
    kn = params[0]
    r_params = params[1:]
    # odeint requires times argument in cans_growth function.
    def comp_growth(amounts, times):
        """Return model rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # Amounts of nutrients and signal.
        nutrients = amounts[1::2]
        # Sums of nutrient and signal diffusion for each culture.
        N_diffusions = [sum([nutrient - nutrients[j] for j in neighbourhood[i]])
                        for i, nutrient in enumerate(nutrients)]
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(*[iter(amounts)]*2, r_params, N_diffusions)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for C, N, r, Ndiff in vals for rate
                 in (r*N*C, -r*N*C - kn*Ndiff)]
        return rates
    return comp_growth


def solve_model(no_cultures, times, neighbourhood, params):
    """Solve ODEs return amounts of C and N.

    Args
    ----
    init_amounts : list
        Initial cell and signal amounts as a list
        [C0(t=0), N0(t=0), C1(t=0), N1(t=0),... ]
    times : list
        A list of cell observation times. The timepoints for
        which the model is solved.
    neighbourhood : list of tuples
        The length of neighbourhood should be equal the number
        of cultures. Tuples at index i in neighbourhood should
        contain the indices of i's neighbours.
    params : list
        Model parameters.
        kn, r0, r1,...

    """
    # init_amounts should be an array of length 2*no_cultures.
    init_amounts = np.tile(params[:2], no_cultures)
    growth_func = make_comp_model(params[2:], neighbourhood)
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)


def plot_growth(rows, cols, amounts, times, title='Competition Growth',
                filename=None, data=None):
    """Plot a grid of timecourses of C and N for each culture.

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
        ax.plot(times, amounts[:, i*2], 'b', label='Cells')
        ax.plot(times, amounts[:, i*2 + 1], 'y', label='Nutrients')
        if data is not None:
            ax.plot(times, data[:, i*2], 'x', label='Cells Data')
            ax.plot(times, data[:, i*2 + 1], 'x', label='Nutrients Data')
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
    plt.close()


# Functions for fitting

def gen_params(no_cultures, mean=1.0, var=0.0):
    """Return a np.array of parameter values."""
    # C(t=0), N(t=0)
    amounts = [0.005, 1.5]
    # kn
    kn = [0.0]
    # r
    if var:
        r = gauss_list(no_cultures, mean, var, negs=False)
    else:
        r = [mean]*no_cultures
    # Initial guess: C(t=0), N(t=0), kn, r0, r1,...
    params = np.array(amounts + kn + r)
    return params


def obj_func(no_cultures, times, c_meas, neighbourhood, params):
    """Objective function for fitting model."""
    # Now find the amounts from simulations using the parameters.
    amounts_est = solve_model(no_cultures, times, neighbourhood, params)
    c_est = np.array([amounts_est[:, i*2] for i in range(no_cultures)]).flatten()
    err = np.sqrt(sum((c_meas - c_est)**2))
    return err


# Functions required for simulations.

def simulate_amounts(rows, cols, times):
    """Return simulated amounts for competition model."""
    neighbourhood = find_neighbourhood(rows, cols)
    no_cultures = rows*cols
    params = gen_params(no_cultures, mean=1.0, var=1.0)
    true_amounts = solve_model(no_cultures, times, neighbourhood, params)
    return true_amounts


def fit_model(rows, cols, times, true_amounts, init_guess=None):
    no_cultures = rows*cols
    neighbourhood = find_neighbourhood(rows, cols)
    c_meas = [true_amounts[:, i*2] for i in range(no_cultures)]
    c_meas = np.array(c_meas).flatten()
    obj_f = partial(obj_func, no_cultures, times, c_meas, neighbourhood)
    if init_guess is None:
        init_guess = gen_params(no_cultures)
    elif init_guess == 'rand_r':
        init_guess = gen_params(no_cultures, mean=1.0, var=1.0)
    else:
        assert(len(init_guess) == 3 + rows*cols)
    print('comp', init_guess)
    # All values non-negative.
    bounds = [(0.0, None) for i in range(len(init_guess))]
    # S(t=0) = 0.
    # bounds[2] = (0.0, 0.0)
    est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                          bounds=bounds, options={'disp': True})#, tol=1e-4)
                          # options={'disp': False, 'gtol': 1e-02,
                          #          'eps': 0.0001, 'maxiter': 1000})
    return est_params


if __name__ == '__main__':
    from cans import find_neighbourhood

    rows = 3
    cols = 3
    no_cultures = rows*cols
    times = np.linspace(0, 20, 21)

    # eventually put it a for loop and save the outputs or many simulations.
    sim = 0
    dir_name = "competition_fits/"

    # sim
    true_amounts = simulate_amounts(rows, cols, times)

    # fit
    neighbourhood = find_neighbourhood(rows, cols)
    est_params = fit_model(rows, cols, times, true_amounts)
    est_init_amounts = np.tile(est_params.x[:2], no_cultures)
    est_amounts = solve_model(no_cultures, times, neighbourhood, est_params.x)
    plot_growth(rows, cols, true_amounts, times, title="Truth",
                filename='{0}truth_{1}.pdf'.format(dir_name, sim))
    plot_growth(rows, cols, est_amounts, times, title="Estimation",
                filename='{0}est_{1}.pdf'.format(dir_name, sim))
