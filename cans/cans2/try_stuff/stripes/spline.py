"""Speed up fitting by splining to reduce no. timepoints.

Many more timepoints in the stripes data set than p15. This is slowing
down the roadrunner solver. If we spline the data we can take a
smaller number of timepionts. It will also be possible to use even
timesteps which should make the roadrunner solver quicker still,
although we will have to reimplement."""
import numpy as np
# import json
import sys
# import time
import matplotlib.pyplot as plt

from scipy import interpolate


from cans2.parser import get_plate_data2
from cans2.plate import Plate
from cans2.model import CompModelBC, CompModel
# from cans2.guesser import fit_imag_neigh, Guesser
# from cans2.cans_funcs import dict_to_json
from cans2.plotter import Plotter
# from cans2.make_sbml import create_sbml
from cans2.zoning import get_plate_zone


barcodes = np.array([
    {"barcode": "K000343_027_001", "ignore_empty": False},
    {"barcode": "K000347_027_022", "ignore_empty": True},    # Filled stripes do not have correct gene names.
])
barcode = barcodes[int(sys.argv[2])]

plate_model = CompModel()
plotter = Plotter(plate_model)

# Read in real data and make a plate.
data_path = "../../../../data/stripes/Stripes.txt"
full_plate = Plate(**get_plate_data2(data_path, **barcode))
barcode = barcode["barcode"]

zone = get_plate_zone(full_plate, (5,5), 3, 3)    ###### ZONE ######

print(zone)

# param_guess = np.array([1e-4, 0.1, 0.15, 5.0] + [30.0 for c in range(zone.no_cultures)])
# bounds = np.array([
#     [1e-7, 1e-2],
#     [0., ],
#     [, ],
#     [, 10.0],
# ])

custom_params = {
    "C_0": 1e-4,
    "N_0": 0.1,
#    "NE_0": 0.15,
    "kn": 2.0,
    }

sim_3x3 = Plate(3, 3)
sim_3x3.times = zone.times
sim_3x3.growers = np.arange(sim_3x3.no_cultures)
sim_3x3.empties = []
sim_3x3.set_sim_data(plate_model, b_mean=35.0, b_var=15.0,
                     custom_params=custom_params, noise=True)
# plotter.plot_c_meas(sim_3x3)    # Plot Spline would be nice.

bounds = [
    [1e-4, 1e-4],
    [0.1, 0.1],
#    [0.085, 0.2],
    [2.0, 2.0],
    ]
bounds += [[0.0, 100.0] for i in range(sim_3x3.no_cultures)]
bounds = np.array(bounds)

param_guess = np.concatenate((np.array([1e-4, 0.1, 2.0]),
                              np.array([35.0 for i in range(sim_3x3.no_cultures)])))


print(bounds)
print(param_guess)

sim_3x3.make_spline(time_steps=15)
sim_3x3.set_rr_model(plate_model, param_guess)

assert len(sim_3x3.c_spline) == len(sim_3x3.t_spline)*sim_3x3.no_cultures

plotter.plot_spline(sim_3x3)

# Default smoothing s=m-sqrt(2*m) where m is the number of data points.
est = sim_3x3.fit_spline(plate_model, param_guess, bounds,
                         minimizer_opts={"disp": True})


print("truth")
print(sim_3x3.sim_params)
print("est")
print(est.x)

plotter.plot_est_rr(sim_3x3, est.x, title="Zone spline growth")



# plt.figure()
# plt.plot(zone.t_spline, zone.c_spline, 'x', xnew, ynew, xnew, np.sin(xnew), x, y, 'b')
# plt.legend(['Linear', 'Cubic Spline', 'True'])
# plt.axis([-0.05, 6.33, -1.05, 1.05])
# plt.title('Cubic-spline interpolation')
# plt.show()
