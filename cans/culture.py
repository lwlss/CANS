"""Clases for the representation of microbial cultures."""

import numpy as np

from scipy.integrate import odeint
import matplotlib.pyplot as plt


class Culture:
    """A culture with an amount of cells, nutrients, and signal."""
    def __init__(self, cells=0.1, nutrients=1.0, signal=0.0):
        """Initialise culture.

        Parameters
        ----------
        cells : Optional[float]
            Initial amount of cells (default 0.1)
        nutrients : Optional[float]
            Initial amount of cells (default 1.0)
        signal : Optional[float]
            Initial amount of signal (default 0.0)
        """
        self.cells = cells
        self.nutrients = nutrients
        self.signal = signal


    def growth(self, y, t, r, b, a):
        """A growth model without diffusion."""
        C, N, S = y
        dydt = [r*N*C - b*S, -r*N*C, a*C]
        return dydt

    def sim_inde_growth(self, t):
        y0 = [self.cells, self.nutrients, self.signal]
        r = 1
        b = 0.01
        a = 0.01
        sol = odeint(self.growth, y0, t, args=(r, b, a))
        return sol

    def plot_growth_sim(self):
        t = np.linspace(0, 10, 101)
        sol = self.sim_inde_growth(t)
        plt.plot(t, sol[:, 0], 'b', label='cells')
        plt.plot(t, sol[:, 1], 'y', label='nutrients')
        plt.plot(t, sol[:, 2], 'r', label='signal')
        plt.legend(loc='best')
        plt.xlabel('t')
        plt.grid()
        plt.show()


if __name__ == '__main__':
    culture1 = Culture()
    culture1.plot_growth_sim()
