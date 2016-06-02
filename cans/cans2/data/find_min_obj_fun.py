import json
import glob
import os


from math import log10, floor


# http://stackoverflow.com/a/3413529
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)

rows = 16
cols = 24
factr_pow = "*"    # "*" for all

# "init_guess_x/" dirs containing "stop_factr_10ey.json" files.
path = "sim_fits/{0}x{1}_comp_model/*/stop_factr_10e{2}.json"
path = path.format(rows, cols, factr_pow)

obj_fun = float('inf')
obj_funs = []
for filename in glob.glob(path):
    with open(filename, 'r') as f:
        data = json.load(f)
    obj_funs.append((filename, data['obj_fun_val']))

obj_funs = sorted(obj_funs, key=lambda tup: tup[0])
obj_funs = sorted(obj_funs, key=lambda tup: tup[1])

# Test sorting
obj_fun_val = 0.0
for obj_fun in obj_funs:
    assert obj_fun_val <= obj_fun[1]
    obj_fun_val = obj_fun[1]

# Print best fits
for obj_fun in obj_funs[:9]:
    # with open(obj_fun[0], 'r') as f:
    #     data = json.load(f)
    print(obj_fun)
    # print((str(round_sig(data['param_devs'][0], sig=2)) + " "
    #        + str(round_sig(data['param_devs'][1], sig=2)) + " "
    #        + str(round_sig(data['param_devs'][2], sig=2)) + " "
    #        + str(round_sig(data['param_devs'][3], sig=2))))
    # print(round_sig(obj_fun[1]))
