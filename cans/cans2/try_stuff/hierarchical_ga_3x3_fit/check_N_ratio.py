import numpy as np
from cans2.process import read_in_json

filename = "data/local_min_sims/sim_{0}.json"
sim_params = [read_in_json(filename.format(i))["sim_params"] for i in range(5)]
sim_params = np.array(sim_params)
N_0 = sim_params[:, 1]
NE_0 = sim_params[:, 2]

print(["sim_{0}".format(i) for i in np.arange(5)])
print("N_0", N_0)
print("NE_0", NE_0)
print("NE_0/N_0", NE_0/N_0)
