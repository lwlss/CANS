"""Functions to make and solve the independent (CN) model."""
import numpy as np
import matplotlib.pyplot as plt


from random import gauss
from scipy.integrate import odeint
from scipy.optimize import minimize
from mpl_toolkits.axes_grid1 import AxesGrid
from functools import partial


from cans import find_neighbourhood, gauss_list


def make_inde_model(params):
    """Return a function for running the inde model.

    Args
    ----
    params : list
        Model parameters
    neighbourhood : list
        A list of tuples of neighbour indices for each culture.
    """
    # Separate out plate and culture level parameters.
    r_params = params
    # odeint requires times argument in cans_growth function.
    def inde_growth(amounts, times):
        """Return cans rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(r_params, *[iter(amounts)]*2)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for r, C, N, in vals for rate in (r*N*C, -r*N*C)]
        return rates
    return inde_growth


def solve_model(no_cultures, times, neighbourhood, params):
    """Solve ODEs return amounts of C and N.

    Args
    ----
    params : list
        Model parameters.
        r0, r1, r2 ...
    """
    # init_amounts should be an array of length 3*no_cultures.
    init_amounts = np.tile(params[:2], no_cultures)
    growth_func = make_inde_model(params[2:])
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)



# Identical to competition.py except for title.
def plot_growth(rows, cols, amounts, times,
                title='Idependent Growth', filename=None, data=None):
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
            ax.plot(data['times'], data['amounts'][:, i*2], 'x',
                    label='Cells Data')
      #     ax.plot(data['times'], data['amounts'][:, i*2 + 1], 'x',
      #     label='Nutrients Data')
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



def obj_func(no_cultures, times, c_meas, neighbourhood, params):
    """Objective function for fitting model."""
    # Now find the amounts from simulations using the parameters.
    amounts_est = solve_model(no_cultures, times, neighbourhood, params)
    c_est = np.array([amounts_est[:, i*2] for i in range(no_cultures)]).flatten()
    err = np.sqrt(sum((c_meas - c_est)**2))
    return err


# Functions required for simulations.

def gen_params(no_cultures, mean=1.0, var=0.0):
    """Return a np.array of parameter values."""
    # C(t=0), N(t=0)
    amounts = [0.005, 1.0]
    # r
    if var:
        r = gauss_list(no_cultures, mean, var, negs=False)
    else:
        r = [mean]*no_cultures
    # Initial guess: C(t=0), N(t=0), r0, r1,...
    params = np.array(amounts + r)
    return params



def simulate_amounts(rows, cols, times):
    """Return simulated amounts."""
    neighbourhood = find_neighbourhood(rows, cols)
    no_cultures = rows*cols
    params = gen_params(no_cultures, mean=1.0, var=1.0)
    true_amounts = solve_model(no_cultures, times, neighbourhood, params)
    return true_amounts


def fit_model(rows, cols, times, true_amounts, init_guess=None, maxiter=None):
    no_cultures = rows*cols
    neighbourhood = find_neighbourhood(rows, cols)
    c_meas = [true_amounts[:, i*2] for i in range(no_cultures)]
    c_meas = np.array(c_meas).flatten()
    obj_f = partial(obj_func, no_cultures, times, c_meas, neighbourhood)
    if init_guess is None:
        init_guess = guess_params(no_cultures)
    # All values non-negative.
    bounds = [(0.0, None) for i in range(len(init_guess))]
    # S(t=0) = 0.
    # bounds[2] = (0.0, 0.0)
    if maxiter is None:
        est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                              bounds=bounds,
                              options={'disp': True, 'maxfun': np.inf})
    else:
        options = {'disp': True, 'maxfun': np.inf, 'maxiter': maxiter}
        est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                              bounds=bounds, options=options)
                          # options={'disp': False, 'gtol': 1e-02,
                          #          'eps': 0.0001, 'maxiter': 1000})
    return est_params


if __name__ == '__main__':
    from cans import find_neighbourhood

    rows = 2
    cols = 2
    no_cultures = rows*cols
    times = np.linspace(0, 20, 21)

    # eventually put it a for loop and save the outputs or many simulations.
    sim = 0
    dir_name = "competition_fits/"

    # sim
    # Should actually use competition and not independent model for truth.
    true_amounts = simulate_amounts(rows, cols, times)

    init_amounts = gen_amounts(no_cultures)
    print(init_amounts)
    neighbourhood = find_neighbourhood(rows, cols)
    params = gen_params(no_cultures)
    print(params)
    params[1:4] = [0, 0, 0]
    print(params)
    true_amounts = solve_model(init_amounts, times, neighbourhood, params)

    # fit
    est_params = fit_model(rows, cols, times, true_amounts)
    est_init_amounts = np.tile(est_params.x[:2], no_cultures)
    est_amounts = solve_model(np.tile(est_params.x[:2], no_cultures),
                              times, neighbourhood, est_params.x[2:])
    plot_growth(rows, cols, true_amounts, times, title="Truth",
                filename='{0}truth_inde_{1}.pdf'.format(dir_name, sim))
    plot_growth(rows, cols, est_amounts, times, title="Estimation",
                filename='{0}est_inde_{1}.pdf'.format(dir_name, sim))
