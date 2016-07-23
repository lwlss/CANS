import numpy as np

from cans2.cans_funcs import dict_to_numpy, dict_to_json
from cans2.process import read_in_json, find_best_fits
from cans2.genetic_kwargs import _get_plate_kwargs
from cans2.zoning import get_plate_zone
from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC, IndeModel
from cans2.plotter import Plotter


best_fit = "data/argv_5_b_guess_35.json"

data = read_in_json(best_fit)
est_params = data["comp_est"]
bounds = data["bounds"]

# make plate from data
plate = Plate(**_get_plate_kwargs(data))



assert False

# Take cell measurements for culture (9, 2).
culture = get_plate_zone(plate, (9, 2), 1, 1)
final_cells = culture.c_meas[-1]

c_meas = cult

inde_model = IndeModel()
culture_guess = np.array([est_params[0], final_cells, 0.0])
culture_bounds = np.array([[0.0, final_cells*100],
                           # bounds[0],
                           [final_cells*0.7, final_cells*1.3],
                           [0, 200.0]])
print(culture_guess)
print(culture_bounds)

culture.inde_est = culture.fit_model(inde_model, culture_guess, culture_bounds,
                                     rr=False)
print(culture.inde_est.x)

inde_plotter = Plotter(IndeModel())
inde_plotter.plot_est(culture, culture.inde_est.x, sim=False)
