class Guesser:
    def __init__(self, model):
        self.model = model


    def _guess_N_0(self, plate):
        # slice the last measure of C and take average
        # C_0 is 1/10,000 of this
        # Can also use these as lower bounds with current (C and N only) models.
        tps = len(plate.times)
        N_0_guess = np.mean(plate.c_meas[plate.no_cultures*(tps-1):])
        return N_0_guess


    def _get_growers(self, plate, C_0_guess):
        pass


    def _get_growers_C_f_var(self, plate, C_0_guess):
        no_tps = len(plate.times)
        C_finals = plate.c_meas[plate.no_cultures*(no_tps - 1):]
        # Use C_0 guess not C_0_meas due to resolution to discard
        # non-growers.
        C_f_growers = (f for f in C_finals if f > 100*C_0_guess)
        C_f_var = np.var(list(C_f_growers))
        return C_f_var

    
    def _guess_kn(self, plate, C_0_guess):
        pass


    def _guess_r(self):
        # fit independent model fixing with C_0 and N_0 guesses and
        # take average r. Could just select those closest to C_f =
        # N_0.
        pass


    def make_guess(self, plate):
        params = self.model.params
        guess = {}
        guess['N_0'] = self._guess_N_0(plate)
        # guess C_0
        guess['C_0'] = guess['N_0']/10000
        # guess kn
        # get C_f_var for growers
        #C_f_var = self._get_growers_C_f_var(plate, guess['C_0'])
        # guess r
        return guess


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import linregress


    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter


    def fit_C_f_var_vs_kn(kns, times, model, guesser, rows=16,
                          cols=24, r_mean=50.0, r_var=25.0):
        C_f_vars = []
        for kn in kns:
            # Simulate a plate and data
            plate1 = Plate(16, 24)
            plate1.times = times
            true_params = {'N_0': 0.1, 'kn': kn}
            true_params['C_0'] = true_params['N_0']/10000
            plate1.set_sim_data(model, 50.0, 25.0, true_params)

            # comp_plotter.plot_est(plate1, plate1.sim_params)

            # The variance in final cell volumes is temporarily our
            # guess for kn.
            guess = guesser.make_guess(plate1)
            C_f_vars.append(guesser._get_growers_C_f_var(plate1, guess['C_0']))

        # Fit a line by least squares.
        A = np.vstack([kns, np.ones(len(kns))]).T
        m, c = np.linalg.lstsq(A, C_f_vars)[0]
        return m, c


    rows = 16
    cols = 24
    times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    comp_guesser = Guesser(comp_model)
    comp_plotter = Plotter(comp_model)

    kns = [x/100 for x in range(31)]

    m, c = fit_C_f_var_vs_kn(kns, times, comp_model, comp_guesser,
                             16, 24, r_mean=r_mean, r_var=r_var)
    print(m, c)

    r_means = [20.0, 40.0, 60.0, 80.0, 100.0]

    r_vars = [x*10.0 for x in range(8)]


    # vary r_mean and plot against gradient in C_f_var vs kn.
    m_c = []
    for r_mean in r_means:


    # vary r_var and plot against gradient in C_f_var vs kn.


        # plt.plot(kns, C_f_vars, label="Final Cells var", marker="x", linestyle="None")
        # plt.legend(loc='best')
        # plt.show()
        # plt.close()

#     var_res = np.vstack([res[:, 0], np.ones(len(res[:, 0]))]).T
#     print(var_res)


# kn ~ cf_var - r_var?
