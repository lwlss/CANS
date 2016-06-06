"""Discover fits which did not run and save arg."""
import glob
import os
import json


from cans2.cans_funcs import dict_to_json


# Coords of zones.
coords = [(7, 13), (9, 15)]

# Arguments which should have been passed.
args = list(range(1210))
args = [str(arg) for arg in args]

# List all of the files in the plot directory for each zone.
path = "results/p15_fits/plots/"
all_files = [f for f in glob.glob(os.path.join(path, "*.pdf"))]

# Group files according to coordinates of zone.
files = []
for coord in coords:
    files.append([f for f in all_files if "coords_{0}_{1}".format(*coord) in f])

# Find missing arguments from filenames.
present_args = [[f.split("_")[-1].split(".")[0] for f in fs] for fs in files]
missing = [[arg for arg in args if arg not in pres] for pres in present_args]

# Write lists to file as json
data = {
    "coords": coords,
    "missing_args": missing
}
data = dict_to_json(data)

with open("missing_data.json", "w") as f:
    json.dump(data, f, indent=4, sort_keys=True)
