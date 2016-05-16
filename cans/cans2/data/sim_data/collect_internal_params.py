"""Find the sim params of a grid inside a plate."""
import numpy as np
import json


from cans2.cans_funcs import get_zone


def zone_plate(resim=True):
    """Return a plate from a zone of a larger plate.

    If resim == True, resimulate from the underlying
    parameters. Otherwise, return the c_measures from the larger
    plate.

    """
    pass

def zone_params(plate_file, coord, rows, cols):
    """Return params from a zone of a larger plate."""
    # Read in the full plate.
    with open(plate_file, 'r') as f:
        plate_data = json.load(f)


assert coords[0] + rows <= big_rows
assert coords[1] + cols <= big_cols

# Read in the full plate.
with open(plate_file, 'r') as f:
    plate_data = json.load(f)

times = plate_params['times']
plate_params = plate_data['sim_params']
plate_rs = plate_params[3:]
assert len(plate_rs) == big_rows*big_cols

# Convert the plate r parameters to an array.
plate_array = np.array(plate_rs)
plate_array.shape = (big_rows, big_cols)
for row in range(big_rows):
    assert all(plate_array[row, :] == plate_rs[row*big_cols:(row+1)*big_cols])

# Now slice the plate array to get the required zone.
zone = get_zone(plate_array, coords, rows, cols)
params = plate_params[:3] + zone.flatten().tolist()


if __name__ == '__main__':
    # Save a 5x5 and 2x1 plate to file.
    from cans2.plate import Plate

    zone1 = plate(rows, cols)

    # Rows and cols of first culture in sought zone (starts at (0, 0)).
    coords = (6, 11)
    # Number of rows and colums for internal zone.
    rows = 5
    cols = 5


    # Rows and cols of full plate.
    big_rows = 16
    big_cols = 24
    plate_file = '{0}x{1}_comp_model/mean_5_var_3.json'.format(big_rows, big_cols)
