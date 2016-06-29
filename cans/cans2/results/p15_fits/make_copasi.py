import json


from cans2.plate import Plate
from cans2.copasi import write_c_meas
from cans2.process import find_best_fits


path = "full_plate/CompModelBC/*.json"

best = find_best_fits(path, 3, key="obj_fun")
print(best)

with open(best[0][0], 'r') as f:
    d = json.load(f)

plate = Plate(d["rows"], d["cols"])
plate.times = d["times"]
plate.c_meas = d["c_meas"]

write_c_meas(plate, outfile="copasi/p15_c_meas.csv")
