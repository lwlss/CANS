"""Discover fits which did not run and save arg."""
import glob
import os
import json



coords = [(7, 13), (9, 15)]

# Arguments which should have been passed.
args = list(range(1210))
args = [str(arg) for arg in args]

# List all of the files in the plot directory for each zone
path = "results/p15_fits/plots/"
all_files = [f for f in glob.glob(os.path.join(path, "*.pdf"))]

files = []
for coord in coords:
    files.append([f for f in all_files if "coords_{0}_{1}".format(*coord) in f])

# files_7_13 = [f for f in all_files if "coords_7_13" in f]
# files_9_15 = [f for f in all_files if "coords_9_15" in f]

present_args = [[f.split("_")[-1].split(".")[0] for f in fs] for fs in files]
missing = [[arg for arg in args if arg not in pres] for pres in present_args]


# Write this list to file as json.
