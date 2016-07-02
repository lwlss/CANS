import numpy as np


from cans2.model import CompModelBC
from cans2.plate import Plate
from cans2.guesser import fit_imag_neigh
from cans2.plotter import Plotter

# Simulate a small 3x3 plate with noise using CompModelBC or CompModel.
rows = 3
cols = 3
times = np.linspace(0, 5, 11)
model = CompModelBC()
plate = Plate(rows, cols)
plate.times = times

C_ratio = 1e-4
area_ratio = 1.4
N_0 = 0.1
b_guess = 45.0
custom_params = {
    "C_0": N_0*C_ratio,
    "N_0": N_0,
    "NE_0": N_0*area_ratio,
    "kn": 1.0,
}
plate.set_sim_data(model, b_mean=50.0, b_var=30.0,
                   custom_params=custom_params, noise=True)

plotter = Plotter(model)
plotter.plot_est_rr(plate, plate.sim_params,
                    title="Sim timecourse", sim=False)

# Starting guess from fits of the imaginary neighbour model.
imag_neigh_params = np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess])

guess, guess_plate = fit_imag_neig(plate, model, area_ratio, C_ratio,
                                   imag_neigh_params,
                                   kn_start=0.0, kn_stop=8.0, kn_num=21)


# Construct a genetic algorithm to fit and compare with the current
# gradient method.

plate.grad_est = plate.fit_model(model, param_guess, bounds=True, rr=True)
