import numpy as np


from cans2.plate import Plate, Culture
from cans2.plotter import Plotter
from cans2.model import ImagNeighModel
from cans2.genetic_kwargs import _get_plate_kwargs
from cans2.process import read_in_json


data_path = "data/best_comp.json"
plate_data = read_in_json(data_path)

plate = Plate(**_get_plate_kwargs(plate_data))

# Choose one culture and plot as a row with c_meas in the middle slow
# and fast either side.

coords = (5, 18)   # Central culture from the zone
culture_index = coords[0]*plate.cols + coords[1]

est_params = plate_data["est_params"]
est_b = est_params[4:][culture_index]

guess_kwargs = plate_data["guess_kwargs"]

imag_neigh_mod = ImagNeighModel(no_neighs=6)

b_fast = 60.0
imag_neigh_params = [est_params[0], est_params[1], 0.0, 0.0, 0.0, b_fast, 35.0]

culture = plate.cultures[culture_index]

neigh_bounds = [
    [est_params[0], est_params[0]],
    [est_params[1], est_params[1]],
    [0.0, 10.0],
    [0.0,10.0],
    [0.0, 0.0],
#    [est_b, est_b],
    [b_fast, b_fast],
    [0.0, 100.0],
    ]
culture.im_neigh_est = culture.fit_model(imag_neigh_mod,
                                         imag_neigh_params,
                                         neigh_bounds)
print(culture.im_neigh_est.x)
# solve() to get amounts and pass these to be plotted in a grid.
amounts = imag_neigh_mod.solve(culture, culture.im_neigh_est.x)
print(amounts)
