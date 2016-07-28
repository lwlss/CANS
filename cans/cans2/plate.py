import numpy as np
import copy
import random
import sys
# RoadRunner is not yet availible in Python3. You can still use
# methods which call SciPy's odeint solver.
if sys.version_info[0] == 2:
    import roadrunner
# import time


from scipy import interpolate


from cans2.model import IndeModel
from cans2.fitter import Fitter
from cans2.cans_funcs import get_mask
from cans2.make_sbml import create_sbml


def sim_a_plate(rows, cols, times, model, params, noise=False):
    """Simulate timecourses for and return a Plate."""
    plate = Plate(rows, cols)
    plate.times = times
    plate.sim_params = params
    # set_sim_data also sets rr_model with the simulated params.
    plate.set_sim_data(model, noise=noise)
    return plate


class BasePlate(object):
    def __init__(self, rows, cols, data=None):
        """Instantiate BasePlate.

        rows and cols give the dimensions of cultures on the plate.

        If provided, data should be in a dictionary with the following
        keys.

        "c_meas" : Values for cell measurements.
            A flat np.array with zero observation values added for
            empty spots. Order C0(t=t0), C1(t=t0), ..., C0(t=t1),
            C1(t=t1),... .

        "times" : np.array of observation times in units days.

        "empties" : Locations of empty cultures (optional).
            Locations are integers from zero to (rows*cols - 1) with
            the culture array flattened in row-major style e.g. for a
            2x2 plate (0, 0), (0, 1), (1, 0), (1, 1) corresponds to
            cultures [0, 1, 2, 3]

        """
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.find_neighbourhood()
        self.edges = np.array([i for i, ns in enumerate(self.neighbourhood)
                               if len(ns) != 4])
        self.internals = np.array([i for i, neighs in enumerate(self.neighbourhood)
                                   if len(neighs) == 4])
        self.data = data
        if data is not None:
            self.c_meas = data['c_meas']
            self.times = data['times']
            self.empties = data['empties']    # List of indices of empty sites
            self.growers = np.array([i for i in range(self.no_cultures)
                                     if i not in self.empties])
            try:
                self.genes = data['genes']
            except KeyError:
                self.genes = []
        else:
            self.c_meas = None
            self.times = None
            self.empties = []
        # create c_meas_obj
        if len(self.empties) != 0:
            c_meas_a = np.array(self.c_meas)
            c_meas_a.shape = (len(self.times), self.no_cultures)
            self.c_meas_obj = c_meas_a[:, list(self.growers)].flatten()
        else:
            self.c_meas_obj = self.c_meas
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
        self.neigh_nos = np.array([len(tup) for tup in neighbourhood])
        self.mask = get_mask(neighbourhood)
        return neighbourhood


    def set_rr_model(self, model, params, outfile=""):
        """Set RoadRunner object for the model.

        model: A CANS Model instance.
        params: A list of parameters for the CANS model.

        If outfile is given the SBML model will also be saved.
        """
        # Set a shape to initailize an empty np array when using
        # Model.solve(). Do it here rather than repeatedly in the
        # function.
        self.data_shape = (len(self.times), self.no_cultures*model.no_species)
        self.rr = roadrunner.RoadRunner(create_sbml(self, model,
                                                    params, outfile))


    # Does not require a 2nd set_rr method, just a solve.
    def make_spline(self, time_points=15):
        """Spline the data in even timesteps.

        timepoints : (int) Number of timepoints to use for spline.

        Sets self.t_spline, self.c_spline, and self.c_meas_obj_spline.
        self.c_meas_obj_spline is c_spline with empty cultures
        removed.

        """
        c_spline = []
        for culture in self.cultures:
            c = culture.c_meas
            tck = interpolate.splrep(self.times, c, k=5, s=1.0)
            t_new = np.linspace(0, self.times[-1], time_points)
            c_new = np.maximum(0.0, interpolate.splev(t_new, tck, der=0))
            c_spline.append(c_new)
        self.t_spline = t_new
        c_spline = np.array(c_spline).flatten(order="F")
        self.c_spline = c_spline
        # Set c_meas_obj_spline for only the growers (i.e. remove empties)
        c_array = np.array(c_spline)
        c_array.shape = (len(self.t_spline), self.no_cultures)
        self.c_meas_obj_spline = c_array[:, list(self.growers)].flatten()


    def rr_solve_spline(self):
        """Simulate for splined times with even timesteps."""
        sol = self.rr.simulate(self.t_spline[0], self.t_spline[-1],
                               len(self.t_spline)-1, reset=True,
                               absolute=1.49012e-8,
                               relative=1.49012e-8,
                               mininumTimeStep=1.0e-8,
                               maximumNumSteps=40000)
        return sol[:, 1:]


    # This, and more importantly fitting, could be made even faster if
    # we return only c_meas in a flattened array. We could just use
    # the slower odeint solver when we want nutrients or a 2nd version
    # of this function with an extra argument. It is easier to write
    # new sbml models than the equivilant python so the latter option
    # should be preferred. I tried to do this with the selections
    # method below (i.e. passing a sel argument to simulate) and it
    # was in fact slower. Slicing only to end of C in the for loop may
    # be faster but probably not by much.
    def rr_solve(self):
        """Solve SBML model between timepoints using roadrunner.

        Returns an 2d array of times x species. Species are
        of order e.g., [C0, C1,..., N0, N1,...] with numbers indicating
        culture index.
        """
        # Reset species amounts to init values. Do this here rather
        # than after the simulation because it is possible that rr has
        # been accessed and simulated elsewhere. Outside the below
        # loop it never occurs that I want to carry over species
        # amounts between simulations so it may also be wise to reset
        # rr before this function call returns but I leave it free for
        # now.
        self.rr.reset()
        a = np.empty(self.data_shape)
        # Set init values in result.
        a[0] = self.rr.model.getFloatingSpeciesInitAmounts()
        for i, t0, t1 in zip(range(len(self.times)),
                             self.times[:-1], self.times[1:]):
            # Solves using SUNDIALS CVODE with MXSTEP_DEFAULT=500. I
            # set minimumTimeStep at about minute resolution for a
            # simulation over 5 days (i.e. 1/(5*24*60)) and
            # maximumNumSteps greater than 5/minimumTimeStep so that
            # it should never be encountered in a typical
            # experiment. absolute and relative are set to the same
            # values used by Scipy's odeint.
            a[i+1] = self.rr.simulate(t0, t1, 1,
                                      absolute=1.49012e-8,    # Affects speed and accuracy.
                                      relative=1.49012e-8,
                                      mininumTimeStep=1.0e-8,
                                      maximumNumSteps=40000)[1][1:]
        return a


    def fit_spline(self, model, param_guess, bounds, minimizer_opts=None):
        fitter = Fitter(model)
        est = fitter.fit_spline(self, param_guess, bounds, minimizer_opts)
        return est


    def fit_model(self, model, param_guess=None, bounds=None,
                  rr=False, sel=False, minimizer_opts=None):
        """Return estimates from fitting model to plate.

        param_guess : List of initial parameter guesses.

        bounds : List of tuples for lower and upper parameter bounds.

        rr : True to use roadrunner solver.

        sel : True to use a selection of cultures in the objective function.

        minimizer_opts : Options for scipy.optimize.minimize fitter.
        """
        fitter = Fitter(model)
        est = fitter.fit_model(self, param_guess=param_guess,
                               bounds=bounds, rr=rr, sel=sel,
                               minimizer_opts=minimizer_opts)
        return est


