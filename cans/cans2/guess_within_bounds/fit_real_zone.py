import numpy as np
import json
import time

from cans2.plate import Plate
from cans2.plotter import Plotter
from cans2.model import CompModel
from cans2.zoning import get_plate_zone
from cans2.guesser import Guesser, add_r_bound
from cans2.cans_funcs import dict_to_json

# Need to make relative
path = "../../../data/p15/Output_Data/"

plate_data = get_plate_data(path)
real_plate = Plate(plate_data["rows"], plate_data["cols"],
                   data=plate_data)

comp_model = CompModel()
plotter = Plotter(comp_model)

#plotter.plot_c_meas(real_plate)

    coords = (3, 17)
    rows = 5
    cols = 5


outdir =  "results/p15_fits/"
datafile = outdir + "coords_{0}_{1}_rows_{2}_cols_{3}_kn_{4}_C0_{5}.json"
datafile = datafile.format(coords[0], coords[1], rows, cols)
plotfile = outdir + "coords_{0}_{1}_rows_{2}_cols_{3}_kn_{4}_C0_{5}.png"
plotfile = plotfile.format(coords[0], coords[1], rows, cols)

zone = get_plate_zone(real_plate, coords, rows, cols)

comp_guesser = Guesser(CompModel())
guess = comp_guesser.make_guess(zone)
param_guess = [guess["C_0"], guess["N_0"], 1.0]
r_guess = [50.0 for i in range(zone.no_cultures)]
param_guess = param_guess + r_guess

    bounds = comp_guesser.get_bounds(zone, guess, factor=1.2)

    # bounds[0] = (5.848410588726615e-07, 5.848410588726615e-05)
    # bounds[1] = (0.05848410588726615, 0.1169682117745323)
    bounds[2] = (1.3, 1.5)

    # add_r_bound(zone, comp_model, , , bounds, (, ))

    t0 = time.time()
    zone.comp_est = zone.fit_model(CompModel(),
                                   param_guess=param_guess,
                                   minimizer_opts={'disp': True},
                                   bounds=bounds)
    t1 = time.time()
    print(t1-t0)

    print(bounds)
    print(zone.comp_est.x)
    plotter.plot_est(zone, zone.comp_est.x, title="Fit of a real zone",
                     filename=plotfile)

    data = {
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


    # plate1 = Plate(5, 5)
    # plate1.times = real_plate.times
    # plate1.set_sim_data(CompModel(), r_mean=10.0, r_var=5.0)
    # plotter.plot_c_meas(plate1)


    # sim_zone = get_plate_zone(plate1, coords=[(1,0), (4,2)])
    # plotter.plot_c_meas(sim_zone)
