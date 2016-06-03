import numpy as np
import copy


from functools import partial
from scipy.optimize import minimize
from scipy.interpolate import splrep, splev

from cans2.cans_funcs import dict_to_json


class GradFitter:

    def __init__(self, model=None):
        self.model = model

    def _obj_func(self, plate, params):
        pass


    # Need to do this for all cultures on the plate
    def make_grad_obj(self, plate, k=5, s=0.01):
        # k order of spline (3 for cubic). s, smoothing condition.
        splines = []
        slopes = []
        for culture in plate.cultures:
            spline_pts = splrep(culture.times, culture.c_meas, k=k, s=s)
            cul_slopes = np.maximum(0, splev(culture.times, spline_pts, der=1))
            splines.append(spline_pts)
            slopes.append(cul_slopes)
        def obj():
            # Values of gradients - b*C*N at timepoint. We are
            # optimising parameter b, have C as a measurement, but
            # what about N?
            pass
        return obj

    def fit_model(self, plate):
        pass


if __name__ == "__main__":
    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter

    sim_params = {
        "C_0": 1e-5,
        "N_0": 0.1,
        "kn": 2.0
    }
    plate = Plate(3, 3)
    plate.times = np.linspace(0, 5, 11)
    plate.set_sim_data(CompModel(), r_mean=40.0, r_var=15.0,
                       custom_params=sim_params, noise=True)

    # Spline each culture
    grad_fitter = GradFitter(CompModel())
    obj = grad_fitter.make_grad_obj(plate)
