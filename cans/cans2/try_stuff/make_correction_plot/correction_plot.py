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
comp_modelbc = CompModelBC()

coords = (9, 2)    # Culture of interest.
culture_i = coords[0]*data["rows"] + coords[1] + 1

# make plate from data and simulate amounts from est params
plate = Plate(**_get_plate_kwargs(data))
plate.est_params = est_params
plate.set_rr_model(comp_modelbc, plate.est_params)
plate.est_amounts = comp_modelbc.rr_solve(plate, plate.est_params)

# Now get est C and N for culture
c_i = plate.est_amounts[:, culture_i]
n_i = plate.est_amounts[:, plate.no_cultures + culture_i]
culture_est_amounts = np.dstack((c_i, n_i))[0]

# Get the params for simulating the correction
correction_params = np.concatenate((plate.est_params[:2],
                                    [plate.est_params[culture_i - plate.no_cultures]]))



# Take cell measurements for culture (9, 2).
culture = get_plate_zone(plate, coords, 1, 1)
final_cells = culture.c_meas[-1]

c_meas = culture.c_meas

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


culture_c = Plate(1, 1)
culture_c.times = plate.times
culture_c.c_meas = culture.c_meas
culture_c.sim_params = correction_params
culture_c.comp_amounts = culture_est_amounts
print(culture_c.sim_params)
print(culture.sim_params)

inde_plotter.plot_correction(culture_c, culture_c.sim_params,
                             culture_c.comp_amounts, legend=True)
