# Find the location of genes on a plate.
import numpy as np
from cans2.parser import get_genes


def get_coords(indices, cols):
    """Return coords starting (0, 0)

    indices : indices starting from zero

    cols : number of columns in array

    """
    r = indices // cols
    c = indices - r*cols
    return (r, c)

genes = np.array(get_genes("../../../../data/p15/ColonyzerOutput.txt")[:384])

locs = np.where(genes == "HAP4")
coords = [get_coords(index, 24) for index in locs]
print(locs)
print(coords)
