import numpy as np


from cans2.process import read_in_json
from cans2.plotter import plot_scatter


results_dir = "results/local_min_sims/"
data_path = results_dir + "sim_0_b_index_5_uniform.json"

data = read_in_json(data_path)

no_cultures = data["rows"]*data["cols"]
x = data["sim_params"][-no_cultures:]
y = data["est_params"][-no_cultures:]
title = "b correlation (Gaussian simulated)"
xlab = "True b"
ylab = "Estimated b"
outfile = results_dir + "plots/est_v_true/uniform_sim_0.pdf"

plot_scatter(x, y, title, xlab, ylab, outfile)
