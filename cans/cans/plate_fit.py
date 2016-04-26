import numpy as np

from plate import Plate, SimPlate


times = np.linspace(0, 20, 21)
plate1 = SimPlate(3, 3, times=times)
plate1.fit_data()
