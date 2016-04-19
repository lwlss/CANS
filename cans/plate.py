"""Classes for the representation of agar plates."""

import numpy as np
import matplotlib.pyplot as plt


from scipy.integrate import odeint


from culture import Culture


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
        self.cultures = []
        for culture in range(rows*cols):
            self.cultures.append(Culture())


    def sim_growth(self):
        pass


    def collect_init_vals(self):
        """Collect a list of initial values for each culture.

        Return a flattened list of cell, nutirient, and signal amounts for
        each culture.

        """
        init_vals = [val for culture in self.cultures
                     for val in (culture.cells, culture.nutrients, culture.signal)]
        return init_vals


    def collect_params(self):
        """Collect parameters for each culture.

        Return a flattened list of r, b, and a constants for each culture.

        """
        params = [param for culture in self.cultures
                  for param in (culture.r, culture.b, culture.a)]
        return params


    # def grouper(self, iterable, n, fillvalue=None):
    #     "Collect data into fixed-length chunks or blocks"
    #     # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    #     args = [iter(iterable)] * n
    #     return zip_longest(fillvalue=fillvalue, *args)

    def inde_growth(self, y, t, r, b, a):
        """Return independent odes for each culture."""
        # The zip reapeats the same interator thrice so as to group y by
        # threes. This is a Python idiom.
        dydt = [rate for C, N, S in zip(*[iter(y)]*3)
                for rate in (r*N*C - b*S, -r*N*C, a*C)]
        return dydt


    def collect_odes(self):
        """Generate ODEs for the entire plate and a model."""
        init_vals = self.collect_init_vals()
        for i, culture in enumerate(self.cultures):
            if i < (self.rows - 1 )*self.cols:
                # then not in last row
                pass
            if (i + 1) % self.cols:
                # then not in last column
                pass

    def sim_inde_growth(self, t):
        init_vals = self.collect_init_vals()
        params = self.collect_params()
        sol = odeint(self.inde_growth, init_vals, t, args=tuple(params[0:3]))
        return sol

    def plot_growth_sims(self):
        t = np.linspace(0, 10, 101)
        sol = self.sim_inde_growth(t)
        print(sol)
        plt.plot(t, sol[:, 3], 'b', label='cells')
        plt.plot(t, sol[:, 4], 'y', label='nutrients')
        plt.plot(t, sol[:, 5], 'r', label='signal')
        plt.legend(loc='best')
        plt.xlabel('t')
        plt.grid()
        plt.show()



if __name__ == "__main__":
    plate1 = Plate()
    print(plate1.rows)
    print(plate1.cols)
    print(plate1.cultures)
    print(plate1.cultures[0].cells)
    print(plate1.cultures[0].nutrients)
    print(plate1.cultures[0].signal)
    print(len(plate1.cultures))
    print(plate1.collect_init_vals())
    print(len(plate1.collect_init_vals()))
    print(plate1.collect_params())
    print(len(plate1.collect_params()))
    plate1.plot_growth_sims()
