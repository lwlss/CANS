import numpy as np
from scipy.integrate import odeint

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
    b = params[0]
    a = params[1]
    r_params = params[2:]
    # odeint requires times argument in cans_growth function.
    def inde_growth(amounts, times):
        """Return cans rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(*[iter(amounts)]*3, r_params)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for C, N, S, r in vals for rate
                 in (r*N*C - b*S*C, -r*N*C, a*C)]
        return rates
    return inde_growth


def solve_inde_model(init_amounts, times, neighbourhood, params):
    """Solve ODEs return amounts of C, N, and S.

    Args
    ----
    params : list
        Model parameters.
        b, a, r0, r1, r2 ...
    """
    # init_amounts should be an array of length 3*no_cultures.
    growth_func = make_inde_model(params, neighbourhood)
    sol = odeint(growth_func, init_amounts, times)
    return np.maximum(0, sol)
