import numpy as np
import json
import Bio.Cluster


from cans2.model import CompModelBC
from cans2.process import find_best_fits, test_bounds, spearmans_rho, mad_tril


best_fits = np.array(find_best_fits("full_plate/*/*.json", num=5, key="obj_fun"))

data = []
for filename in best_fits[:, 0]:
    with open(filename, 'r') as f:
        d = json.load(f)
    data.append(d)

at_bounds = [any(test_bounds(d["comp_est"][:4], d["bounds"][:4])) for d in data]
print(at_bounds)

guess_key = "guess_method_C_ratio_zero_kn"
guess_method = [str(d[guess_key][0]) for d in data]
print(guess_method)

# Want to find the model associated with each fit and
models = [d["model"] for d in data]
print(models)


# Make a matrix of correlations of rank orders.
no_cultures = 16*24
b_ests = np.array([d["comp_est"][-no_cultures:] for d in data])

distances = (spearmans_rho(b_ests))
print(distances)

d_tri = np.zeros((5, 5))
for ds, row in zip(distances, d_tri):
    row[:len(ds)] = ds
print(d_tri)

mads = mad_tril(b_ests)
print(mads)


import csv
outfile = "full_plate/replots/first_10_params.csv"
with open(outfile, 'ab') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(models)
    writer.writerow(["Spearmans for top 5 fits (either model)."])
    for r in d_tri:
        writer.writerow(r)
    writer.writerow(["b parameter MADs for top 5 fits (either model)."])
    for r in mads:
        writer.writerow(r)
