import numpy as np


from functools import partial
from scipy.optimize import minimize


class Fitter:
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
        # Find amounts by solving the model using the estimated parameters.
        amounts_est = self.model.solve(plate, params)
        c_est = amounts_est.flatten()[::self.model.no_species]
        err = np.sqrt(sum((plate.c_meas - c_est)**2))
        return err


    def fit_model(self, plate, param_guess=None, maxiter=None):
        assert(plate.c_meas is not None)
        obj_f = partial(self._obj_func, plate)
        if param_guess is None:
            # Fit using uniform parameters
            param_guess = self.model.gen_params(plate)
        # All values non-negative.
        bounds = [(0.0, None) for param in param_guess]
        # Add r (0, 0) bounds for empty sites according to plate.mask.
        if plate.mask is not None:
            for index in plate.mask:
                bounds[model.r_index + index] = (0.0, 0.0)
        if maxiter is None:
            est_params = minimize(obj_f, param_guess, method='L-BFGS-B',
                                  bounds=bounds,
                                  options={'disp': True, 'maxfun': np.inf})
        else:
            options = {
                'disp': True, 'maxfun': np.inf,
                'maxiter': maxiter, 'ftol': 10.0*np.finfo(float).eps
            }
            est_params = minimize(obj_f, param_guess, method='L-BFGS-B',
                                  bounds=bounds, options=options)
        return est_params
