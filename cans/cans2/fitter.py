import numpy as np
import copy


from functools import partial
from scipy.optimize import minimize
# from scipy.interpolate import splrep, splev

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
        # Scale C_0 back to actual amount here. Lists are mutable!
        # Probably faster to operate on the zero index twice than to
        # deepcopy the entire list.
        # params = copy.deepcopy(params)
        params[0] = params[0]/10000
        # Find amounts by solving the model using the estimated parameters.
        amount_est = self.model.solve(plate, params)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = np.split(amount_est, self.model.no_species, axis=1)[0].flatten()
        # Zeros appear in here for empty plates but this shouldn't
        # have any effect.
        err = np.sqrt(np.sum((plate.c_meas - c_est)**2))
        return err


    # We can also select to return only C from the rr_solver to make
    # this faster.
    def _rr_obj(self, plate, params):
        # Find amounts by solving the roadrunner sbml model using the
        # estimated parameters (including init amounts).
        params[0] = params[0]/10000
        # Need to supply params to the sbml roadrunner model.
        amount_est = self.model.rr_solve(plate, params)
        # plate.rr.reset()    # Do I need to reset?
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = np.split(amount_est, self.model.no_species, axis=1)[0].flatten()
        # Zeros appear in here for empty plates but this shouldn't
        # have any effect.
        err = np.sqrt(np.sum((plate.c_meas - c_est)**2))
        return err


    def _neigh_obj_func(self, plate, params):
        """Obj fun for arbitrary neighbour model.

        Must be treated differently because not all growing cultures
        have cell observations.

        """
        params[0] = params[0]/10000
        # Find amounts by solving the model using the estimated parameters.
        amounts_est = self.model.solve(plate, params)
        # Mutable so must scale C_0 back
        params[0] = params[0]*10000
        c_est = amounts_est.flatten()[::self.model.no_species]
        c_est = c_est[1::3]    # Only the middle culture
        err = np.sqrt(np.sum((plate.c_meas - c_est)**2))
        return err


    def fit_model(self, plate, param_guess=None, custom_options=None,
                  bounds=None, rr=False):
        """Fit the model to data on the plate.

        If passed use param guess as the initial guess for
        minimization, else generate a uniform guess. custom_options
        should be a dictionary. Commmon options to set are ftol and
        maxiter.

        Bounds should be passed in as a full list of tuples with
        correct position for the model according to
        model.params. Individual bounds must be included at the end
        for each r parameter.

        """
        # Make deep_copies of param_guesses and bounds because of
        # rescaling for the minimizer and mutability.
        param_guess = copy.deepcopy(param_guess)
        bounds = copy.deepcopy(bounds)

        assert(plate.c_meas is not None)
        if self.model.name == "Neighbour model":
            obj_f = partial(self._neigh_obj_func, plate)

        if rr:
            obj_f = partial(self._rr_obj, plate)
        else:
            obj_f = partial(self._obj_func, plate)
        if param_guess is None:
            # Fit using uniform parameters
            param_guess = self.model.gen_params(plate)
        else:
            assert(len(param_guess) == self.model.r_index + plate.no_cultures)

        if bounds is None:
            # All values non-negative.
            bounds = [(0.0, None) for param in param_guess]

        # Add r (0, 0) bounds for empty sites according to plate.empties.
        for index in plate.empties:
            bounds[self.model.r_index + index] = (0.0, 0.0)

        options = {
            # 'disp': True,
            'maxfun': np.inf,
            #'ftol': 10.0*np.finfo(float).eps
        }
        if custom_options is not None:
            options.update(custom_options)

        # Scale C_0 for the minmizer. Also have to scale the bounds.
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
