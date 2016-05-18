import numpy as np
import json


from cans2.plotter import Plotter
from cans2.model import CompModel
from cans2.plate import Plate


rows = 5
cols = 5
guess_no = 5
# Stopping criteria: factr = 10**factr_pow
factr_pow = 0

data_file = "sim_fits/{0}x{1}_comp_model/init_guess_{2}/stop_factr_10e{3}.json"
data_file = data_file.format(rows, cols, guess_no, factr_pow)

plate = Plate(rows, cols)
model = CompModel()
plotter = Plotter(model)

# Read in data from json file
with open(data_file, 'r') as f:
    fit_data = json.load(f)

# Add necessary data attributes to produce plots

plate.times = fit_data['times']
plate.c_meas = fit_data['c_meas']    # Needed if plot_est option sim=False
plate.sim_amounts = np.array(fit_data['true_amounts'])
plate.comp_est = fit_data['est_params']

plotter.plot_est(plate, plate.comp_est, title='Estimatied Growth',
                 sim=False, legend=True)
