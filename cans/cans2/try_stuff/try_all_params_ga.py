import time
import json
import numpy as np


from cans2.cans_funcs import dict_to_numpy
from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.genetic2 import evolver, custom_evolver, mp_evolver, gen_random_uniform, evaluate_b_candidate, evaluate_b_candidates
from cans2.genetic_kwargs import PickleableCompModelBC, make_evaluate_b_candidate_kwargs, make_evaluate_b_candidates_kwargs, _get_plate_kwargs
