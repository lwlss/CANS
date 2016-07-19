import csv
import glob
import os
from datetime import datetime
import pandas as pd
import numpy as np


def datetime_to_days(datetimes):
    """Return time in days with zero at first timepoint."""
    t0 = datetimes[0]
    days = [(dt - t0).total_seconds()/(60*60*24) for dt in datetimes]
    return(days)


def get_data_files(path, ext="*.out"):
    """Get all filenames in a directory with extension ext.

    Returns full paths.

    """
    files = [f for f in glob.glob(os.path.join(path, ext))]
    return files


def name_to_datetime(filename):
    """Return a datatime from a Colonyzer datafile name."""
    froot = os.path.basename(filename).split(".")[0]
    dt_obj = datetime.strptime(froot[-19:], "%Y-%m-%d_%H-%M-%S")
    return dt_obj


# Should use splitting and remove -20 and -19.
def parseColonyzer(fname):
    """Read in Colonyzer csv file and parse some info from filename."""
    # From Conor's parseColonyzer.py.
    froot = os.path.basename(fname).split(".")[0]
    barc = froot[0:-20]
    dt = froot[-19:]
    data = pd.read_csv(fname, sep="\t", header=0)
    data["Barcode"] = barc
    data["DateTime"] = datetime.strptime(dt, "%Y-%m-%d_%H-%M-%S")
    data["FileName"] = froot
    return(data)


def get_plate_data(path):
    """Return data necessary to make a Plate object.

    path : directory containing Colonyzer output files for one plate.

    """
    files = get_data_files(path)
    files.sort(key=name_to_datetime)
    c_meas = np.array([])
    times = []
    for filename in files:
        data = parseColonyzer(filename)
        c_meas = np.append(c_meas, data["Intensity"])
        times.append(data["DateTime"][0])
    # Just take from last file read in. Could add an assertion to
    # check all files are for same plate.
    rows = max(data["Row"])
    cols = max(data["Column"])
    plate_data = {
        "rows": rows,
        "cols": cols,
        "times": datetime_to_days(times),
        "c_meas": c_meas,
        "empties": []
    }
    return plate_data


def get_genes(filename):
    """Return plate gene names by row.

    Requires a csv file with a column genes listing genes by row. I am
    using the file ColonyzerOutput.txt which seems to have been
    automatically generated in the same directory as the raw images.

    """
    data = pd.read_csv(filename, sep="\t", header=0)
    genes = data["Gene"]
    # orfs = data["ORF"]
    return genes


if __name__ == "__main__":
    import json
    import time

    from cans2.plate import Plate
    from cans2.plotter import Plotter
    from cans2.model import CompModel
    from cans2.zoning import get_plate_zone
    from cans2.guesser import Guesser, add_r_bound
    from cans2.cans_funcs import dict_to_json



    path = "../../data/p15/Output_Data/"

    plate_data = get_plate_data(path)
    times = plate_data["times"]
    print(times)
    steps = [times[i + 1] - times[i] for i in range(len(times) - 1)]
    print(steps)


    assert False
    real_plate = Plate(plate_data["rows"], plate_data["cols"],
                       data=plate_data)

    comp_model = CompModel()
    plotter = Plotter(comp_model)

    #plotter.plot_c_meas(real_plate)

    coords = (3, 17)
    rows = 5
    cols = 5


    outdir =  "results/p15_fits/first_attempt/"
    datafile = outdir + "coords_{0}_{1}_rows_{2}_cols_{3}_1.json"
    datafile = datafile.format(coords[0], coords[1], rows, cols)
    plotfile = outdir + "coords_{0}_{1}_rows_{2}_cols_{3}_1.pdf"
    plotfile = plotfile.format(coords[0], coords[1], rows, cols)

    # This would have 5 rows and 5 cols
    zone = get_plate_zone(real_plate, coords, rows, cols)
    # plotter.plot_c_meas(zone)

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
