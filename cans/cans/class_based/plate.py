import numpy as np


from model import IndeModel
from fitter import Fitter


class BasePlate:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.find_neighbourhood()
        self.data = data
        # Is data going to be a dictionary of observation times and
        # cell measurements? Let's assume so.
        if data is not None:
            self.c_meas = data['c_meas']    # Should flatten as np.array
            self.times = data['times']
        else:
            self.c_meas = None    # Should flatten as np.array
            self.times = None
        # Attributes for simulated data.
        self.sim_amounts = None
        self.sim_params = None


    def find_neighbourhood(self):
        """Return a list of tuples of neighbour indices for each culture."""
        neighbourhood = []
        for i in range(self.no_cultures):
            neighbours = []
            if i // self.cols:
                # Then not in first row.
                neighbours.append(i - self.cols)
            if i % self.cols:
                # Then not in first column.
                neighbours.append(i - 1)
            if (i + 1) % self.cols:
                # Then not in last column.
                neighbours.append(i + 1)
            if i < (self.rows - 1 )*self.cols:
                # Then not in last row.
                neighbours.append(i + self.cols)
            neighbourhood.append(tuple(neighbours))
        return neighbourhood


    def fit_model(self, model, param_guess=None, maxiter=None):
        """Return estimates from fitting model to plate."""
        fitter = Fitter(model)
        est = fitter.fit_model(self, param_guess, maxiter)
        return est


class Plate(BasePlate):
    def __init__(self, rows, cols, data=None):
        super(Plate, self).__init__(rows, cols, data)
        if self.data is not None:
            # Feed data to Cultures. Depends on form of data but would
            # like a dictionary with times and c_meas.
            pass
        else:
            self.cultures = [Culture() for i in range(self.no_cultures)]


    def set_cultures(self):
        """Add Culture data from sims."""
        for i, culture in enumerate(self.cultures):
            # May need to pass the model used in order to
            # generalize. Then we can also provide parameters used for
            # the simulations and other amounts (e.g. N). We can also
            # use model.no_species. This is not possible with real
            # data and not really necessary with simulated data.
            no_species = int(len(self.sim_amounts[0])/self.no_cultures)
            culture.c_meas = self.sim_amounts[:, i*no_species].flatten()
            culture.times = self.times


    def est_from_cultures(self):
        """Estimate parameters from inde fits of individual Cultures.

        Set idependent estimates (with scipy.integrate.odeint data) as
        culture attribute inde_est and return estimate values.

        """
        # Could be generalized by supplying Model as argument. For
        # instance if we have different independent models.
        inde_model = IndeModel()
        # Make inde fits for individual Cultures.
        for culture in self.cultures:
            culture.inde_est = culture.fit_model(inde_model)
        params = np.array([c.inde_est.x for c in self.cultures])
        # Only take averages if r>0 otherwise amount estimates are arbitrary.
        avgs = np.average([p for p in params if p[-1]], axis=0)
        # Averages only for plate level params.
        avg_params = np.append(avgs[:inde_model.r_index],
                               params[:, inde_model.r_index])
        return avg_params




class Culture(BasePlate):
    def __init__(self, data=None):
        super(Culture, self).__init__(1, 1, data)

if __name__ == '__main__':
    plate1 = Plate(3, 3)
    culture1 = Culture()
    print(plate1.neighbourhood)
    print(culture1.neighbourhood)
