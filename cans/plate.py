"""Classes for the representation of agar plates."""

import numpy as np
import matplotlib.pyplot as plt
import math

from operator import add
from scipy.integrate import odeint


from culture import Culture, RandomCulture


class Plate:
    """An agar plate containing cultures."""
    def __init__(self, rows=3, cols=3, kn=0.0, ks=0.0):
        """Initialise plate with an array of cultures.

        Parameters
        ----------
        rows : Optional[int]
            Number of rows (default 3)
        cols : Optional[int]
            Number of columns (default 3)
        kn : Optional[float]
            Nutrient diffusion constant (default 0.0)
        ks : Optional[float]
            Signal diffusion constant (default 0.0)
        cultures : list[Culture]
            A list of rows*cols Culture objects.
        """
        self.rows = rows
        self.cols = cols
        self.kn = kn
        self.ks = ks
        self.cultures = self.get_cultures()


    def get_cultures(self):
        """Populate plate with cultures with the same parameters."""
        return [Culture() for culture in range(self.rows*self.cols)]


    def collect_init_vals(self):
        """Collect a list of initial values for each culture.

        Return a flattened list of cell, nutirient, and signal amounts for
        each culture. I.e. [C0, N0, S0, C1, N1, S1, ...].
        """
        init_vals = [val for culture in self.cultures
                     for val in (culture.cells, culture.nutrients,
                                 culture.signal)]
        return init_vals


    def collect_params(self):
        """Collect parameters for each culture.

        Return a flattened list of r, b, and a constants for each culture.

        """
        params = [param for culture in self.cultures
                  for param in (culture.r, culture.b, culture.a)]
        return params


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
            if (i + 1) % self.cols:
                # Then not in last column.
                neighbours.append(i + 1)
            if i < (rows - 1 )*cols:
                # Then not in last row.
                neighbours.append(i + cols)
            neighbourhood.append(tuple(neighbours))
        return neighbourhood


    def inde_growth(self, y, t, params):
        """Return independent odes for each culture."""
        # Cannot have negative cell numbers or concentrations
        np.maximum(0, y, out=y)
        # The zip reapeats the same interator thrice so as to group y by
        # threes. This is a Python idiom.
        rates = [rate for C, N, S, r, b, a in zip(*[iter(y)]*3, *[iter(params)]*3)
                 for rate in (r*N*C - b*S, -r*N*C, a*C)]    # *b*S*C?
        return rates


    def sim_inde_growth(self, t):
        """Simulate independent growth for ."""
        init_vals = self.collect_init_vals()
        params = self.collect_params()
        sol = odeint(self.inde_growth, init_vals, t, args=(params,))
        # Remove negative amounts.
        np.maximum(0, sol, out=sol)
        return sol


    def plot_inde_sims(self, filename='inde.pdf'):
        """Plot growth curves for each culture."""
        t = np.linspace(0, 15, 151)
        sol = self.sim_inde_growth(t)
        fig = plt.figure()
        for i in range(self.rows*self.cols):
            fig.add_subplot(self.rows, self.cols, i+1)
            plt.plot(t, sol[:, i*3], 'b', label='cells')
            plt.plot(t, sol[:, i*3 + 1], 'y', label='nutrients')
            plt.plot(t, sol[:, i*3 + 2], 'r', label='signal')
            plt.xlabel('t')
            plt.grid()
        if filename is None:
            plt.show()
        else:
            # plt.legend(loc='best')
            plt.savefig(filename)


    def cans_growth(self, y, t, params, neighbourhood):
        """Return independent odes for each culture.

        y contains a list of cells, nutrients, and signal... repeated
        for each culture.

        """
        # Cannot have negative cell numbers or concentrations. If we
        # set this here then we may still get negative values for
        # amounts in the solution but these can be replaced without
        # having any side effects.
        np.maximum(0, y, out=y)
        try:
            assert(min(y) >= 0)
        except AssertionError:
            print("y contains C, N, or S less than zero.")
        # Amounts of nutrients and signal.
        nutrients = y[1::3]
        signal = y[2::3]
        # Sums of nutrient and signal diffusion for each culture.
        N_diffusions = [sum([nutrient - nutrients[j] for j in neighbourhood[i]])
                        for i, nutrient in enumerate(nutrients)]
        S_diffusions = [sum([sig - signal[j] for j in neighbourhood[i]])
                        for i, sig in enumerate(signal)]
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(*[iter(y)]*3, *[iter(params)]*3, N_diffusions, S_diffusions)
        # This will sometimes store a negative amounts. This can be
        # corrected in the results returned by odeint if at the start
        # of each function call values are set to zero (see
        # np.maximum() above).
        rates = [rate for C, N, S, r, b, a, Ndiff, Sdiff in vals for rate in
                (r*N*C - b*S, -r*N*C - self.kn*Ndiff, a*C - self.ks*Sdiff)]
        return rates


    def sim_cans_growth(self, t):
        """Simulate cans growth for whole plate."""
        init_vals = self.collect_init_vals()
        # can I just define params and neighbourhood in this scope and
        # not have to pass them to odeint? Conor acheives this by
        # defining the ode function within another function which
        # returns the inner function. Maybe odeint deals with args in
        # a clever way though so that they are not passes every time.
        # Also consider moviing growth models to a different module.
        params = self.collect_params()
        neighbourhood = self.find_neighbourhood()
        sol = odeint(self.cans_growth, init_vals, t,
                     args=(params, neighbourhood))
        # Remove negative amounts.
        np.maximum(0, sol, out=sol)
        print("Solved")
        return sol


    def plot_cans_sims(self, filename='cans.pdf'):
        """Plot growth curves for each culture."""
        t = np.linspace(0, 15, 151)
        sol = self.sim_cans_growth(t)
        fig = plt.figure()
        for i in range(self.rows*self.cols):
            fig.add_subplot(self.rows, self.cols, i+1)
            plt.plot(t, sol[:, i*3], 'b', label='cells')
            plt.plot(t, sol[:, i*3 + 1], 'y', label='nutrients')
            plt.plot(t, sol[:, i*3 + 2], 'r', label='signal')
            plt.xlabel('t')
            plt.grid()
        if filename is None:
            plt.show()
        else:
            # plt.legend(loc='best')
            plt.savefig(filename)


class RandomPlate(Plate):
    """A plate containing cultures with randomised parameters."""

    def get_cultures(self):
        """Return a list of cultures with random parameters."""
        # This is called in __init__.
        return [RandomCulture() for culture in range(self.rows*self.cols)]


if __name__ == "__main__":
#     plate1 = Plate()
#     print(plate1.rows)
#     print(plate1.cols)
#     print(plate1.cultures)
#     print(plate1.cultures[0].cells)
#     print(plate1.cultures[0].nutrients)
#     print(plate1.cultures[0].signal)
#     print(len(plate1.cultures))
#     print(plate1.collect_init_vals())
#     print(len(plate1.collect_init_vals()))
#     print(plate1.collect_params())
#     print(len(plate1.collect_params()))
# #    plate1.plot_growth_sims()
#     print(plate1.find_neighbourhood())
#    plate1.plot_cans_sims()
    rand_plate = RandomPlate(3, 3, kn=0.1, ks=0.1)
#    t = np.linspace(0, 15, 151)
#    rand_plate.sim_cans_growth(t)
    rand_plate.plot_cans_sims()
    rand_plate.plot_inde_sims()
    # rand_plate.plot_cans_sims(t)
    # rand_plate.kn = 0.0
    # rand_plate.ks = 0.0
    # rand_plate.plot_cans_sims('inde.pdf')
