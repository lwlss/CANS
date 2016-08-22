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


def get_qfa_R_dct(path):
    """Get data from QFA R output."""
    data = pd.read_csv(path, sep="\t", header=0)
    return data


def get_mdrmdp(path):
    """Get mdr*mdp from QFA R output."""
    data = pd.read_csv(path, sep="\t", header=0)
    mdrmdp = data["MDRMDP"]
    return mdrmdp


# Start using ColonyzerOutput.txt files for all parsing.
def get_plate_data2(path, barcode=None, ignore_empty=False):
    """Return data necessary to make a Plate object.

    path : path to ColonyzerOutput.txt file.

    barcode : Data may be from different plates with differing
    barcodes. Choose which to return.

    ignore_empty : (bool) I have some data (stripes) where cultures
    are mistakenly listed with the gene name "EMPTY". In this case
    (True) return empties as an empty np.array.

    """
    data = pd.read_csv(path, sep="\t", header=0)
    if barcode is not None:
        print("Barcodes", set(data["Barcode"]))
        assert barcode in set(data["Barcode"])
        data = data.loc[data["Barcode"] == barcode]
    rows = max(data["Row"])
    cols = max(data["Column"])
    c_meas = np.array(data["Intensity"])
    times = np.array(data["Expt.Time"][::rows*cols])
    # Correct times to set t=0 for first observation.
    times = times - times[0]
    genes = np.array(data["Gene"][:rows*cols])
    if ignore_empty:
        empties = np.array([])
    else:
        empties = np.array([i for i, gene in enumerate(genes) if gene == "EMPTY"])
    plate_data = {
        "rows": rows,
        "cols": cols,
        "data": {
            "c_meas": c_meas,
            "times": times,
            "empties": empties,
            "genes": genes,
            }
        }
    return plate_data


if __name__ == "__main__":
    from cans2.plate import Plate


    stripes_path = "../../data/stripes/Stripes.txt"
    plate1 = Plate(**get_plate_data2(stripes_path, 'K000347_027_022'))
    plate = Plate(**get_plate_data2(stripes_path, 'K000343_027_001'))
    print(plate.genes)
    print(plate.empties)
    print(plate.times)
    assert plate.rows*plate.cols*len(plate.times) == len(plate.c_meas)

    assert all(plate1.genes == plate.genes)
