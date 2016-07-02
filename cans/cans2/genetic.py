import numpy as np
from cans2.plate import Plate


# Simulate a small plate 3x3 using CompModelBC or CompModel with noise.
# Construct a genetic algorithm to solve.

rows = 3
cols = 3
times = np.linspace(0, 5, 11)
plate = Plate(rows, cols)
plate.times = times
