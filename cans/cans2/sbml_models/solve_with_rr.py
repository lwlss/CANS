"""Solve SBML model using libroadrunner (python2).

Requires libroadrunner installed in python2.

"""
import roadrunner
import time
import roadrunner.testing as rrtest


rr = roadrunner.RoadRunner("simulated_16x24_plate.xml")
t0 = time.time()
result = rr.simulate()
t1 = time.time()
print(t1 - t0)
rr.plot()
