import json

from cans2.model import CompModelBC
from cans2.cans_funcs import cans_to_json, dict_to_json

# rows, cols = (16, 24)

data_path = "sim_plate_with_fit_{0}x{1}.json".format(rows, cols)
with open(data_path, "r") as f:
    data = json.load(f)

model = CompModelBC()
data["model"] = model.name
data["species"] = model.species
data["params"] = model.species
data = dict_to_json(data)

with open(data_path, "w") as f:
    json.dump(data, f, indent=4, sort_keys=True)
