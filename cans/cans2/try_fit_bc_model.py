import numpy as np

from cans2.plate import Plate
from cans2.model import CompModelBC
from cans2.plotter import Plotter

comp_mod_bc = CompModelBC()
comp_plotter = Plotter(comp_mod_bc)

plate1 = Plate(6, 6)
plate1.times = np.linspace(0, 5, 11)


true_params = {"N_0": 0.1, "NE_0": 0.2, "kn": 0.1}
true_params["C_0"] = true_params["N_0"]/1000000
plate1.set_sim_data(comp_mod_bc, b_mean=50.0, b_var=15.0,
                    custom_params=true_params)

# comp_plotter.plot_c_meas(plate1)

plate1.set_rr_model(comp_mod_bc, plate1.sim_params)


comp_plotter.plot_est(plate1, plate1.sim_params, sim=True)
# plate1.set_rr_selections(indices="internals")
plate1.est = plate1.fit_model(comp_mod_bc, minimizer_opts={"disp": True},
                              rr=True, sel=False)
print(plate1.est.x)
print(plate1.sim_params)


comp_plotter.plot_est(plate1, plate1.est.x, sim=True)
