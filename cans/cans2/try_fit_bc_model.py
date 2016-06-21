import numpy as np

from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC
from cans2.plotter import Plotter
from cans2.guesser import Guesser

# First try solving and plotting ordinary CompModel
comp_model = CompModel(rev_diff=False)

plate1 = Plate(3, 3)
plate1.times = np.linspace(0, 5, 11)

true_params = {"N_0": 0.1, "kn": 1.0}
true_params["C_0"] = true_params["N_0"]/100000

# Also sets rr_model with the simulated params
plate1.set_sim_data(comp_model, b_mean=50.0, b_var=15.0,
                    custom_params=true_params)

comp_plotter = Plotter(comp_model)
comp_plotter.plot_est(plate1, plate1.sim_params,
                      title="CompModel Simulation", sim=True)

comp_guesser = Guesser(comp_model)

# Then try CompModelBC

comp_mod_bc = CompModelBC()
comp_plotter_bc = Plotter(comp_mod_bc)

plate_bc = Plate(6, 6)
plate_bc.times = np.linspace(0, 5, 11)


true_params_bc = {"N_0": 0.1, "NE_0": 0.15, "kn": 1.0}
true_params_bc["C_0"] = true_params_bc["N_0"]/1000000
# Also sets rr_model with the simulated params
plate_bc.set_sim_data(comp_mod_bc, b_mean=50.0, b_var=15.0,
                      custom_params=true_params_bc)

comp_plotter_bc.plot_est(plate_bc, plate_bc.sim_params, sim=True)

# plate_bc.est = plate_bc.fit_model(comp_mod_bc, minimizer_opts={"disp": True},
#                               rr=True, sel=False)
# print(plate_bc.est.x)
# print(plate_bc.sim_params)


# comp_plotter.plot_est(plate_bc, plate_bc.est.x, sim=True)
