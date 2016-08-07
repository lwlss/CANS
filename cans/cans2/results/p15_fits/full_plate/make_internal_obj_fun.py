"""Find and save the objective function for just the internal cultures.

Make sure that all of the old data is also saved.

"""
import json
import numpy as np

dirs = [
    "../../results/p15_fits/full_plate/CompModel/*.json",
    "../../results/p15_fits/full_plate/CompModelBC/*.json",
]
