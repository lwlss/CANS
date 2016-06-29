import numpy as np
import json
import Bio.Cluster
import itertools


from cans2.model import CompModelBC
from cans2.process import find_best_fits, test_bounds, spearmans_rho, mad_tril


best_fits = np.array(find_best_fits("full_plate/*.json", 5, key="obj_fun"))

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

model = CompModelBC()

# Make a matrix of correlations of rank orders.
b_ests = np.array([d["comp_est"][model.b_index:] for d in data])

distances = (spearmans_rho(b_ests))
print(distances)

mads = mad_tril(b_ests)
print(mads)



# for x, y in np.nditer([b_ests, b_ests]):
#     print(vmad(x, y))
