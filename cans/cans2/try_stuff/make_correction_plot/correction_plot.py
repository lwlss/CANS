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
est_params = np.array(data["comp_est"])
bounds = data["bounds"]
comp_modelbc = CompModelBC()
no_cultures = data["rows"]*data["cols"]

coords = (9, 2)    # Culture of interest.
culture_i = coords[0]*data["cols"] + coords[1]

# make plate from data and make a 1x1 zone for the culture of interest.
plate = Plate(**_get_plate_kwargs(data))
plate.est_params = est_params

# Get the params for simulating the correction
correction_params = np.concatenate((est_params[:2],
                                    [est_params[culture_i - no_cultures]]))


# Take cell measurements for culture (9, 2).
culture = get_plate_zone(plate, coords, 1, 1)
final_cells = culture.c_meas[-1]
c_meas = culture.c_meas

inde_model = IndeModel()
culture_guess = np.array([est_params[0], final_cells, 0.0])
culture_bounds = np.array([[0.0, final_cells*100],
                           [final_cells*0.7, final_cells*1.3],
                           [0, 200.0]])

culture.inde_est = culture.fit_model(inde_model, culture_guess, culture_bounds,
                                     rr=False)

inde_plotter = Plotter(IndeModel(), ms=10.0, mew=1.5, lw=2.5,
                       font_size=18, title_font_size=20,
                       legend_font_size=16, xpad=1, ypad=7,
                       labelsize=12)
inde_plotter.plot_est(culture, culture.inde_est.x, sim=False,
                      legend=True, title="Logistic Equivalent Fit")


# smooth times for simulation
smooth_plate = Plate(**_get_plate_kwargs(data))
smooth_plate.times = np.linspace(plate.times[0], plate.times[-1], 100)    # for smooth sim
smooth_plate.est_params = est_params
smooth_plate.set_rr_model(comp_modelbc, smooth_plate.est_params)
smooth_plate.est_amounts = comp_modelbc.rr_solve(smooth_plate, smooth_plate.est_params)

# Now get est C and N for culture
c_i = smooth_plate.est_amounts[:, culture_i]
n_i = smooth_plate.est_amounts[:, no_cultures + culture_i]
culture_est_amounts = np.dstack((c_i, n_i))[0]

culture_c = Plate(1, 1)
culture_c.times = culture.times
culture_c.c_meas = culture.c_meas
culture_c.sim_params = correction_params
culture_c.comp_amounts = culture_est_amounts

inde_plotter.plot_correction(culture_c, culture_c.sim_params,
                             culture_c.comp_amounts, legend=True,
                             title="Corrected Competition Fit")
