"""Simulate data for a zone of an existing plate.

Parameters for the existing plate are read from a json file.

"""
from cans2.model import CompModel
from cans2.zoning import sim_zone, save_zone_as_json


if __name__ == '__main__':
    # Save 5x5 and 2x1 plate parameters from a larger simulation.
    plate_file = '16x24_comp_model/full_plate.json'
    # Model to resimulate.
    model = CompModel()

    zone_coords = [(6, 11), (7, 13)]
    zone_dims = [(5, 5), (2, 1)]
    outfiles = ['16x24_comp_model/5x5_zone.json',
                '16x24_comp_model/2x1_zone.json']
    for coords, dims, outfile in zip(zone_coords, zone_dims, outfiles):
        rows = dims[0]
        cols = dims[1]
        zone = sim_zone(plate_file, model, coords, rows, cols)
        save_zone_as_json(zone, model, coords, plate_file, outfile)
