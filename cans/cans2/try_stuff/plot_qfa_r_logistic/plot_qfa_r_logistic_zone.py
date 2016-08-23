"""Script to calculate QFA R logistic ojective function and plot a zone."""
import numpy as np
import json
import csv


from cans2.plotter import Plotter
from cans2.model import CompModel, CompModelBC, IndeModel
from cans2.plate import Plate, Culture
from cans2.process import read_in_json, remove_edges, calc_b, calc_N_0, least_sq
from cans2.parser import get_qfa_R_dct
from cans2.genetic_kwargs import _get_plate_kwargs


def convert_to_b(r, K, C_0):
    """Convert logistic r and K to competition K"""
    return r/K

def convert_to_N_0(r, K, C_0):
    """Convert logistic K and C_0 (g) competition N_0"""
    N_0 = K - C_0
    return N_0

def least_sq(a, b):
    """Calculate and return the objective function."""
    assert len(a) == len(b)
    return np.sum((a - b)**2)


plate_path = "data/ColonyzerOutput.txt"
log_path = "data/P15_QFA_LogisticFitnesses.txt"
comp_path = "data/best_comp.json"

# Read in the best competition model fit
comp_data = read_in_json(comp_path)
comp_plate = Plate(**_get_plate_kwargs(comp_data))

rows, cols = comp_plate.rows, comp_plate.cols

# Read in the logistic model data.
log_data = get_qfa_R_dct(log_path)
qfa_R_params = {
    "C_0": np.array(log_data["g"]),
    "r": np.array(log_data["r"]),
    "K": np.array(log_data["K"]),
    }
# Convert logistic model params to competiton model params
log_C_0 = qfa_R_params["C_0"]
log_N_0 = convert_to_N_0(**qfa_R_params)
log_b = convert_to_b(**qfa_R_params)

assert len(log_C_0) == rows*cols; assert len(log_C_0) == len(log_b); assert len(log_C_0) == len(log_N_0)

# Add all of these parameters to Cultures on a Plate
log_plate = Plate(**_get_plate_kwargs(comp_data)) # Get the c_meas for each culture
for C_0, N_0, b, culture in zip(log_C_0, log_N_0, log_b, log_plate.cultures):
    culture.log_params = [C_0, N_0, b]

# Calculate the obective function for each culture and save as an attribute
log_model = IndeModel()
for culture in log_plate.cultures:
    culture.log_amounts = log_model.solve(culture, culture.log_params, culture.times)
    culture.c_log = culture.log_amounts[:, 0]
    culture.least_sq = least_sq(culture.c_log, culture.c_meas)


log_least_sqs = [culture.least_sq for culture in log_plate.cultures]
internal_log_least_sqs = remove_edges(log_least_sqs, rows, cols)

print("All log least sqs", np.sum(log_least_sqs))
print("Internal log least sqs", np.sum(internal_log_least_sqs))

print(log_plate.cultures[66].log_amounts)
# Pass the plate to a plotter as a speacial argument. Simulate each
# culture separately and plot the amounts for the zone from values
# stored in each culture.
fig_settings = {
    "figsize": [16.0, 12.0],
    "dpi": 100.0,
    }
plotter = Plotter(log_model, lw=3.0, ms=12.0, mew=2.0, xpad=5, ypad=17,
                  font_size=30.0, title_font_size=38.0,
                  legend_font_size=22.0, labelsize=16,
                  fig_settings=fig_settings, legend_cols=3, bbox=(1.0, 0.0))
plotter.plot_qfa_R_logistic_fit(log_plate, qfa_R_params)


assert False


result_path = "full_plate/CompModelBC_2/*.json"
best_fit = find_best_fits(result_path, num=1, key="internal_least_sq")
print(best_fit)
fit_data = [read_in_json(find_best_fits(p, 1, "obj_fun")[0][0]) for p in paths]
plates = [Plate(**_get_plate_kwargs(data)) for data in fit_data]

# Read in data from json file
with open(best_fit[0][0], 'r') as f:
    fit_data = json.load(f)

plate = Plate(fit_data["rows"], fit_data["cols"])
models = [CompModel(), CompModelBC()]
model_name = fit_data["model"]
model = next((m for m in models if m.name == fit_data["model"]), None)

# Add necessary data attributes to produce plots
plate.times = fit_data['times']
plate.c_meas = fit_data['c_meas']
# plate.sim_params = fit_data['comp_est']
plate.set_rr_model(model, fit_data['comp_est'])
plate.sim_params = fit_data["comp_est"]


# Plot the guess and fit on the same Figure.
plates = [plate, plate]
plate_names = ["", ""]
est_params = [fit_data["comp_est"], fit_data["init_guess"]]
models = [CompModelBC(), CompModelBC()]
plot_types = ["Estimated", "Guessed"]
coords = (4, 17)
rows, cols = 3, 3
# rows, cols = 12, 20
# coords = (2, 2)
fig_settings = {
    "figsize": [16.0, 12.0],
    "dpi": 100.0,
    }
plot_title = r'Fit of the competition model to P15 (R5, C18)' # for \textit{cdc13-1} P15 at 27C (R5, C18)'
plotter = Plotter(model, lw=3.0, ms=12.0, mew=2.0, xpad=5, ypad=17,
                  font_size=30.0, title_font_size=38.0,
                  legend_font_size=22.0, labelsize=16,
                  fig_settings=fig_settings, legend_cols=3, bbox=(1.0, 0.0))
plotter.plot_zone_est(plates, plate_names, est_params, models, coords,
                      rows, cols, legend=True, title=plot_title,
                      plot_types=plot_types, vis_ticks=False)
# plotter = Plotter(model, lw=3.0, ms=10.0, mew=2.0, xpad=15, ypad=30)
# plotter.plot_zone_est(plates, plate_names, est_params, models, coords,
#                       rows, cols, legend=True, title=plot_title,
#                       plot_types=plot_types, vis_ticks=True)
