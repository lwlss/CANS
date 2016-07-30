import numpy as np
import json
import csv
import Bio.Cluster



from cans2.model import CompModelBC
from cans2.process import find_best_fits, test_bounds, spearmans_rho, mad_tril

bc_index = 1    # 0 for Stripe, 1 for filled.
num_tops = 5    # Number of top fits to look at.

barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False, "name": "Empty"},
    {"barcode": "K000347_027_022", "ignore_empty": True, "name": "Filled"},    # Filled stripes do not have correct gene names.
])
barcode = barcodes[bc_index]["barcode"]
res_path = barcode + "/results/*.json"

best_fits = np.array(find_best_fits(res_path, num=num_tops, key="obj_fun"))

data = []
for filename in best_fits[:, 0]:
    with open(filename, 'r') as f:
        d = json.load(f)
    data.append(d)

at_bounds = [any(test_bounds(d["est_params"][:4], d["bounds"][:4])) for d in data]
print(at_bounds)

# Make a matrix of correlations of rank orders.
no_cultures = 16*24
b_ests = np.array([d["est_params"][-no_cultures:] for d in data])
plate_lvl_ests = np.array([d["est_params"][:-no_cultures] for d in data])

distances = (spearmans_rho(b_ests))
print(distances)

d_tri = np.zeros((5, 5))
for ds, row in zip(distances, d_tri):
    row[:len(ds)] = ds
print(d_tri)

mads = mad_tril(b_ests)
print(mads)

outfile = barcode + "_spearmans.csv"
with open(outfile, 'ab') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["Spearmans for top {0} fits {1}.".format(num_tops, barcode)])
    for r in d_tri:
        writer.writerow(r)
    writer.writerow(["b parameter MADs for top {0} fits {1}.".format(num_tops, barcode)])
    for r in mads:
        writer.writerow(r)
    writer.writerow(["Plate level parameter ests for top {0} fits {1}.".format(num_tops, barcode)])
    for r in plate_lvl_ests:
        writer.writerow(r)
