import numpy as np
import matplotlib.pyplot as plt


from scipy.integrate import odeint


from culture import RandomCulture


class Plate:


    def __init__(self, rows=3, cols=3, kn=None, ks=None):
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.find_neighbourhood()
        self.kn = kn
        self.ks = ks


    def find_neighbourhood(self):
        """Return a list of tuples of neighbour indices for each culture."""
        rows = self.rows
        cols = self.cols
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
        culture_params = params[2:]    # Could also do the iter here.
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
            # This will sometimes store a negative amounts. This can
            # be corrected in the results returned by odeint if call
            # values are ALSO set to zero at the start of each
            # function call (see np.maximum() above).
            rates = [rate for C, N, S, r, b, a, Ndiff, Sdiff in vals for rate in
                     (r*N*C - b*S, -r*N*C - kn*Ndiff, a*C - ks*Sdiff)]
            return rates
        return cans_growth


    def solve_model(self, init_amounts, times, params):
        growth_func = self.make_cans_model(params)
        sol = odeint(growth_func, init_amounts, times)
        return np.maximum(0, sol)


    # Should work for simulations, fits, and experimental data.
    # Times used by odeint can be returned as 'tcur' in the info dict
    # if full_output is set to True.
    def plot_growth(self, amounts, times, filename=None):
        fig = plt.figure()
        for i in range(self.no_cultures):
            fig.add_subplot(self.rows, self.cols, i+1)
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




# Can do this with or without using culture classes. Going to stick
# with Culture classes because we may more easily adapt code to
# simulate a plate of cultures that have different parameter
# distributions. This could be useful when testing fitting methods for
# fixing certain parameters on some plates.
class SimPlate(Plate):

    def __init__(self, rows=3, cols=3, kn=0.1, ks=0.1):
        # Call Plate __init__
        super(SimPlate, self).__init__(rows, cols, kn, ks)
        # Then also fill the plate with RandomCultures.
        self.cultures = [RandomCulture() for i in range(self.no_cultures)]


    def collect_init_amounts(self):
        """Collect a list of initial values for each culture.

        Return a flattened list of cell, nutirient, and signal amounts for
        each culture. I.e. [C0, N0, S0, C1, N1, S1, ...].
        """
        init_amounts = [amount for culture in self.cultures
                        for amount in (culture.cells, culture.nutrients,
                                       culture.signal)]
        return init_amounts


    def collect_params(self):
        """Collect parameters for each culture.

        Return a flattened list of r, b, and a constants for each culture.
        """
        culture_params = [param for culture in self.cultures
                          for param in (culture.r, culture.b, culture.a)]
        params = [self.kn, self.ks] + culture_params
        return params


if __name__ == '__main__':
    # Initialize a plate filled with random cultures.
    sim1 = SimPlate(3, 3)
    # Set/collect arguments for simulation.
    times = np.linspace(0, 15, 151)
    init_amounts = sim1.collect_init_amounts()
    cans_true_params = sim1.collect_params()
    # Simulate and save plot of cans growth.
    cans_sol = sim1.solve_model(init_amounts, times, cans_true_params)
    sim1.plot_growth(cans_sol, times, filename='cans_growth.pdf')
    # Now make independent by setting diffusion parameters to zero,
    sim1.kn = 0.0
    sim1.ks = 0.0
    inde_true_params = sim1.collect_params()
    # and simulate again
    inde_sol = sim1.solve_model(init_amounts, times, inde_true_params)
    sim1.plot_growth(inde_sol, times, filename='inde_growth.pdf')