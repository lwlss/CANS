import json
import numpy as np

import cans.inde as inde
import cans.competition as comp
from cans.cans import find_neighbourhood


rows = 16
cols =24
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
times = np.linspace(0, 15, 21)

with open('inde_param_devs_0_strict_stop_1000.json', 'r') as f:
    data = json.load(f)

true_params = data['true_params']
inde_est = data['inde_est']


# Plot using save in matplot window (true and inde)
inde_sol = inde.solve_model(np.tile(inde_est[:2], no_cultures), times,
                            neighbourhood, inde_est[3:])
inde.plot_growth(rows, cols, inde_sol, times,
                 title="Independent Fit 16x24 (kn=0)")

true_sol = comp.solve_model(np.tile(true_params[:2], no_cultures), times,
                            neighbourhood, true_params[2:])
comp.plot_growth(rows, cols, true_sol, times,
                 title="Truth 16x24 (kn=0)")