class Plate(BasePlate):
    def __init__(self, rows, cols, data=None):
        super(Plate, self).__init__(rows, cols, data)
        self.cultures = [Culture() for i in range(self.no_cultures)]
        if self.data is not None:
            self._set_cultures()


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


    def _gen_sim_params(self, model, b_mean, b_var, custom_params):
        """Generate a set of simulation parameters for a model."""
        # There is a bug here if model instance is being used
        # somewhere else then plate fails to be passed.
        self.sim_params = model.gen_params(self, mean=b_mean, var=b_var)
        if custom_params is not None:
            for k, v in custom_params.items():
                try:
                    index = model.params.index(k)
                    self.sim_params[index] = v
                except ValueError:
                    print("No plate level {0} in {1}.".format(k, model.name))
                    raise
        # Set b params for zero for empty plates. Could also go with nan.
        for index in self.empties:
            self.sim_params[model.b_index+index] = 0.0


    def set_sim_data(self, model, b_mean=1.0, b_var=1.0,
                     custom_params=None, noise=True):
        """Set simulation data.

        If sim_params attribute does not exist one will be
        generated. This option is to allow the use of simulation
        parameters loaded from file.

        """
        if self.sim_params is None:
            self._gen_sim_params(model, b_mean, b_var, custom_params)
        self.set_rr_model(model, self.sim_params)
        self.sim_amounts = model.rr_solve(self, self.sim_params)
        self.c_meas = np.split(self.sim_amounts, model.no_species, axis=1)[0].flatten()
        if noise:
            self.add_noise()
        self._set_cultures()    # Set culture c_meas and times.


    # Easier ways of doing this with numpy. See Conor's feedback from
    # code review.
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


    def rr_solve_selections(self):
        """Solve for selected species between timepoints using roadrunner.

        Returns a flattened array ready for the objective function.
        """
        # Reset species amounts to init values.
        self.rr.reset()
        a = np.empty(self.sel_shape)
        a[0] = self.rr.model.getFloatingSpeciesInitAmounts()[self.selection_inds]
        for i, t0, t1 in zip(range(len(self.times)),
                             self.times[:-1], self.times[1:]):
            # Solves using SUNDIALS CVODE with MXSTEP_DEFAULT=500. I
            # set minimumTimeStep at about minute resolution for a
            # simulation over 5 days (i.e. 1/(5*24*60)) and
            # maximumNumSteps greater than 5/minimumTimeStep so that
            # it should never be encountered in a typical experiment.
            # I would like to have set rr.timeCourseSelections just
            # once to return the species I want but the API does not
            # seem to work like the documentation. Therefore just pass
            # the selections using the sel argument.
            a[i+1] = self.rr.simulate(t0, t1, 1,
                                      mininumTimeStep=1.39e-4,
                                      maximumNumSteps=40000,
                                      sel=self.timeCourseSelections)[1]
        return a.flatten()


    def set_rr_selections(self, id="[C{0}]", indices="internals"):
        """Set the return C amount indices for RoadRunner simulations.

        At the moment we only ever want to set this for C amounts. The
        intended use is to eliminate edge cultures from the objective
        function. If we want to select other species it will suffice
        to solve for all species and then index the output as speed is
        not important.

        ids: Id of cells in SBML model with positional references for
        formatting of indices of the selected cultures.

        indices: list of culture indices.
        """
        if indices == "internals":
            indices = self.internals
            self.selection_inds = self.internals    # Should be a numpy array
        else:
            self.selection_inds = np.array(indices)
        selections = [id.format(i) for i in indices]
        # For some reason RoadRunner's timeCourseSelections API is not
        # working (maybe I have an older verion or could have been an
        # issue with swig version on installation) so just set
        # timeCourseSelections as a Plate attribute and fix in future
        # if possible/needed by changing to a RoadRunner attribute and
        # altering the argument in call to rr.simulate in the method
        # Plate.rr_solve_selections. i.e. change below to
        # self.rr.timesCourseSelections and remore sel attr from
        # simulate.
        self.timeCourseSelections = selections
        # Set a shape for simulated timecourse arrays.
        self.sel_shape = (len(self.times), len(selections))
        # Set c_meas_sel for objective function evaluations.
        c_sels = [self.c_meas[i::self.no_cultures] for i in indices]
        self.c_meas_sel = np.array(c_sels).flatten(order="F")


class Culture(BasePlate):
    def __init__(self, data=None):
        super(Culture, self).__init__(1, 1, data)


if __name__ == '__main__':
    import roadrunner

    from cans2.cans_funcs import get_mask
    from cans2.model import CompModel
    from cans2.plotter import Plotter

    comp_model = CompModel()
    comp_plotter = Plotter(comp_model)

    plate1 = Plate(2, 2)
    plate1.times = np.linspace(0, 5, 11)

    print("edges", plate1.edges)

    true_params = {'N_0': 0.1, 'kn': 0.1}
    true_params['C_0'] = true_params['N_0']/1000000
    plate1.set_sim_data(comp_model, b_mean=50.0, b_var=15.0,
                        custom_params=true_params)

    comp_plotter.plot_c_meas(plate1)

    plate1.set_rr_model(comp_model, plate1.sim_params)
    # plate1.set_rr_selections(indices="internals")
    plate1.est = plate1.fit_model(comp_model, minimizer_opts={"disp": True},
                                  rr=True, sel=False)
    print(plate1.est.x)
    print(plate1.sim_params)
    print(plate1.c_meas)

    comp_plotter.plot_est(plate1, plate1.est.x, sim=True)
