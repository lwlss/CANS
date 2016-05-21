class Guesser:
    def __init__(self, model):
        self.model = model
        self.guess = {}


    def _guess_N_0(self, plate):
        # slice the last measure of C and take average
        # C_0 is 1/10,000 of this
        # Can also use these as lower bounds with current (C and N only) models.
        tps = len(plate.times)
        N_0_guess = np.mean(plate.c_meas[plate.no_cultures*(tps-1):])
        return N_0_guess


    def _guess_kn(self, plate):
        # Look at range of final cell values excluding zeros
        # Remove
        KN_FACTR = 4.5
        tps = len(plate.times)
        # Use maximum deviatiion of C_f from N_0
        max_c = max(plate.c_meas)
        c_range = max_c - self.guess['N_0']

        # or use mad of C_f to N_0 except for zero growers.  Only
        # really appropriate if growth has stopped which will not be
        # the case for very low kn where nutrients are still diffusing
        c_starts = plate.c_meas[:plate.no_cultures]
        c_finals = plate.c_meas[plate.no_cultures*(tps-1):]
        growers = [f for s, f in zip(c_starts, c_finals) if f > 10*s]
        # print(c_starts)
        # print(c_finals)
        # print(len(growers))
        growers_dev = np.mean(list(map(lambda x: abs(x-self.guess['N_0']), growers)))
        # print(growers_dev)
        # print(c_range)
        return growers_dev*KN_FACTR


    def _guess_r(self):
        # fit independent model fixing with C_0 and N_0 guesses and
        # take average r. Could just select those closest to C_f =
        # N_0.
        pass


    def make_guess(self, plate):
        params = self.model.params
        self.guess['N_0'] = self._guess_N_0(plate)
        # guess C_0
        self.guess['C_0'] = self.guess['N_0']/10000
        # guess kn
        self.guess['kn'] = self._guess_kn(plate)
        # guess r
        return self.guess


if __name__ == '__main__':
    import numpy as np
    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter


    plate1 = Plate(5, 5)
    plate1.times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    true_params = {'N_0': 0.1, 'kn': 1.0}
    true_params['C_0'] = true_params['N_0']/10000
    plate1.set_sim_data(comp_model, 50.0, 25.0, true_params)

    comp_guesser = Guesser(comp_model)
    guess = comp_guesser.make_guess(plate1)
    print(guess)

    # Could do with a plot_sim method
    comp_plotter = Plotter(comp_model)
    comp_plotter.plot_est(plate1, plate1.sim_params)
