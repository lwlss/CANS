import numpy as np


from cans2.model import IndeModel


def add_b_bound(plate, model, i, j, bounds, bound):
    """Add a bound given i and j of culture on plate.

    i and j should start at zero.
    bound should be a tuple.

    """
    index = model.b_index + i*plate.cols + j
    bounds[index] = bound


class Guesser(object):
    def __init__(self, plate, model, area_ratio=1.0, C_ratio=1e-5):
        """Instantiate Guesser with a Plate and Model.

        plate : CANS Plate object.

        model : CANS Model object.

        area_ratio : Ratio of (edge culture area / internal culture
        area). This is not the area of the cultures, which are assumed
        equal, but the area of agar that is closest to, and could be
        said to belong to, a culture. (Assumed equal to Ne/Ni.) Used
        if model is CompModelBC but ignored if model is CompModel.

        C_ratio : (Init cell amounts / final cell amounts). The user
        must provide a guess for the ratio based on knowledge about
        the experiment. The data does not have resolution enough to
        determine starting cell amounts and, unlike for nutrient
        amounts, there is no easy way to infer a guess without
        fitting.

        """
        self.plate = plate
        self.model = model
        self.area_ratio = float(area_ratio)
        self.C_ratio = float(C_ratio)


    def _guess_init_N(self):
        """Guess starting amounts of Nutrients.

        If the model treats all cultures as having the same starting
        amount of nutrients (i.e. if model.species_bc contains an
        empty string at the index of species "N"), returns a single
        element list [N_all]. If the model contains separate
        parameters for initial nutrients in internal and edge
        cultures, returns a two element list of initial nutrient
        amounts [Ni, Ne].

        """
        no_tps = len(self.plate.times)
        # Assuming complete reactions and relatively small starting
        # amounts of cells, total nutrient amount is equal to the
        # total final cell amount.
        N_tot = np.sum(self.plate.c_meas[self.plate.no_cultures*(no_tps-1):])
        N_index = self.model.species.index("N")
        if self.model.species_bc[N_index]:
            # Number of internal and edge cultures.
            ni = len(self.plate.internals)
            ne = len(self.plate.edges)
            # Init nutrients in internal and edge cultures. Derived
            # from the following relationships: N_tot = ni*Ni + ne*Ne;
            # Ne = Ni*ratio.
            Ni = N_tot / (ni + ne*self.area_ratio)
            Ne = (N_tot - ni*Ni) / ne
            return [Ni, Ne]
        else:
            N_all = N_tot / float(self.plate.no_cultures)
            return [N_all]


    # Could write additional code to remove very slow or non-growing
    # cultures from the average. For plate 15, however, most cells
    # exhibit some growth. We hope to get a better guess from fits of
    # the logistic equivalent of imaginary neighbour model anyway so
    # don't worry too much.
    def _guess_init_C(self):
        """Guess initial cell amounts.

        Returns a single element list containing an intial guess of
        cell amounts applicable to all cultures on the plate.

        C_0 guess may be revised after fitting the logistic equivalent
        or imaginary neighbour model but those methods also require a
        guess.

        """
        # Just take ratio of average of final cells without special
        # treatment of edge and internal cultures because, for typical
        # dilution methods, the ratio is likely to be a fairly rough
        # guess anyway. We will revise the guess anyway after fitting
        # the logistic equivalent of imaginary neighbour
        # model. Previously
        # (https://boo62.github.io/blog/fits-of-overlapping-5x5-zones/),
        # I carried out many fits using a grid of initial guesses and
        # these were not very dependent on the accuracy of the initial
        # guess of C_0.
        no_tps = len(self.plate.times)
        final_Cs = self.plate.c_meas[self.plate.no_cultures*(no_tps-1):]
        C_0 = np.mean(final_Cs)*self.C_ratio
        return [C_0]


    def _bound_init_amounts(self, guess, C_doubt=1e3, N_doubt=2):
        """Return list of bounds for init amounts.

        guess : List of guesses of init amounts.

        C_doubt : Factor for Uncertainty in guess of initial cell
        amounts. Divides and multiplies the initial guess of C_0 to create
        lower and upper bounds.

        N_doubt : Factor for Uncertainty in guess of initial nutrient
        amounts. Divides and/or multiplies the initial guess(es) to
        create lower and upper bounds. See code for exact usage.

        """
        # Bound cells.
        bounds = [(guess[0]/C_doubt, guess[0]*C_doubt)]
        # Bound nutrients.
        N_index = self.model.species.index("N")
        if not self.model.species_bc[N_index]:
            # Bound N_0. This is strongly coupled to the final amount
            # of cells so, assuming relatively small intial cell
            # amounts, we can be fairly strict with a lower bound. The
            # upper bound depends on whether the reactions are
            # complete at the time of the final cell measurement.
            bounds.append((guess[1]*0.9, guess[1]*N_doubt))
        else:
            # Bound N_0 and NE_0. Cannot be as strict with N_0 in this
            # case as the minimum value is dependent on the accuracy
            # of the area_ratio and the level of diffusion between
            # edges and internals which is unknown. If we were sure of
            # the value of area_ratio and that all nutrients were used
            # up we could bound one limit of each amount using the
            # guess of the other amount. I choose not to be so strict.
            bounds.append((guess[1]/N_doubt, guess[1]*N_doubt))
            bounds.append((guess[2]/N_doubt, guess[2]*N_doubt))
        return bounds


    def _sep_by_N_0(self, param_guess, bounds):
        """Separate parameter guesses and bounds by N_0 guess.

        This way guesses and bounds can be used to fit single
        cultures.

        param_guess and bounds should be numpy arrays with N_0 indices
        starting at one.

        Returns lists of length one if there is one N_0 in the model
        and lists of length two if there is is also an N_0 for edge
        cultures.

        """
        N_index = self.model.species.index("N")
        if self.model.species_bc[N_index]:
            param_guess = np.array([param_guess.delete[2], param_guess.delete[1]])
            bounds = np.array([bounds.delete[2], bounds.delete[1]])
        else:
            param_guess = np.array([param_guess])
            bounds = np.array([bounds])
        return param_guess, bounds


    def _get_top_half_C_f_ests(self, all_ests):
        """Return np.array of estimates for Cultures with highest final Cells.

        If the number of cultures is odd return the larger portion.

        all_ests : estimates for all cultures.

        """
        no_tps = len(self.plate.times)
        # Measured final cell amounts.
        C_fs = self.plate.c_meas[self.plate.no_cultures*(no_tps-1):]
        C_f_sorted = [est for (C_f, est) in sorted(zip(C_fs, all_ests))]
        # Indices of cultures sorted by C_f. May use later.
        # labelled_C_fs = [tup for tup in enumerate(C_fs)]
        # ordered_C_fs = sorted(labelled_C_fs, key=lambda tup: tup[1])
        # C_f_sorted_indices = [i for i, C in ordered_C_fs]
        top_half_ests = C_f_sorted[self.plate.no_cultures//2:]
        return np.array(top_half_ests)


    def _process_quick_ests(self, quick_mod, est_name):
        """Process estimates from quick fits.

        Take a mean of estimated C_0s, use the N_0 guess(es) made from
        average final cell amounts, and add on b guesses from the
        quick fit.

        quick_mod : Instance of the model used for quick fit.

        est_name : Name of the Culture attribute where estimated
        values are stored. Either "log_est" or "im_neigh_est".

        """
        # Allow to raise AttributeError if bad est_name.
        all_ests = np.array([getattr(c, est_name).x for c in self.plate.cultures])
        b_ests = all_ests[:, quick_mod.b_index]

        # Select estimates to use for taking average of init
        # C_0. Cultures with a zero b estimate have arbitrary init
        # amount ests. It is possible that more than half of cultures
        # have a zero b estimate, in which case we would have to
        # remove more than just the lowest half. If the issue is due
        # to the plate having gaps we could use plate.empties to deal
        # with this.
        included_ests = self._get_top_half_C_f_ests(all_ests)
        C_0_mean = [np.mean(included_ests[:, 0])]

        # Use N_0 guess(es) made from average final cell amounts.
        N_0_guess = self._guess_init_N()
        # N_guess may be a single value. We need an iterable to
        # concatenate with guesses of other parameters.
        try:
            list(N_0_guess)
        except TypeError:
            N_0_guess = [N_0_guess]

        # N_guess may be a single value. We need an iterable to
        # concatenate with other guesses.
        new_guess = np.concatenate((C_0_mean, N_0_guess, b_ests))
        return np.array(new_guess)


    # It would be possible to find specific estimates for b, before
    # any fitting, by scaling an average guess by final cell
    # amounts. Alternatively we could guess a maximum and scale
    # towards zero. However, the factor by which to scale would depend
    # on kn and the absolute value of the average (and possibly also
    # initial cell amounts?). I hope to find reasonable geusses
    # without the need for this.
    def quick_fit_log_eq(self, b_guess, C_doubt=1e3, N_doubt=2.0):
        """Guess b by fitting the logistic equivalent model.

        Returns guesses for all parameters in self.model for a
        self.model of CompModel or CompModelBC.

        Fits to individual cultures. For speed, there is no collective
        fitting of plate level parameters, e.g. initial
        amounts. Instead, an average can be taken after the individual
        fits. Guesses for C_0 and individual b parameters result from
        fitting, whereas guesses for N_0 are infered from average
        final measurements and not updated after fitting.

        b_guess : guess for b parameter. The same for all cultures.

        C_doubt : Factor for Uncertainty in guess of initial cell
        amounts. Divides and multiplies the initial guess of C_0 to
        create lower and upper bounds.

        N_doubt : Factor for Uncertainty in guess of initial nutrient
        amounts. Divides and/or multiplies the initial guess(es) to
        create lower and upper bounds. See code for exact usage.

        """
        C_0_guess = self._guess_init_C()
        # This N_0_guess is not used in logistic equivalent fits but
        # is returned in the new_guess; logistic estimated N_0s are not
        # realistic for the competition model. The number of elements
        # depends on whether the model has a separate N_0 for edge
        # cultures.
        N_0_guess = self._guess_init_N()
        amount_guess = np.append(C_0_guess, N_0_guess)
        first_guess = np.append(amount_guess, b_guess)

        # Use final amounts of cells as inital guesses of nutrients
        # because logistic equivalent growth is governed by N + C ->
        # 2C, there is no diffusion, and C_0 is assumed to be
        # relatively small.
        tps = len(self.plate.times)
        C_fs = self.plate.c_meas[self.plate.no_cultures*(tps-1):]
        log_eq_N_0_guesses = C_fs
        log_eq_guesses = [C_0_guess + [N_0, b_guess] for N_0 in log_eq_N_0_guesses]

        # For logistic equivalent fit fix C_0 and allow N_0 and b to
        # vary freely. Could also try varying C_0 freely but would
        # likely get inconsistent estimates. It would perhaps be
        # better to fit C_0 collectively but this would be much
        # slower. [C_0, N_0, b]
        log_eq_bounds = [(C_0_guess[0], C_0_guess[0]), (0.0, None), (0.0, None)]

        log_eq_mod = IndeModel()
        print(log_eq_bounds)
        for guess, culture in zip(log_eq_guesses, self.plate.cultures):
            culture.log_est = culture.fit_model(log_eq_mod,
                                                param_guess=guess,
                                                bounds=log_eq_bounds)

        new_guess = self._process_quick_ests(log_eq_mod, est_name="log_est")

        # Insert nan at index of kn.
        kn_index = self.model.params.index("kn")
        new_guess = np.insert(new_guess, kn_index, np.nan)

        return new_guess


    def quick_fit_imag_neighs(self, plate):
        """Guess b by fitting the imaginary neighbour model."""
        pass


##########################


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


    def _guess_b(self):
        # fit independent model fixing with C_0 and N_0 guesses and
        # take average b. Could just select those closest to C_f =
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
        # guess b
        # arrange guess according to index in model.
        return guess


    def nparray_guess(self, plate, guess):
        guess_list = np.zeros(self.model.b_index - 1)# + plate.no_cultures])
        for k, v in guess.items():
            index = self.model.params.index(k)
            guess_list[index] = v
        return guess_list
        # Need to make guesses or kn and bs (maybe as a list with a
        # guess for each b).


    def get_bounds(self, plate, guess, factor=0.5):

        """A list of tuples for each parameter in the model.

        Must be suitable for scipy.optimize.minimize.

        """
        no_params = self.model.b_index + plate.no_cultures
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
        return np.asarray(bounds)



if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import linregress


    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter
    from cans2.cans_funcs import round_sig


    def fit_C_f_var_vs_kn(kns, times, model, guesser, rows=16,
                          cols=24, b_mean=50.0, b_var=25.0):
        C_f_vars = []
        for kn in kns:
            # Simulate a plate and data
            plate1 = Plate(16, 24)
            plate1.times = times
            true_params = {'N_0': 0.1, 'kn': kn}
            true_params['C_0'] = true_params['N_0']/10000
            plate1.set_sim_data(model, b_mean, b_var, true_params)

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
    # make good (enough) guesses for b then we can guess kn (and
    # possibly constrain it).
    rows = 16
    cols = 24
    times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    comp_guesser = Guesser(comp_model)
    comp_plotter = Plotter(comp_model)


    kns = np.array([x/100 for x in range(31)])
    # kns = np.array([0.5, 0.1])


    # plot cf vs kn for two different b dists and linear fit and eqn.
    def plot_fits(kns, times, model, guesser, bows, cols, b_dists):
        fits = []
        for b_mean, b_var in b_dists:
            fit = fit_C_f_var_vs_kn(kns, times, comp_model,
                                    comp_guesser, rows=rows,
                                    cols=cols, b_mean=b_mean,
                                    b_var=b_var)
            fits.append(fit)

        col = 1
        colors = ['k', 'r', 'b', 'g', 'y']
        for b_dist, fit in zip(b_dists, fits):
            plt.plot(kns, fit[2], label="b ~ N({0}, {1})".format(*b_dist),
                     marker='x', linestyle='None', color=colors[col])
            plt.plot(kns, kns*fit[0] + fit[1], color=colors[col],
                     label="y = {0}x + {1}".format(round_sig(fit[0]),
                                                   round_sig(fit[1])))
            col += 1
        plt.title("Fits of C_final variance vs kn for different b distributions")
        plt.xlabel("kn")
        plt.ylabel("Variance in final cell amount")
        plt.legend(loc='best')
        plt.show()
        plt.close()

    b_dists = [(50.0, 25.0), (100.0, 50.0)]
    plot_fits(kns, times, comp_model, comp_guesser, rows, cols, b_dists)

    # Study b_mean and b_var effect on gradient
    b_means = [20.0, 40.0, 60.0, 80.0, 100.0]
    b_vars = [x*10.0 for x in range(8)]

    # vary b_mean and plot against gradient in C_f_var vs kn.
    b_mean_m_c = []
    for b_mean in b_means:
        b_mean_m_c.append(list(fit_C_f_var_vs_kn(kns, times, comp_model,
                                                 comp_guesser, rows=rows,
                                                 cols=cols, b_mean=b_mean)[:2]))
    b_mean_m_c = np.array(b_mean_m_c)

    # vary b_var and plot against gradient in C_f_var vs kn.
    b_var_m_c = []
    for b_var in b_vars:
        b_var_m_c.append(list(fit_C_f_var_vs_kn(kns, times, comp_model,
                                                comp_guesser, b_var=b_var)[:2]))
    b_var_m_c = np.array(b_var_m_c)

    print(b_mean_m_c)
    print(b_var_m_c)
    # plot m against b_mean
    plt.plot(b_means, b_mean_m_c[:, 0], linestyle='None', marker='x')
    plt.title("Gradient vs b mean")
    plt.ylabel("m")
    plt.xlabel("b mean")
    plt.show()
    plt.close()

    # plot m against b_var
    plt.plot(b_vars, b_var_m_c[:, 0], linestyle='None', marker='x')
    plt.title("Gradient vs b var")
    plt.ylabel("m")
    plt.xlabel("b var")
    plt.show()
    plt.close()
