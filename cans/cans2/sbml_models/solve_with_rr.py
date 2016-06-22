"""Solve SBML model using libroadrunner (python2).

Requires libroadrunner installed in python2.

"""
import roadrunner
import time
import timeit

from cans2.plate import Plate
from cans2.model import CompModel
from cans2.make_sbml import create_sbml

def sim():
    rr.simulate(0, 5, 7200, absolute=1.49012e-8, relative=1.49012e-8)

def sim2():
    rr.simulate(0, 5, 7200)

# if __name__ == "__main__":

#     rr = roadrunner.RoadRunner("simulated_16x24_test_plate_rev.xml")
#     print(timeit.timeit("sim()", setup="from __main__ import sim", number=1))

#     rr = roadrunner.RoadRunner("simulated_16x24_test_plate_ir.xml")
#     rr.reset()
#     print(timeit.timeit("sim()", setup="from __main__ import sim", number=1))

# An example set of real timepoints. The timepoint 5.0 is artificial.
real_times = [
    0.0, 0.5814814814814815, 0.8585648148148148, 1.1073842592592593,
    1.5974421296296297, 1.8656481481481482, 2.6327546296296296,
    3.1222453703703703, 3.5842708333333335, 4.090706018518518, 5.0
]
rows = 16
cols = 24
plate1 = Plate(rows, cols)
plate1.times = real_times
comp_model = CompModel(rev_diff=True)
params = {
    "C_0": 1e-6,
    "N_0": 0.1,
    "kn": 1.5
}

plate1.set_sim_data(comp_model, b_mean=40.0, b_var=15.0,
                    custom_params=params)



# time RoadRunner
p1_sbml = create_sbml(plate1, comp_model, plate1.sim_params)
rr = roadrunner.RoadRunner(p1_sbml)
t0 = time.time()
rr.simulate(0, 5, 50)
t1 = time.time()
print(t1 - t0)
rr.simulate
