import numpy as np
import json


from cans2.process import read_in_json, find_best_fits


def get_sim_data(path, guessing):
    """Return a list of data from each sim for a given guessing method."""
    paths = np.array([path.format(sim, guessing) for sim in range(5)])
    sim_fits = []
    for path in paths:
        sim_fits.append(np.array(find_best_fits(path, num=None, key="MAD")))

    sim_data = []
    for paths in sim_fits:
        sim_data.append(np.vectorize(read_in_json)(paths[:, 0]))
    return sim_data

data_path = "results/local_min_sims/sim_{0}*{1}.json"

uniform = get_sim_data(data_path, "uniform")
imag_neigh = get_sim_data(data_path, "imag_neigh")

print(len(uniform), len(imag_neigh))
print(uniform[0][0].keys())
print(imag_neigh[0][0].keys())

print("uniform")

for i, sim in enumerate(uniform):
    print("sim", i)
    for b_guess in sim:
        print("b_index", b_guess["b_index"], "MAD", b_guess["MAD"], "fun", b_guess["obj_fun"])

print("")
print("imag_neigh")

mean_times = []
total_times = []
for i, sim in enumerate(imag_neigh):
    print("sim", i)
    # mads = []
    times = []
    obj_funs = []
    for b_guess in sim:
        print("b_index", b_guess["b_index"], "MAD", b_guess["MAD"], "fun", b_guess["obj_fun"])
        # mads.append(b_guess["MAD"]))
        times.append([b_guess["guess_time"], b_guess["fit_time"], b_guess["total_time"]])
        obj_funs.append(b_guess["obj_fun"])
    print(obj_funs.index(min(obj_funs)) == 0)
    times = np.array(times)
    total_times.append(times[:, 2])
    mean_times.append(np.mean(times[:, 2]))
    print(mean_times[-1])
    print(times)

print(mean_times)
print(np.mean(mean_times))
print("max", np.max(total_times), "min", np.min(total_times))
print("")

