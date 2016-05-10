class BasePlate:
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
        # Attributes for simulated data.
        self.sim_amounts = None
        self.sim_params = None


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


class Plate(BasePlate):
    def __init__(self, rows, cols, data=None):
        super(Plate, self).__init__(rows, cols, data)
        if self.data is not None:
            # Feed data to Cultures. Depends on form of data but would
            # like a dictionary with times and c_meas.
            pass
        else:
            self.cultures = [Culture() for i in range(self.no_cultures)]


    def add_cultures_sim_data(self):
        for i, culture in enumerate(self.cultures):
            # May need to pass the model used in order to
            # generalize. Then we can replace 2 with the number of
            # species and also provide parameters used for the
            # simulations and other amounts (e.g. N). This is not
            # possible with real data and not really necessary
            # simulated data.
            no_species = int(len(self.sim_amounts[0])/self.no_cultures)
            # culture.sim_amounts = self.sim_amounts[:, i*2:(i+1)*2]
            culture.c_meas = self.sim_amounts[:, i*no_species].flatten()
            culture.times = self.times
            # culture.sim_params = self.sim_params[0:]


class Culture(BasePlate):
    def __init__(self, data=None):
        super(Culture, self).__init__(1, 1, data)

if __name__ == '__main__':
    plate1 = Plate(3, 3)
    culture1 = Culture()
    print(plate1.neighbourhood)
    print(culture1.neighbourhood)
