"""Generation of kwargs for inspyred generators and evaluators.

Includes wrapping of objects to make them pickleable for
multiprocessing.

"""
import numpy as np
import roadrunner


from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.fitter import Fitter
from cans2.make_sbml import create_sbml
from cans2.cans_funcs import pickleable


class PickleableSWIG(object):
    # http://stackoverflow.com/a/9325185
    def __setstate__(self, state):
        self.__init__(*state['args'])

    def __getstate__(self):
        return {'args': self.args}


class PickleableRoadRunner(roadrunner.RoadRunner, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        roadrunner.RoadRunner.__init__(self)


class PickleableCompModel(CompModel, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        CompModel.__init__(self)


class PickleableCompModelBC(CompModelBC, PickleableSWIG):
    # http://stackoverflow.com/a/9325185
    def __init__(self, *args):
        self.args = args
        CompModelBC.__init__(self)


def _get_plate_kwargs(dct):
    """Create plate making kwargs from a dictionary of data.

    dct : A dictionary containing, possibly amongst other things, key
    value pairs required for instantiating a Plate object.

    Return the dictionary plate_kwargs to be called with
    Plate(**plate_kwargs).

    """
    try:
        dct["empties"]
    except KeyError:
        dct["empties"] = []
    plate_kwargs = {
        "rows": dct["rows"],
        "cols": dct["cols"],
        "data": {
            "times": dct["times"],
            "c_meas": dct["c_meas"],
            "empties": dct["empties"],
        },
    }
    return plate_kwargs


# def make_gen_b_candidate_kwargs(b_bound):
#     """Return kwargs for generating random uniform b candidates.

#     Expected to be used with the function gen_random_uniform.

#     b_bound : [lower_bound, upper_bound].

#     """
#     gen_kwargs = {
#         "bounds": [b_bound for i in plate.no_cultures]
#         }
#     return gen_kwargs


def make_eval_b_candidate_kwargs(data, model, plate_lvl):
    """Make evalaluation kwargs for multiprocessing b_candidate evaluation.

    Corresponds to the function genetic.eval_b_candidate.

    data : A dictionary

    model : A pickleable CANS Model instance.

    plate_lvl : An array of plate level parameters.

    The returned dictionary should be supplied in the call to evolve
    when using the eval_b_candidate evaluator for
    multiprocessing. Due to the overhead of loading SBML models, a
    large number of cores (>20) may be needed before any performance
    benefit is seen.

    """
    plate = Plate(**_get_plate_kwargs(data))
    plate.data_shape = np.array([len(plate.times),
                                 plate.no_cultures*model.no_species])
    plate.rr = PickleableRoadRunner()
    eval_kwargs = {
        "plate": plate,
        "fitter": Fitter(model),
        "sbml": create_sbml(plate, model, data["sim_params"]),
        "plate_lvl": plate_lvl,
    }
    return eval_kwargs


def make_eval_b_candidates_kwargs(data, model, plate_lvl):
    """Make evalaluation kwargs for in serial b_candidate evaluation.

    Corresponds to the function genetic.eval_b_candidates. The
    returned values in the dict eval_kwargs need not be pickleable.

    data : A dictionary

    model : A CANS Model instance.

    plate_lvl : An array of plate level parameters.

    The returned dictionary should be supplied in the call to evolve
    when using the eval_b_candidates evaluator for serial
    processing.

    """
    plate = Plate(**_get_plate_kwargs(data))
    no_params = len(plate_lvl) + plate.no_cultures
    plate.set_rr_model(model, np.ones(no_params))    # Dummy params
    eval_kwargs = {
        "plate": plate,
        "fitter": Fitter(model),
        "plate_lvl": plate_lvl,
    }
    return eval_kwargs


def make_eval_candidates_kwargs(data, model):
    """Make evalaluation kwargs for in serial parameter candidate evaluation.

    Corresponds to the function genetic.eval_candidates. The returned
    values in the dict eval_kwargs need not be pickleable.

    data : A dictionary

    model : A CANS Model instance.

    The returned dictionary should be supplied in the call to evolve
    when using the eval_candidates evaluator for serial processing.

    """
    plate = Plate(**_get_plate_kwargs(data))
    no_params = model.b_index + plate.no_cultures
    plate.set_rr_model(model, np.ones(no_params))    # Dummy params
    eval_kwargs = {
        "plate": plate,
        "fitter": Fitter(model),
    }
    return eval_kwargs


def make_eval_plate_lvl_kwargs(data, model, c_evolver):
    """Make eval kwargs for plate level parallel parameter candidate evaluaton.

    Corresponds to the function genetic.eval_plate_lvl.

    model : A Pickleable CANS model.

    c_evolver : A dictionary containing the culture level evolver
    function (key "evolver") and kwargs for this function as a nested
    dictionary (key "evolver_kwargs"). The culture level "args"
    argument must be created inside the genetic.eval_plate_lvl
    function call because it will contain the unpickleable
    objects. Instead, just leave it out or supply None.

    """
    pickleable(model)    # Model must be pickleable for multiprocessing.
    plate_data = {
        "rows": data["rows"],
        "cols": data["cols"],
        "times": data["times"],
        "c_meas": data["c_meas"],
        "empties": data["empties"],
    }
    eval_kwargs = {
        # To go to the function make_eval_b_candidates_kwargs.
        "c_lvl_make_kwargs_kwargs": {
            "data": plate_data,
            "model": model,    # Must be pickleable
            "plate_lvl": None,    # Must be set as candidate inside evaluator.
            },
        "c_evolver": c_evolver,    # Also containes b_bounds.
    }
    return eval_kwargs


def package_evolver(evolver, **kwargs):
    """Package an evolver function and kwargs in a dictinoary.

    Of use in heirarchical evolution. When multiprocessing is used,
    unpickleable kwargs must be added later inside evaluators
    (useually in "args").

    evolver : An evolver function.

    kwargs : key word arguments for the evolver function.

    """
    evolver_dct = {
        "evolver": evolver,    # An evolver function
        "evolver_kwargs": kwargs,    # Must also add args in the p level evaluator.
    }
    return evolver_dct


def make_eval_plate_lvl_im_neigh_grad_kwargs(data, model, b_bound):
    """Make eval kwargs for plate level parallel parameter candidate evaluaton.

    Corresponds to the function genetic.eval_plate_lvl_im_neigh_grad.

    data : dictionary

    model : A Pickleable CANS model.

    b_bound : bound for gradient fitting of b parameters. e.g. [0.0, 100.0].

    """
    pickleable(model)    # Model must be pickleable for multiprocessing.
    plate = Plate(**_get_plate_kwargs(data))
    eval_kwargs = {
        "plate": plate,
        "model": model,
        # Not including amounts. Last two are place holders for
        # b_guess*1.5 and b_guess.
        "imag_neigh_params": np.array([1.0, 1.0, 0.0, 0.0, 0.0]),
        "b_bounds": np.array([b_bound for c in range(plate.no_cultures)]),
    }
    return eval_kwargs
