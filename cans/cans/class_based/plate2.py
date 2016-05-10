class Plate:

    def __init__(rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.find_neighbourhood()
        self.data = data
        # Is data going to be a dictionary of observation times and
        # cell measurements? Let's assume so.
        if data is not None:
            self.c_meas = data['c_meas']
            self.times = data['times']
        else:
            self.c_meas = None
            self.times = None
        # Specicial attributes for simulated data.
        self.sim_amounts = None
        self.sim_params = None
        # A plate has Cultures


    def find_neighbourhood():
    """Return a list of tuples of neighbour indices for each culture."""
    neighbourhood = []
    for i in range(self.no_cultures):
        neighbours = []
        if i // self.cols:
            # Then not in first row.
            neighbours.append(i - self.cols)
        if i % self.cols:
            # Then not in first column.
            neighbours.append(i - 1)
        if (i + 1) % self.cols:
            # Then not in last column.
            neighbours.append(i + 1)
        if i < (self.rows - 1 )*self.cols:
            # Then not in last row.
            neighbours.append(i + self.cols)
        neighbourhood.append(tuple(neighbours))
    return neighbourhood
