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
        # Generalized using Model.species attribute
        c_est = np.array([amounts_est[:, i*len(self.model.species)] for i
                          in range(plate.no_cultures)]).flatten()
        err = np.sqrt(sum((plate.c_meas - c_est)**2))
        return err


    def fit_model(self, plate, param_guess=None, maxiter=None):
        obj_f = partial(self._obj_func, plate)
        if param_guess is None:
            # Fit using uniform parameters
            param_guess = self.model.gen_params(plate)
        # All values non-negative.
        bounds = [(0.0, None) for param in param_guess]
        if maxiter is None:
            est_params = minimize(obj_f, param_guess, method='L-BFGS-B',
                                  bounds=bounds,
                                  options={'disp': True, 'maxfun': np.inf})
        else:
            options = {'disp': True, 'maxfun': np.inf, 'maxiter': maxiter}
            est_params = minimize(obj_f, param_guess, method='L-BFGS-B',
                                  bounds=bounds, options=options)
        return est_params
