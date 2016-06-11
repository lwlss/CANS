"""Solve SBML model using libroadrunner (python2).

Requires libroadrunner installed in python2.

"""
import roadrunner
import time
import timeit


def sim():
    rr.simulate()


if __name__ == "__main__":

    rr = roadrunner.RoadRunner("simulated_16x24_plate_ir_1.xml")
    print(timeit.timeit("sim()", setup="from __main__ import sim", number=1000))

    rr = roadrunner.RoadRunner("simulated_16x24_plate_rev_1.xml")
    print(timeit.timeit("sim()", setup="from __main__ import sim", number=1000))

    rr = roadrunner.RoadRunner("simulated_16x24_plate_rev_2.xml")
    print(timeit.timeit("sim()", setup="from __main__ import sim", number=1000))
