import numpy as np
import json


from plate import Plate
from model import CompModel


rand_rs_dir = '16x24_rs_mean_{}_var_{}/'

mean = 5
var = 3

rows = 16
cols = 24

custom_params = {
    'C_0': 0.0001,
    'N_0': 1.0,
    'kn': 0.1,
}
custom_params['kn'] = 0.2

model = CompModel()
times = np.linspace(0, 5, 21)

# Generate 100 sets or random rs.
for i in range(100):
    plate1 = Plate(rows, cols)
    plate1.times = times
    plate1.set_sim_data(model, r_mean=mean, r_var=var,
                        custom_params=custom_params)

    rand_rs = plate1.sim_params[model.r_index:]
    rand_rs = rand_rs.tolist()
    assert len(rand_rs) == plate1.no_cultures

    data = {
        'rand_rs': rand_rs,
        'mean': mean,
        'var': var,
        'no_cultures': plate1.no_cultures
    }
    with open(rand_rs_dir.fromat(mean, var) + '16x24_rs_{}.json'.format(i), 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
