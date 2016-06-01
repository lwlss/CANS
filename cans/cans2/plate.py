import numpy as np
import copy
import random


from cans2.model import IndeModel
from cans2.fitter import Fitter


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
            # c_measn should be a flat np.array with zero observation
            # values added for empty spots
            self.c_meas = data['c_meas']
            self.times = data['times']
            self.empties = data['empties']    # List of indices of empty sites
        else:
            self.c_meas = None
            self.times = None
            self.empties = []
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


    def fit_model(self, model, param_guess=None, minimizer_opts=None,
                  bounds=None):
        """Return estimates from fitting model to plate."""
        fitter = Fitter(model)
        est = fitter.fit_model(self, param_guess, minimizer_opts, bounds)
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


    def _set_cultures(self):
        """Add plate level simulation data to Cultures."""
        for i, culture in enumerate(self.cultures):
            # May need to pass the model used in order to
            # generalize. Then we can also provide parameters used for
            # the simulations and other amounts (e.g. N). We can also
            # use model.no_species. This is not possible with real
            # data and not really necessary with simulated data.
            culture.c_meas = self.c_meas[i::self.no_cultures]
            culture.times = self.times
            if i in self.empties:
                culture.empties = [0]


    def _gen_sim_params(self, model, r_mean, r_var, custom_params):
        """Generate a set of simulation parameters for a model."""
        # There is a bug here if model instance is being used
        # somewhere else then plate fails to be passed.
        self.sim_params = model.gen_params(self, mean=r_mean, var=r_var)
        if custom_params is not None:
            for k, v in custom_params.items():
                try:
                    index = model.params.index(k)
                    self.sim_params[index] = v
                except ValueError:
                    print("No plate level {0} in {1}.".format(k, model.name))
                    raise
        # Set r params for zero for empty plates. Could also go with nan.
        for index in self.empties:
            self.sim_params[model.r_index+index] = 0.0


    def set_sim_data(self, model, r_mean=1.0, r_var=1.0,
                     custom_params=None, noise=True):
        """Set simulation data.

        If sim_params attribute does not exist one will be
        generated. This option is to allow the use of simulation
        parameters loaded from file.

        """
        if self.sim_params is None:
            self._gen_sim_params(model, r_mean, r_var, custom_params)
        self.sim_amounts = model.solve(self, self.sim_params)
        self.c_meas = np.split(self.sim_amounts, model.no_species, axis=1)[0].flatten()
        if noise:
            self.add_noise()
        self._set_cultures()    # Set culture c_meas and times.



    def add_noise(self, sigma=None):
        """Add random noise to c_meas."""
        # Find a scale
        if sigma is None:
            max_c = max(self.c_meas)
            sigma = max_c*0.025
        if not isinstance(self.c_meas, np.ndarray):
            noisey = np.asarray(copy.deepcopy(self.c_meas), dtype=np.float64)
        else:
            noisey = copy.deepcopy(self.c_meas)
        for x in np.nditer(noisey, op_flags=['readwrite']):
            x[...] = x + random.gauss(0, sigma)
        np.maximum(0, noisey, out=noisey)
        self.c_meas = noisey


    def est_from_cultures(self):
        """Estimate parameters from inde fits of individual Cultures.

        Set idependent estimates (with scipy.integrate.odeint data) as
        culture attribute inde_est and return averaged values. Also
        set the average as the plate attribute avg_culture_ests.

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
        if np.all(np.isnan(avgs)):
            print("Warning: All rs were zero so estimates may not be reliable.")
            avgs = np.average(params, axis=0)
        # Averages only for plate level params.
        avg_params = np.append(avgs[:inde_model.r_index],
                               params[:, inde_model.r_index])
        self.avg_culture_ests = avg_params
        return avg_params



class Culture(BasePlate):
    def __init__(self, data=None):
        super(Culture, self).__init__(1, 1, data)


if __name__ == '__main__':
    plate1 = Plate(3, 3)
    culture1 = Culture()
    print(plate1.neighbourhood)
    print(culture1.neighbourhood)
