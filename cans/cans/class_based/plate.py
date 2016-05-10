class Plate:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.no_cultures = rows*cols
        self.neighbourhood = self.find_neighbourhood()
        self.data = data
        # Is data going to be a dictionary of observation times and
        # cell measurements? Let's assume so.
        if data is not None:
            self.c_meas = data['c_meas']    # Should flatten as np.array
            self.times = data['times']
        else:
            self.c_meas = None    # Should flatten as np.array
            self.times = None
        # Specicial attributes for simulated data.
        self.sim_amounts = None
        self.sim_params = None
        # A plate has Cultures


    def find_neighbourhood(self):
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


class Culture(Plate):
    def __init__(self, data=None):
        super(Culture, self).__init__(1, 1, data)

if __name__ == '__main__':
    plate1 = Plate(3, 3)
    culture1 = Culture()
    print(plate1.neighbourhood)
    print(culture1.neighbourhood)
