"""Discover fits which did not run and save arg."""
import glob
import json



# Arguments which should have been passed.
args = list(range(1201))

# List all of the files in the plot directory for each zone
path = "results/p15/plots/"

# Find list of args from filename that are in arglist but not a file.

# Write this list to file as json.
