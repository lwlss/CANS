import csv
import numpy as np
import json

from cans import find_neighbourhood
import inde

from fitting import calc_devs

# Read in same 16x24 data as before for kn=0
# This time use stricter stopping criteria for independent model.
rows = 16
cols = 24
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)
dir_name = 'results/comp_sim_fits_vary_kn_16x24/'

param_file = dir_name + 'sim_0_true_params.csv'
with open(param_file, 'r') as f:
    param_reader = csv.reader(f)
    true_params = np.array([float(row[0]) for row in param_reader])

init_amounts = np.tile(true_params[:2], no_cultures)
true_amounts = comp.solve_model(init_amounts, times,
                                neighbourhood, true_params[2:])

inde_param_est = inde.fit_model(rows, cols, times, true_amounts)
inde_param_est = np.insert(inde_param_est.x, 2, np.nan)

inde_devs = calc_devs(true_params, 3, inde_param_est)[0]

data = {
    'kn=0 refitting' :
    {
        'true_params' : true_params,
        'inde_est' : inde_param_est.x,
        'inde_devs' : inde_devs
    }
}
# Json requires np.ndarray to be dumped as a list.
for k, v in data.items():
    if isinstance(v, np.ndarray):
        data[k] = v.tolist()

with open(dir_name + 'inde_param_devs_0_strict_stop.json', 'w') as f:
    json.dump(data, f, sort_keys=True, indent=4)



