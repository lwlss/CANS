class Fitter:

    # Can either fit different Models to data on a given Plate
    # or fit the same Model to data on different Plates
    def __init__(self, model=None, plate=None):
        self.model = model    # A Model object
        self.plate = plate    # A plate object


    # params must be correct for the Model.


    def _obj_func(self, plate, params):
        """Objective function for fitting model."""
        # Now find the amounts from simulations using the parameters.
        amounts_est = self.model.solve(plate, params)
        c_est = np.array([amounts_est[:, i*2] for i
                          in range(plate.no_cultures)]).flatten()
        err = np.sqrt(sum((plate.c_meas - c_est)**2))
        return err


    def fit_model_to_data(param_guess):
        pass


    def fit_model(plate, init_guess=None, maxiter=None):
        no_cultures = plate.no_cultures
        neighbourhood = plate.neighbourhood
        c_meas = plate.c_meas    # Flattened np.array
        obj_f = partial(obj_func, plate)
        if init_guess is None:
            init_guess = self.model.gen_params(plate)
        # All values non-negative.
        bounds = [(0.0, None) for i in range(len(init_guess))]
        if maxiter is None:
            est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                                  bounds=bounds,
                                  options={'disp': True, 'maxfun': np.inf})
        else:
            options = {'disp': True, 'maxfun': np.inf, 'maxiter': maxiter}
            est_params = minimize(obj_f, init_guess, method='L-BFGS-B',
                                  bounds=bounds, options=options)
    return est_params
