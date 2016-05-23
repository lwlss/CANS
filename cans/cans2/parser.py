import csv
import glob
import os
from datetime import datetime
import pandas as pd
import numpy as np

# Ideally want to specify two coordinates on plate and find the data
# for that grid. Can just read in whole plate and do this with
# zoning.py.


# read in as a np.array()
# Easily converts to a c_meas flat list.

# Need to open all files in the directory and take the time and
# intensity measurement.

# Consider package_resources and how data will actually be read
# in. Will we be invoking a packaged script instead?


def get_data_files(path, ext="*.out"):
    """Get all filenames in a directory with extension ext.

    Returns full paths.

    """
    files = [f for f in glob.glob(os.path.join(path, ext))]
    return files


def name_to_datetime(filename):
    """Returns a datatime from a Colonyzer datafile name."""
    froot = os.path.basename(filename).split(".")[0]
    dt_obj = datetime.strptime(froot[-19:], "%Y-%m-%d_%H-%M-%S")
    return dt_obj


def parseColonyzer(fname):
    """Read in Colonyzer csv file and parse some info from filename.

    From Conor's parseColonyzer.py"""
    froot=os.path.basename(fname).split(".")[0]
    barc=froot[0:-20]
    dt=froot[-19:]
    data=pd.read_csv(fname,sep="\t",header=0)
    data["Barcode"]=barc
    data["DateTime"]=datetime.strptime(dt, "%Y-%m-%d_%H-%M-%S")
    data["FileName"]=froot
    return(data)


def get_plate_data(path):
    """Return data necessary to make a Plate object.

    path is the directory containing Colonyzer output files for one
    plate.

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
        "times": times,
        "c_meas": c_meas,
        "empties": []
    }
    return plate_data

if __name__ == "__main__":
    from cans2.plate import Plate
    from cans2.plotter import Plotter
    from cans2.model import CompModel


    path = "/home/dan/projects/CANS/data/p15/Output_Data/"

    plate_data = get_plate_data(path)
    real_plate = Plate(plate_data["rows"], plate_data["cols"],
                       data=plate_data)

    comp_model = CompModel
    plotter = Plotter(comp_model)
    plotter.plot_c_meas(real_plate)
