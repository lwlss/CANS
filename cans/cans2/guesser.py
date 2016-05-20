class Guesser:
    def __init__(self, model):
        self.model = model


    def _guess_N_0(self, plate):
        # slice the last measure of C and take average
        # C_0 is 1/10,000 of this
        # Can also use these as lower bounds with current (C and N only) models.
        tps = len(plate.times)
        print(plate.c_meas)
        N_0_guess = np.mean(plate.c_meas[plate.no_cultures*(tps-1):])
        return N_0_guess

    def guess(self, plate):
        params = self.model.params
        guess = {}
        guess['N_0'] = self._guess_N_0(plate)
        guess['C_0'] = guess['N_0']/10000
        return guess

if __name__ == '__main__':
    import numpy as np
    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter


    plate1 = Plate(3, 3)
    plate1.times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    true_params = {'N_0': 0.1, 'kn': 0.2}
    true_params['C_0'] = true_params['N_0']/10000
    plate1.set_sim_data(comp_model, 50.0, 25.0, true_params)

    comp_guesser = Guesser(comp_model)
    guess = comp_guesser.guess(plate1)
    print(guess)


    # Could do with a plot_sim method
#    plate1.comp_est = plate1.fit_model(comp_model)
    comp_plotter = Plotter(comp_model)
    comp_plotter.plot_est(plate1, plate1.sim_params)
