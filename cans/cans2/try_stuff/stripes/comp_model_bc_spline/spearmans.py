import numpy as np
import json
import csv
import Bio.Cluster


from cans2.plate import Plate
from cans2.parser import get_plate_data2
from cans2.model import CompModelBC
from cans2.process import find_best_fits, remove_edges, test_bounds, spearmans_rho, mad_tril


bc_index = 1    # 0 for Stripe, 1 for filled.
num_tops = 1    # Number of top fits to look at.

barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False, "name": "Empty"},
    {"barcode": "K000347_027_022", "ignore_empty": True, "name": "Filled"},    # Filled stripes do not have correct gene names.
])
barcode = barcodes[bc_index]["barcode"]
res_path = barcode + "/results/*.json"

best_fits = np.array(find_best_fits(res_path, num=num_tops, key="obj_fun"))

# for fit in best_fits:
#     print(float(fit[-1])**2)

data = []
for filename in best_fits[:, 0]:
    with open(filename, 'r') as f:
        d = json.load(f)
    data.append(d)

# bs = data[0]["est_params"][-384:]
# print(len(bs))
# print(np.mean(bs))
# assert False

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

# Remove stripes empties and edges from b_ests before finding the
# average.
data_path = "../data/stripes/Stripes.txt"
plates = [Plate(**get_plate_data2(data_path, bc["barcode"])) for bc in barcodes]
genes = plates[0].genes
# Boolean array for non-empties
stripes_bool = genes != "EMPTY"
rows, cols = plates[0].rows, plates[0].cols
stripes_bool = remove_edges(stripes_bool, rows, cols)

b_ests = [remove_edges(bs, rows, cols) for bs in b_ests]
b_ests = np.array([np.extract(stripes_bool, bs) for bs in b_ests])
mads = mad_tril(b_ests)
print(mads)

# outfile = barcode + "_spearmans.csv"
# with open(outfile, 'ab') as f:
#     writer = csv.writer(f, delimiter="\t")
#     writer.writerow(["Spearmans for top {0} fits {1}.".format(num_tops, barcode)])
#     for r in d_tri:
#         writer.writerow(r)
#     writer.writerow(["b parameter MADs for top {0} fits {1}.".format(num_tops, barcode)])
#     for r in mads:
#         writer.writerow(r)
#     writer.writerow(["Plate level parameter ests for top {0} fits {1}.".format(num_tops, barcode)])
#     for r in plate_lvl_ests:
#         writer.writerow(r)
