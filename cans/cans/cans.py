import numpy as np
import matplotlib.pyplot as plt


from scipy.integrate import odeint


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
    neighbourhood : list(tuples)
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


def solve_model(init_amounts, times, params):
    """Solve ODEs return amounts of C, N, and S."""
    # init_amounts should be an array of length 3*no_cultures.
    growth_func = make_cans_model(params)
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)


def plot_growth(rows, cols, amounts, times, filename=None):
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
def gen_amounts(rows, cols):
    pass

def gen_params(rows, cols):
    # Init amounts
    C = 0.1
    N = 1.0
    S = 0.0
    # Plate level
    kn = 0.1    # Nutrient diffusion
    ks = 0.1    # Signal diffusion
    # Culture level
    r = max(0.0, random.gauss(1.0, 1.0))   # Growth rate constant
    b = 0.05   # Signal on cells effect constant
    a = 0.05    # Signal secretion constant



if __name__ == '__main__':
    rows = 3
    cols = 3
    neighbourhood = find_neighbourhood(rows, cols)
    params = gen_params(rows, cols)
    print(make_cans_model(params, neighbourhood))
