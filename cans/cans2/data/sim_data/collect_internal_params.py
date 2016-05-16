"""Find the sim params of a grid inside a plate."""
import numpy as np
import json


from cans2.cans_funcs import get_zone


def plate_zone(resim=True):
    """Return a plate from a zone of a larger plate.

    If resim == True, resimulate from the underlying
    parameters. Otherwise, return the c_measures from the larger
    plate.

    """
    pass


def get_zone_params(plate_file, coords, rows, cols):
    """Return params for a zone of a plate saved as json.

    Returns plate level parameters and in a flattened list.

    """
    # Read in the full plate.
    with open(plate_file, 'r') as f:
        plate_data = json.load(f)

    plate_rows = plate_data['rows']
    plate_cols = plate_data['cols']
    times = plate_data['times']
    r_index = len(plate_data['model_params']) - 1
    plate_params = plate_data['sim_params']
    plate_rs = plate_params[r_index:]

    assert coords[0] + rows <= plate_rows
    assert coords[1] + cols <= plate_cols
    assert len(plate_rs) == plate_rows*plate_cols

    # Convert the plate r parameters to an array.
    plate_array = np.array(plate_rs)
    plate_array.shape = (plate_rows, plate_cols)
    for row in range(plate_rows):
        assert all(plate_array[row, :] ==
                   plate_rs[row*plate_cols:(row+1)*plate_cols])

    # Now slice the plate array to get the required zone.
    zone = get_zone(plate_array, coords, rows, cols)
    params = plate_params[:r_index] + zone.flatten().tolist()
    return params


if __name__ == '__main__':
    # Save a 5x5 and 2x1 plate to file.

    plate_file = '16x24_comp_model/mean_5_var_3.json'

    zone_5x5 = get_zone_params(plate_file, coords=(6, 11),
                               rows=5, cols=5)
    # zone_2x1 = get_zone_params(plate_file, coords=(6, 11),
    #                            rows=2, cols=1)

    print(zone_5x5)
