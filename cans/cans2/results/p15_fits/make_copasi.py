import numpy as np
import json


from cans2.plate import Plate
from cans2.model import CompModelBC, CompModel
from cans2.copasi import write_c_meas
from cans2.process import find_best_fits
from cans2.make_sbml import create_sbml
from cans2.zoning import get_plate_zone, get_zone_bs

path = "full_plate/CompModelBC/*.json"

best = find_best_fits(path, 3, key="obj_fun")
print(best)

with open(best[0][0], 'r') as f:
    d = json.load(f)

plate = Plate(d["rows"], d["cols"])
plate.times = d["times"]
plate.c_meas = d["c_meas"]

write_c_meas(plate, outfile="full_plate/copasi/p15_c_meas.csv")

# I accidentally save the initial guess SBML rather than the SBML for
# the estimated parameters. Not to worry we have these in the json
# data.
model = CompModelBC()
est_params = d["comp_est"]
# outfile = "full_plate/copasi/compmodelbc_argv_5_b_guess_35.xml"
# sbml = create_sbml(plate, model, est_params, outfile)


# print(est_params)
print(d["bounds"][:5])
assert False

# Try copasi fitting for a zone first to make sure that I am doing it right.
zone = get_plate_zone(plate, (5, 5), 3, 3)
zone_params = np.delete(est_params[:model.b_index], 2)
zone_bs = get_zone_bs(est_params[model.b_index:], 16, 24, (5, 5), 3, 3)
zone_params = np.concatenate((zone_params, zone_bs))
zone_out = "full_plate/copasi/p15_test_5_5_3x3_from_compmodelbc_argv_5_b_guess_35.xml"
write_c_meas(zone, outfile="full_plate/copasi/p15_test_zone_5_5_3x3.csv")
create_sbml(zone, CompModel(), zone_params, outfile=zone_out)
