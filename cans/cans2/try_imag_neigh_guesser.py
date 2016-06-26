import numpy as np


from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC, ImagNeighModel
from cans2.guesser import Guesser, sim_a_plate, fit_imag_neigh
from cans2.cans_funcs import gauss_list
from cans2.plotter import Plotter


model = CompModelBC()
rows = 8
cols = 8
times = np.linspace(0, 5, 11)
true_params = {"N_0": 0.1, "NE_0": 0.15, "kn": 1.0}
true_params["C_0"] = true_params["N_0"]/10000
bs = gauss_list(rows*cols, mean=50.0, var=30.0, negs=False)
# Make a np.array of true params.
true_params = np.array([true_params[p] for p in model.params[:model.b_index]]
                       + list(bs))

sim_kwargs = {
    "rows": rows,
    "cols": cols,
    "times": times,
    "model": model,
    "true_params": true_params,
}

plate = sim_a_plate(rows, cols, times, model, true_params)

quick_fit_kwargs = {
    "plate": plate,
    "plate_model": model,
    # Guess of edge_area/internal_area. Only required for CompModelBC and
    # ignored for CompModel.
    "area_ratio": 1.5,
    # Not including amounts which are guesses from final cell amounts
    # and the C_ratio argument. ['kn1', 'kn2', 'b-', 'b+', 'b'] The
    # final parameter is the guess of the CompModel parameter b. Other
    # parameters are uniquie to the imaginary neighbour model.
    "imag_neigh_params": np.array([1.0, 1.0, 0.0, 50.0, 45.0]),
    "no_neighs": None,    # Can specify or allow it to be calculated np.ceil(C_f/N_0)
    "C_ratio": 1e-4,    # Guess of init_cells/final_cells.
    # "C_doubt": 1e2,
    # "N_doubt": 2.0,
}

quick_guess, quick_guesser = fit_imag_neigh(**quick_fit_kwargs)
# Need to add in a kn guess.
quick_guess[model.params.index("kn")] = true_params[model.params.index("kn")]

print("true_parms", true_params)
print("quick_guess", quick_guess)

# Plot a rr model solution using the estimated b params and the true kn
plotter = Plotter(model)
plotter.plot_est_rr(quick_guesser.plate, quick_guess, sim=True)

full_param_guess = quick_guesser.guess_kn(0, 2, 21, quick_guess)
print("and kn", full_param_guess)
plotter.plot_est_rr(quick_guesser.plate, full_param_guess, sim=True)
