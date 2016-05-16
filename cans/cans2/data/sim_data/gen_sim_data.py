"""Simulate plate amounts and save data as json."""
import numpy as np
import json


from cans2.plate import Plate
from cans2.model import CompModel
from cans2.cans_funcs import dict_to_json


mean = 5
var = 3

rows = 5
cols = 5

file_name = '{0}x{1}_comp_model/mean_5_var_3.json'.format(rows, cols)

custom_params = {
    'C_0': 0.0001,
    'N_0': 1.0,
    'kn': 0.1,
}
custom_params['kn'] = 0.2

model = CompModel()
times = np.linspace(0, 5, 21)

# Generate sets of simulated amounts
for i in range(1):
    plate1 = Plate(rows, cols)
    plate1.times = times
    plate1.set_sim_data(model, r_mean=mean, r_var=var,
                        custom_params=custom_params)

    data = {
        'sim_params': plate1.sim_params,
        'sim_amounts': plate1.sim_amounts,
        'c_meas': plate1.c_meas,
        'times': plate1.times,
        'r_mean': mean,
        'r_var': var,
        'rows': plate1.rows,
        'cols': plate1.cols,
        'model': model.name,
        'model_params': model.params,
    }
    data = dict_to_json(data)

    with open(file_name, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
