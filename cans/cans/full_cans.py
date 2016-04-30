import numpy as np
from scipy.integrate import odeint


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
        vals = zip(*[iter(amounts)]*3, r_params, N_diffusions,
                   S_diffusions)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for C, N, S, r, Ndiff, Sdiff in vals for rate
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
