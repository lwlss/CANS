import numpy as np
import copy
# import time

from functools import partial
from scipy.optimize import minimize


from cans2.cans_funcs import dict_to_json


class Fitter(object):
    # Can either fit different Models to data on a given Plate or fit
    # the same Model to data on different Plates. It is more natural
    # that we will want to fit different Models to the same data. I
    # choose to give the Model to the fitter in init to set up inde
    # and comp fitter instances which can be used with various Plates.
    def __init__(self, model=None):
        self.model = model    # A Model object


    # params must be correct for the Model.
    def _obj_func(self, plate, params):
        """Objective function for fitting model."""
        # Scale C_0 back to actual amount here.
        params[0] = params[0]/10000
        # Find amounts by solving the model using the estimated parameters.
        amount_est = self.model.solve(plate, params, plate.times)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = np.split(amount_est, self.model.no_species, axis=1)[0].flatten()
        # Zeros appear in here for empty plates but this shouldn't
        # have any effect.
        err = np.sqrt(np.sum((plate.c_meas - c_est)**2))
        return err


    def _rr_obj(self, plate, params):
        """Return the objective function from RoadRunner simulations.

        The C_0 parameter is scaled to the "true" value for solving. A
        scaled C_0 is used for the minimizer so that absolute parmeter
        values are reasonably close.

        The solver returns amounts for all species on the plate. There
        is an alternative method which just returns a user defined
        selection. params includes init amounts.

        """
        params[0] = params[0]/10000
        # There are multiple alternative Model methods for solving
        # using RoadRunner. The specific method is stored as a
        # Model attribute rr_solver.
        amount_est = self.model.rr_solve(plate, params)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = np.split(amount_est, self.model.no_species, axis=1)[0]
        # CONSIDER WHEN REFACTORING. It will probably quicker to
        # remove the cell reaction equations for empty cultures from
        # the SMBL rather than setting b=0 and slicing out. Then, cell
        # amounts will not be returned by rr_solve for empty cultures
        # and we do not have to slice by the indices of all of the
        # growers. Instead we would slice as c_est[:,
        # :len(plate.growers)].
        growers_c_est = c_est[:, list(plate.growers)].flatten()
        err = np.sqrt(np.sum((plate.c_meas_obj - growers_c_est)**2))
        return err


    def _rr_obj_spline(self, plate, params):
        """Return the objective function from RoadRunner simulations.

        Solves using splines values at even timespteps. Quicker for
        data with many timepoints.

        The C_0 parameter is scaled to the "true" value for solving. A
        scaled C_0 is used for the minimizer so that absolute parmeter
        values are reasonably close.

        The solver returns amounts for all species on the plate. There
        is an alternative method which just returns a user defined
        selection. params includes init amounts.

        """
        params[0] = params[0]/10000
        # There are multiple alternative Model methods for solving
        # using RoadRunner. The specific method is stored as a
        # Model attribute rr_solver.
        amount_est = self.model.rr_solve_spline(plate, params)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = np.split(amount_est, self.model.no_species, axis=1)[0]
        growers_c_est = c_est[:, list(plate.growers)].flatten()
        err = np.sqrt(np.sum((plate.c_meas_obj_spline - growers_c_est)**2))
        return err


    def _rr_obj_no_scaling(self, plate, params):
        """Return the objective function from RoadRunner simulations.

        C_0 parameters are not scaled.

        The solver returns amounts for all species on the plate. There
        is an alternative method which just returns a user defined
        selection. params includes init amounts.

        """
        # There are multiple alternative Model methods for solving
        # using RoadRunner. The specific method is stored as a
        # Model attribute rr_solver.
        amount_est = self.model.rr_solve(plate, params)
        c_est = np.split(amount_est, self.model.no_species, axis=1)[0].flatten()
        err = np.sqrt(np.sum((plate.c_meas - c_est)**2))
        return err


    # TODO. Better to make this more general by returning C and N and
    # splitting and using rr_solver. Also have to rename sel_shape and
    # data_shape to the same name.
    def _rr_selection_obj(self, plate, params):
        """Return the objective function from RoadRunner simulations.

        The solver returns C amounts from a user defined selection of
        cultures. These are set by the Plate method
        set_rr_selections. params includes init amounts.

        """
        params[0] = params[0]/10000
        c_est = self.model.rr_solve_selections(plate, params)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        err = np.sqrt(np.sum((plate.c_meas_sel - c_est)**2))
        return err


    def _neigh_obj_func(self, plate, params):
        """Obj fun for arbitrary neighbour model.

        Must be treated differently because not all growing cultures
        have cell observations.

        """
        params[0] = params[0]/10000
        # Find amounts by solving the model using the estimated parameters.
        amounts_est = self.model.solve(plate, params, plate.times)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = amounts_est.flatten()[::self.model.no_species]
        c_est = c_est[1::3]    # Only the middle culture
        err = np.sqrt(np.sum((plate.c_meas - c_est)**2))
        return err


    def fit_spline(self, plate, param_guess, bounds, minimizer_opts):
        """Fit a spline using the RoadRunner solver."""
        param_guess = copy.deepcopy(param_guess)
        bounds = copy.deepcopy(bounds)

        obj_f = partial(self._rr_obj_spline, plate)

        # Add b (0, 0) bounds for empty sites according to plate.empties.
        if len(plate.empties) != 0:
            bounds[list(np.array(plate.empties) + self.model.b_index)] = np.array([0.0, 0.0])

        options = {
            # 'disp': True,
            'maxfun': np.inf,
            # 'maxcor': 20,
            # 'eps': 1e-06,
            'maxls': 20,    # max line searches per iter.
            #'ftol': 10.0*np.finfo(float).eps
        }

        if minimizer_opts is not None:
            options.update(minimizer_opts)

        # Scale C_0 for the minmizer. Also have to scale upper and
        # lower C bounds.
        param_guess[0] = param_guess[0]*10000
        bounds[0] = np.array([bounds[0][i]*10000 if bounds[0][i] is not None
                              else bounds[0][i] for i in range(2)])

        est_params = minimize(obj_f, param_guess, method='L-BFGS-B',
                              bounds=bounds, options=options)

        # Scale C_0 to true amount in result.
        est_params.x[0] = est_params.x[0]/10000

        # Add extra attributes to scipy.optimize.OptimizeResult
        # object. Can access with keys() as this is just a subclass of
        # dict.
        est_params.init_guess = param_guess
        est_params.fit_options = dict_to_json(options)    # including ftol
        est_params.model = self.model
        est_params.bounds = bounds
        est_params.method = 'L-BFGS-B'
        return est_params


    def fit_model(self, plate, param_guess=None, bounds=None,
                  rr=False, sel=False, minimizer_opts=None):
        """Fit the model to data on the plate.

        If passed use param guess as the initial guess for
        minimization, else generate a uniform guess. minimizer_opts
        should be a dictionary. Commmon options to set are ftol and
        maxiter.

        Bounds should be passed in as a full list of tuples with
        correct position for the model according to Fitter.model (a
        Model instance) params attribute. Individual bounds must be
        included at the end for each b parameter.

        If rr is true, solve using RaodRunner (faster).

        If sel is True, use only cell amounts from a selection of
        cultures in the objective function. These can be set with the
        Plate method set_rr_selections.

        """
        # Make deep_copies of param_guesses and bounds because of
        # rescaling for the minimizer.
        param_guess = copy.deepcopy(param_guess)
        bounds = copy.deepcopy(bounds)

        assert(plate.c_meas is not None)
        if self.model.name == "Neighbour model":
            obj_f = partial(self._neigh_obj_func, plate)
        elif rr and sel:
            obj_f = partial(self._rr_selection_obj, plate)
        elif rr and not sel:
            obj_f = partial(self._rr_obj, plate)
        elif not rr and sel:
            raise ValueError("Can only make a selection if rr=True")
        else:
            # odeint solver.
            obj_f = partial(self._obj_func, plate)

        if param_guess is None:
            # Fit using uniform parameters
            param_guess = self.model.gen_params(plate)
        else:
            assert len(param_guess) == self.model.b_index + plate.no_cultures

        if bounds is None:
            # All values non-negative.
            bounds = [(0.0, None) for param in param_guess]

        # Add b (0, 0) bounds for empty sites according to plate.empties.
        if len(plate.empties) != 0:
            bounds[list(np.array(plate.empties) + self.model.b_index)] = np.array([0.0, 0.0])

        options = {
            # 'disp': True,
            'maxfun': np.inf,
            # 'maxcor': 20,
            # 'eps': 1e-06,
            'maxls': 20,    # max line searches per iter.
            #'ftol': 10.0*np.finfo(float).eps
        }

        if minimizer_opts is not None:
            options.update(minimizer_opts)

        # Scale C_0 for the minmizer. Also have to scale upper and
        # lower C bounds.
        param_guess[0] = param_guess[0]*10000
        bounds[0] = tuple(bounds[0][i]*10000 if bounds[0][i] is not None
                          else bounds[0][i] for i in range(2))

        est_params = minimize(obj_f, param_guess, method='L-BFGS-B',
                              bounds=bounds, options=options)

        # Scale C_0 to true amount in result.
        est_params.x[0] = est_params.x[0]/10000

        # Add extra attributes to scipy.optimize.OptimizeResult
        # object. Can access with keys() as this is just a subclass of
        # dict.
        est_params.init_guess = param_guess
        est_params.fit_options = dict_to_json(options)    # including ftol
        est_params.model = self.model
        est_params.bounds = bounds
        est_params.method = 'L-BFGS-B'
        return est_params
