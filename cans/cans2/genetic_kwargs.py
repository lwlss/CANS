"""Generation of kwargs for inspyred generators and evaluators.

Includes wrapping of objects to make them pickleable for
multiprocessing.

"""
import roadrunner


from cans2.model import CompModel, CompModelBC
from cans2.plate import Plate
from cans2.fitter import Fitter
from cans2.make_sbml import create_sbml


class PickleableSWIG(object):
    # http://stackoverflow.com/a/9325185
    def __setstate__(self, state):
        print(state)
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


def make_evaluate_b_candidate_kwargs(data, model):
    """Make evalaluation kwargs for multiprocessing b_candidate evaluation.

    Corresponds to the function genetic.evaluate_b_candidate.

    data : A dictionary

    model : A pickleable CANS Model instance

    The returned dictionary should be supplied in the call to evolve
    when using the evaluate_b_candidate evaluator for
    multiprocessing. Due to the overhead of loading SBML models, a
    large number of cores (>20) may be needed before any performance
    benefit is seen.

    """
    plate = Plate(**_get_plate_kwargs(data))
    plate.data_shape = np.array([len(plate.times), plate.no_cultures*model.no_species])
    plate.rr = PickleableRoadRunner()
    mp_eval_kwargs = {
        "plate": plate,
        "fitter": Fitter(model),
        "SBML": create_sbml(plate, model, data["sim_params"]),
    }
    pickleable(mp_eval_kwargs)
    return mp_eval_kwargs
