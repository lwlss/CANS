import json
from cans2.model import CompModel

filename =

with open(filename, 'r') as f:
    data = json.load(f)

model = CompModel()

data['model_species'] = model.species


# with open(filename, 'w') as f:
#     json.dump()
