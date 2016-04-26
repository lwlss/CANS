import numpy as np
import matplotlib.pyplot as plt


from scipy.integrate import odeint
from scipy.optimize import minimize


from culture import RandomCulture


class Plate:
    def __init__(self, rows=3, cols=3, kn=None, ks=None):
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.find_neighbourhood()
        self.kn = kn
        self.ks = ks
        # self.init_params
        # self.init_amounts = None
        # self.init_guess
        # self.times = times



    def find_neighbourhood(self):
        """Return a list of tuples of neighbour indices for each culture."""
        rows = self.rows
        cols = self.cols
        neighbourhood = []
        for i in range(self.no_cultures):
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


    def make_cans_model(self, params):
        """Return a function for running the cans model.

        Args
        ----
        params : list
            Model parameters
        """
        neighbourhood = self.neighbourhood
        # Separate out plate and culture level parameters.
        kn = params[0]
        ks = params[1]
        culture_params = params[2:]
        # Must have times as argument in cans_growth function as this
        # is a requirement of odeint?
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


    def solve_model(self, init_amounts, params):
        # init_amounts should be an array of length 3*no_cultures.
        growth_func = self.make_cans_model(params)
        sol = odeint(growth_func, init_amounts, self.times)
        return np.maximum(0, sol)


    # Should work for simulations, fits, and experimental data.
    # Times used by odeint can be returned as 'tcur' in the info dict
    # if full_output is set to True.
    def plot_growth(self, amounts, filename=None):
        fig = plt.figure()
        for i in range(self.no_cultures):
            fig.add_subplot(self.rows, self.cols, i+1)
            plt.plot(self.times, amounts[:, i*3], 'b', label='cells')
            plt.plot(self.times, amounts[:, i*3 + 1], 'y', label='nutrients')
            plt.plot(self.times, amounts[:, i*3 + 2], 'r', label='signal')
            plt.xlabel('t')
            plt.grid()
        if filename is None:
            plt.show()
        else:
            # plt.legend(loc='best')
            plt.savefig(filename)


    def obj_func(self, params):
        # Could do tiling later in solve_model if faster.
        init_amounts = np.tile(params[: 3], self.no_cultures)
        params = params[3:]
        # Now find the amounts from simulations using the parameters.
        amounts_est = self.solve_model(init_amounts, params)
        c_est = np.array([amounts_est[:, i*3] for i in range(self.no_cultures)]).flatten()
        err = np.sqrt(sum((self.c_meas - c_est)**2))
        return err


    def init_guess(self):
        """Return an initial parameter guess."""
        # C(t=0), N(t=0), S(t=0)
        amounts_guess = [0.2, 0.2, 0.0]
        # kn, ks
        kn_ks_guess = [0.05, 0.15]
        # r, b, a
        rates_guess = [1.0, 0.05, 0.05]
        # Initial guess: C(t=0), N(t=0), S(t=0), kn, ks, r0, b0, a0, r1, b1, a1, ...
        init_guess = np.array(amounts_guess + kn_ks_guess
                              + rates_guess*self.no_cultures)
        return init_guess




# Can do this with or without using culture classes. Going to stick
# with Culture classes because we may more easily adapt code to
# simulate a plate of cultures that have different parameter
# distributions. This could be useful when testing fitting methods for
# fixing certain parameters on some plates.
class SimPlate(Plate):

    def __init__(self, rows=3, cols=3, kn=0.1, ks=0.1, times=None):
        # Call Plate __init__
        super(SimPlate, self).__init__(rows, cols, kn, ks)
        # Then also fill the plate with RandomCultures.
        self.cultures = [RandomCulture() for i in range(self.no_cultures)]
        self.true_init_amounts = self.collect_init_amounts()
        self.true_params = self.collect_params()
        self.times = times    # Can be taken from the data for a plate.
        # Artificial data including hidden varibles.
        self.true_amounts = self.solve_model(self.true_init_amounts,
                                             self.true_params)
        # Cells times-course. The data from a real plate.
        self.c_meas = np.array([self.true_amounts[:, i*3] for i in
                                range(self.no_cultures)]).flatten()


    def collect_init_amounts(self):
        """Collect a list of initial values for each culture.

        Return a flattened list of cell, nutirient, and signal amounts for
        each culture. I.e. [C0, N0, S0, C1, N1, S1, ...].
        """
        init_amounts = [amount for culture in self.cultures for amount in
                        (culture.cells, culture.nutrients, culture.signal)]
        return init_amounts


    def collect_params(self):
        """Collect parameters for each culture.

        Return a flattened list of r, b, and a constants for each culture.
        """
        culture_params = [param for culture in self.cultures
                          for param in (culture.r, culture.b, culture.a)]
        params = [self.kn, self.ks] + culture_params
        return params


    def fit_data(self, plot=True):
        init_guess = self.init_guess()
        bounds = [(0.0, None) for i in range(len(init_guess))]
        bounds[2] = (0.0, 0.0)    # S(t=0), remove from params and
                                  # instead set const.
        res = minimize(self.obj_func, init_guess, method='L-BFGS-B',
                       bounds=bounds, options={'disp': True})
        est_amounts = self.solve_model(np.tile(res.x[: 3], self.no_cultures),
                                       res.x[3 :])
        if plot:
            self.plot_growth(self.true_amounts, filename='true.pdf')
            self.plot_growth(est_amounts, filename='est.pdf')
        return est_amounts


if __name__ == '__main__':
    # Initialize a plate filled with random cultures.
    times = np.linspace(0, 20, 201)
    sim1 = SimPlate(3, 3, times=times)
    # Set/collect arguments for simulation.
    cans_true_params = sim1.collect_params()
    # Simulate and save plot of cans growth.
    cans_sol = sim1.true_amounts
    sim1.plot_growth(cans_sol, filename='cans_growth.pdf')
    # Now make independent by setting diffusion parameters to zero,
    sim1.kn = 0.0
    sim1.ks = 0.0
    init_amounts = sim1.collect_init_amounts()
    # Careful not to use self.true_params which contains old kn, ks.
    inde_true_params = sim1.collect_params()
    # and simulate again
    inde_sol = sim1.solve_model(init_amounts, inde_true_params)
    sim1.plot_growth(inde_sol, filename='inde_growth.pdf')
