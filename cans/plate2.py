import numpy as np
import matplotlib.pyplot as plt


from scipy.integrate import odeint


from culture import RandomCulture


class Plate:


    def __init__(self, rows=3, cols=3, kn=None, ks=None):
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.fing_neighbourhood()
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
        kn = params[0]
        ks = params[1]
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
            vals = zip(*[iter(y)]*3, *[iter(params[2:])]*3, N_diffusions, S_diffusions)
            # This will sometimes store a negative amounts. This can
            # be corrected in the results returned by odeint if call
            # values are ALSO set to zero at the start of each
            # function call (see np.maximum() above).
            rates = [rate for C, N, S, r, b, a, Ndiff, Sdiff in vals for rate in
                     (r*N*C - b*S, -r*N*C - kn*Ndiff, a*C - ks*Sdiff)]
            return rates
        return cans_growth


    # Should work for simulations, fits, and experimental data.
    def plot_growth(self):
        pass


class SimPlate(Plate):

    def __init__(self, rows=3, cols=3, kn=None, ks=None):
        # Call Plate __init__
        super(SimPlate, self).__init__(rows=3, cols=3, kn=None, ks=None)
        # Then also fill the plate with RandomCultures.
        self.cultures = [RandomCulture() for i in range(self.no_cultures)]
