import numpy as np


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
        # arrange guess according to index in model.
        return guess


    def list_guess(self, plate, guess):
        guess_list = np.empty([1, self.model.r_index + plate.no_cultures])
        for k, v in guess.items():
            index = self.model.params.index(k)
            guess_list[index] = v
        # Need to make guesses or kn and rs (maybe as a list with a
        # guess for each r).


    def get_bounds(self, plate, guess, factor=0.5):
        """A list of tuples for each parameter in the model.

        Must be suitable for scipy.optimize.minimize.

        """
        no_params = self.model.r_index + plate.no_cultures
        # First set all bounds greater than zero
        bounds = [(0.0, None) for param in range(no_params)]
        # Then change the bounds for parameters for which there is a
        # guess.
        for k, v in guess.items():
            assert k in self.model.params
            if k == "C_0":
                # Bounds on C_0 need to be looser as we don't really
                # know.
                index = self.model.params.index(k)
                bounds[index] = (v/10 , v*10)
            elif k == "N_0":
                # N_0 is always underestimated unless all reactions
                # are finished.
                index = self.model.params.index(k)
                bounds[index] = (v, 2*v)
            elif k == "kn":
                pass
        return bounds



if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import linregress


    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter
    from cans2.cans_funcs import round_sig


    def fit_C_f_var_vs_kn(kns, times, model, guesser, rows=16,
                          cols=24, r_mean=50.0, r_var=25.0):
        C_f_vars = []
        for kn in kns:
            # Simulate a plate and data
            plate1 = Plate(16, 24)
            plate1.times = times
            true_params = {'N_0': 0.1, 'kn': kn}
            true_params['C_0'] = true_params['N_0']/10000
            plate1.set_sim_data(model, r_mean, r_var, true_params)

            # comp_plotter.plot_est(plate1, plate1.sim_params)

            # The variance in final cell volumes is temporarily our
            # guess for kn.
            guess = guesser.make_guess(plate1)
            C_f_vars.append(guesser._get_growers_C_f_var(plate1, guess['C_0']))

        # Fit a line by least squares.
        A = np.vstack([kns, np.ones(len(kns))]).T
        m, c = np.linalg.lstsq(A, C_f_vars)[0]
        return m, c, C_f_vars


    # For fixed r_mean and r_var, the variance in final cell
    # measurement follows a linear relationship with kn. If we can
    # make good (enough) guesses for r then we can guess kn (and
    # possibly constrain it).
    rows = 16
    cols = 24
    times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    comp_guesser = Guesser(comp_model)
    comp_plotter = Plotter(comp_model)


    kns = np.array([x/100 for x in range(31)])
    # kns = np.array([0.5, 0.1])


    # plot cf vs kn for two different r dists and linear fit and eqn.
    def plot_fits(kns, times, model, guesser, rows, cols, r_dists):
        fits = []
        for r_mean, r_var in r_dists:
            fit = fit_C_f_var_vs_kn(kns, times, comp_model,
                                    comp_guesser, rows=rows,
                                    cols=cols, r_mean=r_mean,
                                    r_var=r_var)
            fits.append(fit)

        col = 1
        colors = ['k', 'r', 'b', 'g', 'y']
        for r_dist, fit in zip(r_dists, fits):
            plt.plot(kns, fit[2], label="r ~ N({0}, {1})".format(*r_dist),
                     marker='x', linestyle='None', color=colors[col])
            plt.plot(kns, kns*fit[0] + fit[1], color=colors[col],
                     label="y = {0}x + {1}".format(round_sig(fit[0]),
                                                   round_sig(fit[1])))
            col += 1
        plt.title("Fits of C_final variance vs kn for different r distributions")
        plt.xlabel("kn")
        plt.ylabel("Variance in final cell amount")
        plt.legend(loc='best')
        plt.show()
        plt.close()

    r_dists = [(50.0, 25.0), (100.0, 50.0)]
    plot_fits(kns, times, comp_model, comp_guesser, rows, cols, r_dists)

    # Study r_mean and r_var effect on gradient
    r_means = [20.0, 40.0, 60.0, 80.0, 100.0]
    r_vars = [x*10.0 for x in range(8)]

    # vary r_mean and plot against gradient in C_f_var vs kn.
    r_mean_m_c = []
    for r_mean in r_means:
        r_mean_m_c.append(list(fit_C_f_var_vs_kn(kns, times, comp_model,
                                                 comp_guesser, rows=rows,
                                                 cols=cols, r_mean=r_mean)[:2]))
    r_mean_m_c = np.array(r_mean_m_c)

    # vary r_var and plot against gradient in C_f_var vs kn.
    r_var_m_c = []
    for r_var in r_vars:
        r_var_m_c.append(list(fit_C_f_var_vs_kn(kns, times, comp_model,
                                                comp_guesser, r_var=r_var)[:2]))
    r_var_m_c = np.array(r_var_m_c)

    print(r_mean_m_c)
    print(r_var_m_c)
    # plot m against r_mean
    plt.plot(r_means, r_mean_m_c[:, 0], linestyle='None', marker='x')
    plt.title("Gradient vs r mean")
    plt.ylabel("m")
    plt.xlabel("r mean")
    plt.show()
    plt.close()

    # plot m against r_var
    plt.plot(r_vars, r_var_m_c[:, 0], linestyle='None', marker='x')
    plt.title("Gradient vs r var")
    plt.ylabel("m")
    plt.xlabel("r var")
    plt.show()
    plt.close()
