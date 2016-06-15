import json
import glob
import os
import csv

from math import log10, floor


# http://stackoverflow.com/a/3413529
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)

coords = (7, 13)
# coords = (9, 15)
rows = 5
cols = 5
argvs = [638, 1012, 440, 803]
middle_r = 18 # 6

# "init_guess_x/" dirs containing "stop_factr_10ey.json" files.
path = "results/p15_fits/coords_{0}_{1}_5x5_argv_{2}.json"
paths = [path.format(*(list(coords) + [argv])) for argv in argvs]

obj_fun = float('inf')
obj_funs = []
est_params = []
bounds = []
for argv, filename in zip(argvs, paths):
    with open(filename, 'r') as f:
        data = json.load(f)
    obj_funs.append((argv, data['obj_fun']))
    est_params.append((filename, data["comp_est"]))
    bounds.append((filename, data["bounds"]))

# Sort by filename then by value of objective function.
# obj_funs = sorted(obj_funs, key=lambda tup: tup[0])
# obj_funs = sorted(obj_funs, key=lambda tup: tup[1])

# Test sorting
# obj_fun_val = 0.0
# for obj_fun in obj_funs:
#     assert obj_fun_val <= obj_fun[1]
#     obj_fun_val = obj_fun[1]

table = []
r1 = ["Guess No.", "obj_f", "C_0", "N_0", "kn", "r_{0}".format(middle_r)]
table.append(r1)
# Print best fits
for obj_fun, params, bounds in zip(obj_funs[:9], est_params[:9], bounds[:9]):
    # with open(obj_fun[0], 'r') as f:
    #     data = json.load(f)
    print(bounds[1][:3])
    row = list(obj_fun) + params[1][:3] + [params[1][3 + middle_r]]
    row = [round_sig(val, 3) if not isinstance(val, int) else val for val in row]
    table.append(row)
    # print((str(round_sig(data['param_devs'][0], sig=2)) + " "
    #        + str(round_sig(data['param_devs'][1], sig=2)) + " "
    #        + str(round_sig(data['param_devs'][2], sig=2)) + " "
    #        + str(round_sig(data['param_devs'][3], sig=2))))
    # print(round_sig(obj_fun[1]))
print(table)

# with open('coords_{0}_{1}_ests.csv'.format(*coords), 'wb') as csvfile:
#     est_writer = csv.writer(csvfile, delimiter=',',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for r in table:
#         est_writer.writerow(r)
