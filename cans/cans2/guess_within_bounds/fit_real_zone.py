import numpy as np
import json
import sys
import time

from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.model import CompModel
from cans2.zoning import get_plate_zone
from cans2.guesser import Guesser
from cans2.cans_funcs import dict_to_json
from cans2.parser import get_plate_data


# Which zone in the missing data do you want to repeat.
coords_arg = sys.argv[2]

# Read in coords and and missing args from file
with open("missing_data.json", "r") as f:
    missing = json.load(f)


if str(sys.argv[1]) not in missing["missing_args"][coords_arg]:
    quit()
else:
    pass

# Define area of zone
coords = missing["coords"][coords_arg]
rows = 5
cols = 5

# Set out dir/files for data and plots.
outdir =  "results/p15_fits/"
datafile = outdir + "coords_{0}_{1}_{2}x{3}_argv_{4}.json"
datafile = datafile.format(coords[0], coords[1], rows, cols,
                           sys.argv[1])
plotfile = outdir + "/plots/coords_{0}_{1}_{2}x{3}_argv_{4}.pdf"
plotfile = plotfile.format(coords[0], coords[1], rows, cols,
                           sys.argv[1])

# Read in real plate and make zone
data_path = "../../../data/p15/Output_Data/"
plate_data = get_plate_data(data_path)
real_plate = Plate(plate_data["rows"], plate_data["cols"],
                   data=plate_data)
zone = get_plate_zone(real_plate, coords, rows, cols)

# Generate guesses
comp_model = CompModel()
comp_guesser = Guesser(CompModel())
guess = comp_guesser.make_guess(zone)

# Change guesses for r, kn, and C_0 according to index of guess_vals
# passed as an argument to the script.
r_avgs = np.linspace(25.0, 75.0, 11)
kns = np.linspace(0.0, 10.0, 11)
C_0s = np.logspace(-10, -1, 10)
guess_vals = np.array([(C_0, r, kn) for C_0 in C_0s for r in r_avgs for kn in kns])
guess_val = guess_vals[int(sys.argv[1])]
C_0_guess = guess_val[0]*guess["N_0"]    # Scale by value of N_0 guess
r_guess = guess_val[1]
kn_guess = guess_val[2]

# Set param guess
param_guess = [C_0_guess, guess["N_0"], kn_guess]
r_guesses = [r_guess for i in range(zone.no_cultures)]
param_guess = param_guess + r_guesses

# Set bounds
bounds = comp_guesser.get_bounds(zone, guess)
# bounds for C_0, N_0, and kn.
bounds[0] = (guess["N_0"]*1.0e-10, guess["N_0"]/10)
bounds[2] = (0.0, 11.00)

t0 = time.time()
zone.comp_est = zone.fit_model(CompModel(),
                               param_guess=param_guess,
                               minimizer_opts={'disp': False},
                               bounds=bounds)
t1 = time.time()

# print(t1-t0)
# print(bounds[:3])
# print(zone.comp_est.x)
# print(zone.comp_est.fun)

data = {
    'argv': int(sys.argv[1]),
    'fit_time': t1-t0,
    'zone_coords': coords,
    'zone_rows': rows,
    'zone_cols': cols,
    'bounds': bounds,
    'comp_est': zone.comp_est.x,
    'obj_fun': zone.comp_est.fun,
    'init_guess': param_guess,
    'model': comp_model.name,
    'model_params': comp_model.params,
    'model_species': comp_model.species
    }
data = dict_to_json(data)


with open(datafile, 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)


plotter = Plotter(comp_model)
plotter.plot_est(zone, zone.comp_est.x,
                 title="Fit of p15 ({0},{1}) 5x5 zone".format(*coords),
                 filename=plotfile)
