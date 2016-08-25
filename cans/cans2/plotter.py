import numpy as np
import matplotlib.pyplot as plt
import copy
import itertools


from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib import rc


from cans2.plate import Plate
from cans2.zoning import get_plate_zone, sim_and_get_zone_amounts, get_zone_amounts, get_qfa_R_zone
from cans2.process import spearmans_rho, calc_b, calc_N_0, least_sq
from cans2.model import IndeModel



class Plotter(object):

    def __init__(self, model, font_size=32.0, title_font_size=36.0,
                 legend_font_size=26.0, lw=3.0, ms=10.0, mew=2.0,
                 labelsize=20, xpad=20, ypad=20, units=None,
                 species=None, fig_settings=None, legend_cols=1,
                 bbox=(1.0, -0.2), title_height=0.955):
        """Initialise plotter and settings.

        figure_setting : (dict) kwargs (figsize, etc.) to be unpacked
        and passed plt.figure().

        legend_cols : (int) number of columns to use in legend.

        bbox : (tup) bbox_to_anchor setting for legend position.
        """
        self.model = model
        # Can decide on other colours when adding models with more species.
        self.colours = ['b', 'y', 'r', 'g']
        self.linestyles = ['-', '--', '-.', ':']
        self.c_meas_colors = ['k', 'r', 'c', 'm']
        self.font_size = font_size
        self.title_font_size = title_font_size
        self.legend_font_size = legend_font_size
        self.lw = lw
        self.ms = ms
        self.mew = mew
        self.labelsize = labelsize    # Font size of major tick labels
        # Gap between axes and x and y labels
        self.xpad = xpad
        self.ypad = ypad
        if units is None:    # List of unit labels
            self.units = ["(d)", "(AU)"]
        else:
            self.units = units
        if species is not None:
            self.species = species
        else:
            self.species = {
                "C": "Cells",
                "N": "Nutrients",
                "S": "Signal",
            }
        self.fig_settings = fig_settings
        self.legend_cols = legend_cols
        self.bbox = bbox
        self.title_height = title_height


    def _find_ymax(self, amounts):
        ymax = np.amax(amounts)
        ymax = np.ceil(ymax*10)/10
        return ymax


    def _make_grid(self, plate, amounts, sim, title, vis_ticks):
        """Make a ractangular grid of axes.

        Each axis may represent a culture in an QFA array.

        vis_ticks : (bool) Whether to plot values on axes. For large
        arrays becomes cluttered.
        """
        rows = plate.rows
        cols = plate.cols
        if sim:
            ymax = self._find_ymax(np.append(amounts, plate.sim_amounts))
        else:
            ymax = self._find_ymax(np.append(amounts, plate.c_meas))
        if self.fig_settings is None:
            fig = plt.figure()
        else:
            fig = plt.figure(**self.fig_settings)
        # http://stackoverflow.com/a/36542971
        # Add big axes and hide frame.
        fig.add_subplot(111, frameon=False)
        # Hide tick and tick label of the big axes.
        plt.tick_params(labelcolor='none', top='off',
                        bottom='off', left='off', right='off')
        plt.xlabel('Time {0}'.format(self.units[0]), fontsize=self.font_size,
                   labelpad=self.xpad)
        plt.ylabel('Amount {0}'.format(self.units[1]), fontsize=self.font_size,
                   labelpad=self.ypad)
        grid = AxesGrid(fig, 111, nrows_ncols=(rows, cols),
                        axes_pad=0.1, aspect=False, share_all=True)
        for i, ax in enumerate(grid):
            ax.set_ylim(0.0, ymax)
            ax.grid()

            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(self.labelsize)
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(self.labelsize)

            if not vis_ticks:
                plt.setp(ax.get_xticklabels(which="both"), visible=False)
                plt.setp(ax.get_yticklabels(which="both"), visible=False)

        #rc('text', usetex=True)
        fig.suptitle(title, fontsize=self.title_font_size, y=self.title_height)

        return fig, grid


    def _hide_last_ticks(self, grid, rows, cols):
        for i, ax in enumerate(grid):
            # Remove last tick values.
            if i + 1 > (rows - 1)*cols:
                # Then in last row.
                plt.setp(ax.get_xticklabels(which="both")[-1], visible=False)
            if not i % cols:
                # Then in first column.
                plt.setp(ax.get_yticklabels(which="both")[-1], visible=False)


    def plot_qfa_R_logistic_fit(self, log_plate, log_params, coords,
                                rows, cols, title="QFA R logistic fit"):
        """Plot logistic model fits from the QFA R package.

        This model has parameters for culture level C_0. I pass these
        values to each culture on a Plate and simulate individually
        using the IndeModel (i.e. can't use a plate level C_0.

        log_plate : A Plate object containing Cultures, each with cell
        observations and times.

        log_params : A dictionary of logistic model parameters, keys
        "C_0", "K", and "r" to convert to C_0, N_0, and b and store as
        attributes of each culture.

        """
        smooth_times = np.linspace(log_plate.times[0], log_plate.times[-1], 100)
        zone = get_qfa_R_zone(log_plate, log_params, coords, rows, cols, smooth_times)

        fig, grid = self._make_grid(zone, zone.c_meas, False, title,
                                    vis_ticks=True)
        for i, ax in enumerate(grid):
            ax.plot(zone.times, zone.c_meas[i::zone.no_cultures],
                    'x', label='Observed Cells', color="b",
                    ms=self.ms, mew=self.mew)
        for ax, culture in zip(grid, zone.cultures):
            ax.plot(smooth_times, culture.c_smooth,
                    '-', label='Logistic Cells', ms=self.ms, mew=self.mew)
        plt.show()
        plt.close()


    # Plate may have plate.inde_est and plate.comp_est so need to pass
    # one of these.
    def plot_est_rr(self, plate, est_params, title='Estimated Growth',
                    sim=False, filename=None, legend=False, vis_ticks=True):
        # Smooth times for sims.
        sim_times = np.linspace(plate.times[0], plate.times[-1], 100)
        # Cannot deepcopy swig objects belonging to plate so define
        # new plate and simulate smooth curves from the estimates.
        est_plate = Plate(plate.rows, plate.cols)
        est_plate.times = sim_times
        est_plate.set_rr_model(self.model, est_params)
        est_amounts = self.model.rr_solve(est_plate, est_params)
        est_amounts = np.split(est_amounts, self.model.no_species, axis=1)

        if sim:
            # "True" data
            sim_amounts = np.split(plate.sim_amounts, self.model.no_species,
                                   axis=1)

        fig, grid = self._make_grid(plate, est_amounts, sim, title, vis_ticks)

        for i, ax in enumerate(grid):
            if not sim: # and i not in plate.empties:
                # Plot c_meas.
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', color="black", label='Observed Cells',
                        ms=self.ms, mew=self.mew)
            for j, species in enumerate(self.model.species):
                ax.plot(sim_times, est_amounts[j][:, i], self.colours[j],
                        label="Est " + self.species[species], lw=self.lw)
                if j == 0: # and i in plate.empties:
                    # Do not plot c_meas for empty cultures.
                    continue
                elif sim:
                    # Plot all "true" amounts (e.g. including C and
                    # unobservable, but known, N.)
                    ax.plot(plate.times, sim_amounts[j][:, i],
                            'x' + self.colours[j],
                            label="True"+self.species[species],
                            ms=self.ms, mew=self.mew)
                else:
                    continue

        self._hide_last_ticks(grid, plate.rows, plate.cols)

        if legend:
            grid[-1].legend(loc='best', fontsize=self.legend_font_size)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    # Old plotter using odeint solver brought back for debugging.
    def plot_est(self, plate, est_params, title='Estimated Growth',
                 sim=False, filename=None, legend=False,
                 vis_ticks=True):
        # Smooth times for sims.
        sim_times = np.linspace(plate.times[0], plate.times[-1], 100)
        amounts = self.model.solve(plate, est_params, sim_times)
        amounts = np.split(amounts, self.model.no_species, axis=1)
        if sim:
            # Split by specie
            sim_amounts = np.split(plate.sim_amounts, self.model.no_species,
                                   axis=1)

        fig, grid = self._make_grid(plate, amounts, sim, title, vis_ticks)

        for i, ax in enumerate(grid):
            if not sim and i not in plate.empties:
                # Plot c_meas.
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', color="black", label='Observed Cells',
                        ms=self.ms, mew=self.mew)
            for j, species in enumerate(self.model.species):
                ax.plot(sim_times, amounts[j][:, i], self.colours[j],
                        label="Logistic "+self.species[species], lw=self.lw)
                if j == 0 and i in plate.empties:
                    continue
                if sim:
                    # Plot all true. These do not have noise added.
                    ax.plot(plate.times, sim_amounts[j][:, i],
                            'x' + self.colours[j],
                            label="True"+self.species[species], ms=self.ms, mew=self.mew)
                else:
                    continue

        self._hide_last_ticks(grid, plate.rows, plate.cols)

        if legend:
            grid[-1].legend(loc=2, fontsize=self.legend_font_size)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    # Should make without roadrunnner to plot logistic eq. and
    # competition model or just handle the models differently.
    def plot_zone_est(self, plates, plate_names, est_params, models,
                      coords, rows, cols, title="Zone Estimates",
                      legend=False, filename=None, plot_types=None,
                      vis_ticks=True, log_plate=None, log_params=None):
        """Plot estimates for a zone.

        Plotting a zone from a full plate estimate requires simulating
        for the full plate and then taking the amounts from the zone
        rather than just simulating from the zone params.

        plates : list of Plates with different c_meas data. If both
        estimates are from the same Plate you need only provide one
        Plate in the list.

        plate_neams : list of strings. Names of plates to use in
        figure legend.

        est_params : list of parameter estimate from fits of different
        models.

        models : list of models corresponding to est_params.

        coords : tuple of coordinates of top left culture in zone
        (indices start from zero).

        row, cols : rows and columns for zone.

        plot_types : list of strings for plot labels. If the first
        plate is to plot the estimate and the second a simulation use
        e.g. ["Est", "Sim"]

        log_plate : A plate from a QFA R logistic fit.

        """
        smooth_times = np.linspace(plates[0].times[0], plates[0].times[-1], 100)

        if log_plate is not None:
            log_zone = get_qfa_R_zone(log_plate, log_params, coords,
                                      rows, cols, smooth_times)

        smooth_plate = Plate(plates[0].rows, plates[0].cols)
        smooth_plate.times = smooth_times
        smooth_plate.smooth_amounts = []
        for params, model in zip(est_params, models):
            smooth_plate.set_rr_model(model, params)
            smooth_amounts = smooth_plate.rr_solve()
            # print("1")
            # print(smooth_amounts)
            # smooth_amounts = np.split(smooth_amounts, self.model.no_species,
            #                           axis=1)
            smooth_plate.smooth_amounts.append(smooth_amounts)

        plates[0].amounts = []
        # Simulate comp model at observed timepoints and get the amounts for the zone
        plates[0].set_rr_model(models[0], est_params[0])
        plates[0].amounts = plates[0].rr_solve()
        zone_amounts = get_zone_amounts(plates[0].amounts, plates[0],
                                        models[0], coords, rows, cols)

        zones = []
        for plate in plates:
            zone = get_plate_zone(plate, coords, rows, cols)
            zone.times = plate.times
            zones.append(zone)

        # Caclulate objective function for comp model
        comp_obj_funs = []
        for i, culture in enumerate(zone.cultures):
            comp_obj_funs.append(least_sq(culture.c_meas, zone_amounts[:, i]))
        print(np.sum(comp_obj_funs))

        zone_smooth_amounts = []
        for model, smooth_amounts in zip(models, smooth_plate.smooth_amounts):
            sim_amounts = get_zone_amounts(smooth_amounts, plate, model,
                                           coords, rows, cols)
            sim_amounts = np.split(sim_amounts, self.model.no_species, axis=1)
            zone_smooth_amounts.append(sim_amounts)

        fig, grid = self._make_grid(zone,
                                    np.array(zone_smooth_amounts).flatten(),
                                    False, title, vis_ticks)

        if plot_types is None:
            plot_types = ["Est." for plate in plates]

        species_labels = {
            "C": "Cells",
            "N": "Nutrients",
            }

        # Check if c_meas are equal for the plates so don't plot
        # twice. Currently only checks for two.
        if len(plates) == 2 and len(plates[0].c_meas) == len(plates[1].c_meas):
            same_c_meas = np.array_equal(plates[0].c_meas, plates[1].c_meas)
        else:
            same_c_meas = False

        colors = {
            "C": ["b", "b", "b"],
            "N": ["y", "y", "g"],
            }
        lines = ["-", "--", "--"]

        # for i, ax in enumerate(grid):
        #     # Plot c_meas.
        #     for plate_name, c, zone in zip(plate_names, self.c_meas_colors, zones):
        #     # for plate_name, c, zone in zip(plate_names, colors["C"][:-1], zones):
        #         if same_c_meas:
        #             ax.plot(zone.times, zone.c_meas[i::zone.no_cultures],
        #                     'x', color=c, label='Observed Cells',
        #                     ms=self.ms, mew=self.mew)
        #             break
        #         else:
        #             ax.plot(zone.times, zone.c_meas[i::zone.no_cultures],
        #                     'x', color=c,
        #                     label='Observed Cells {0}'.format(plate_name),
        #                     ms=self.ms, mew=self.mew)
        #     # continue    # Remove this line
        #     # Plot smooth amounts for each estimate.
        #     plot_zip = zip(plate_names, plot_types, zone_smooth_amounts, models)
        #     for k, (plate_name, plot_type, smooth_amounts, model) in enumerate(plot_zip):
        #         for j, (amounts, species) in enumerate(zip(smooth_amounts, model.species)):
        #             # if j==1: break
        #             ax.plot(smooth_times, amounts[:, i], colors[species][k],
        #                     label="{0} ".format(plot_type) + species_labels[species] + " {0}".format(plate_name),
        #                     # lw=self.lw, ls=self.linestyles[plate_names.index(plate_name)])
        #                     lw=self.lw, ls=lines[k])
        # if log_zone is not None:
        #     # for ax, culture in zip(grid, log_zone.cultures):
        #     #     ax.plot(smooth_times, culture.c_smooth, '-',
        #     #             label='Logistic Cells', color="r", lw=self.lw)
        #     for ax, culture in zip(grid, log_zone.cultures):
        #         ax.plot(smooth_times, culture.c_smooth, '-',
        #                 label="Log. obj. {0:.3f}".format(culture.least_sq*1000),
        #                 color="r", lw=self.lw)
        #         ax.legend(loc='best', fontsize=self.legend_font_size)

        # Add text to plots with objective fuction values

        # Alternative labels objective function.
        for i, ax in enumerate(grid):
            # Plot c_meas.
            for plate_name, c, zone in zip(plate_names, self.c_meas_colors, zones):
            # for plate_name, c, zone in zip(plate_names, colors["C"][:-1], zones):
                if same_c_meas:
                    ax.plot(zone.times,
                            zone.c_meas[i::zone.no_cultures], 'x',
                            color=c, ms=self.ms, mew=self.mew)
                    break
                else:
                    ax.plot(zone.times,
                            zone.c_meas[i::zone.no_cultures], 'x',
                            color=c, ms=self.ms, mew=self.mew)
            # continue    # Remove this line
            # Plot smooth amounts for each estimate.
            plot_zip = zip(plate_names, plot_types, zone_smooth_amounts, models)
            for k, (plate_name, plot_type, smooth_amounts, model) in enumerate(plot_zip):
                for j, (amounts, species) in enumerate(zip(smooth_amounts, model.species)):
                    if j==0 and k==0:
                        ax.plot(smooth_times, amounts[:, i], colors[species][k],
                                label="Obj. {0:.2f}".format(comp_obj_funs[i]*10000),
                                # lw=self.lw, ls=self.linestyles[plate_names.index(plate_name)])
                                lw=self.lw, ls=lines[k])
                    else:
                        ax.plot(smooth_times, amounts[:, i], colors[species][k],
                                # lw=self.lw, ls=self.linestyles[plate_names.index(plate_name)])
                                lw=self.lw, ls=lines[k])
        if log_zone is not None:
            for ax, culture in zip(grid, log_zone.cultures):
                ax.plot(smooth_times, culture.c_smooth, '-',
                        label="Obj. {0:.2f}".format(culture.least_sq*10000),
                        color="r", lw=self.lw)
                ax.legend(loc=2, fontsize=self.legend_font_size)


        self._hide_last_ticks(grid, zone.rows, zone.cols)

        # plt.tight_layout()

        # # Change order of labels.
        # ax = grid[-1]
        # handles, labels = ax.get_legend_handles_labels()
        # new_order = [0, 2, 3, 1, 4, 5, 6, 7]
        # handles2 = [handles[i] for i in new_order]
        # labels2 = [labels[i] for i in new_order]

        # # Change order of labels.
        # ax = grid[-1]
        # handles, labels = ax.get_legend_handles_labels()
        # new_order = [0, 2, 1, 3, 4]
        # handles2 = [handles[i] for i in new_order]
        # labels2 = [labels[i] for i in new_order]

        # For multiple columns reorder the axis labels by row
        def flip(items, ncol):
            """http://stackoverflow.com/a/10101532"""
            return itertools.chain(*[items[i::ncol] for i in range(ncol)])
        ax = grid[-1]
        handles, labels = ax.get_legend_handles_labels()
        handles = flip(handles, self.legend_cols)
        labels = flip(labels, self.legend_cols)

        if legend:
            # grid[1].legend(handles2, labels2, loc='best', fontsize=self.legend_font_size)
            grid[-1].legend(handles, labels, loc='best',
                            fontsize=self.legend_font_size,
                            ncol=self.legend_cols,
                            bbox_to_anchor=self.bbox)

        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    def plot_correction(self, plate, est_params, comp_amounts,
                        title="Corrected Growth",
                        legend=False, filename=None):
        sim_times = np.linspace(plate.times[0], plate.times[-1], 100)
        corrected_amounts = self.model.solve(plate, est_params, sim_times)
        corrected_amounts = np.split(corrected_amounts,
                                     self.model.no_species, axis=1)
        comp_amounts = np.split(comp_amounts, self.model.no_species,
                                axis=1)

        fig, grid = self._make_grid(plate, corrected_amounts,
                                    False, title, vis_ticks=True)

        for i, ax in enumerate(grid):
            # plot c_meas
            if i not in plate.empties:
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', color="black", label='Observed Cells', ms=self.ms,
                        mew=self.mew)
                for j, species in enumerate(self.model.species):
                    # plot comp_est_amounts
                    ax.plot(sim_times, comp_amounts[j][:, i], self.colours[j],
                            label="Competition Model "+self.species[species], lw=self.lw)
                    # plot correction
                    ax.plot(sim_times, corrected_amounts[j][:, i],
                            self.colours[j] + "--", label="Corrected "
                            + self.species[species], lw=self.lw)

        if legend:
            grid[-1].legend(loc='best', fontsize=self.legend_font_size)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    def plot_c_meas(self, plate, title="Measured cell intensity",
                    ms=6.0, mew=0.5):
        fig, grid = self._make_grid(plate, plate.c_meas, False, title, vis_ticks=True)

        for i, ax in enumerate(grid):
            ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                    'x', label='Observed Cells', ms=ms, mew=mew)
        plt.show()
        plt.close()


    def plot_spline(self, plate, title="Spline of cell data", ms=6.0, mew=0.5, lw=1.0):
        """Plot the true c_meas and the spline."""
        fig, grid = self._make_grid(plate, plate.c_meas, False, title, vis_ticks=True)

        for i, ax in enumerate(grid):
            ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                    'x', label='Observed Cells', ms=ms, mew=mew)
            ax.plot(plate.t_spline, plate.c_spline[i::plate.no_cultures],
                    label="Spline", ms=ms, mew=mew, lw=lw)
        plt.show()
        plt.close()



    # Need to plot simulations when the independent (or another model)
    # is fit to individual cultures
    def plot_culture_fits(self, zone, model, title="Individual fits of cultures",
                          sim=False, ms=6.0, mew=0.5, lw=1.0, legend=False,
                          filename=None, est_name="est"):
        fig, grid = self._make_grid(zone, zone.c_meas, sim, title, vis_ticks=False)

        sim_times = np.linspace(zone.times[0], zone.times[-1], 100)

        for i, ax in enumerate(grid):
            culture = zone.cultures[i]
            # Simulate culture amounts from the estimates.
            try:
                # For SciPy OptimizeResult objects.
                est = getattr(culture, est_name).x
            except AttributeError:
                est = getattr(culture, est_name)
            culture_amounts = model.solve(culture, est, sim_times)
            if model.name == "Neighbour model":
                # Do not want neighbouring - and + cultures
                culture_amounts = culture_amounts[:, [2, 3]]
            # Plot c_meas
            ax.plot(zone.times, zone.c_meas[i::zone.no_cultures], 'x',
                    label='Observed Cells', ms=ms, mew=mew, color='r')

            for j, species in enumerate(model.species):
                # Plot estimated amounts
                ax.plot(sim_times, culture_amounts[:, j],
                        self.colours[j], label="Est "+species, lw=lw)
                if j == 0 and i in zone.empties:
                    continue
                elif sim and j != 0:
                    ax.plot(zone.times, zone.sim_amounts[:, j*zone.no_cultures + i],
                            'x' + self.colours[j], label="True "+species,
                            ms=ms, mew=mew)
                else:
                    continue

        if legend:
            grid[-1].legend(loc='best')
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    def plot_scatter(self, xs, ys, labels, title="", xlab="", ylab="",
                     outfile="", ax_multiples=None, legend=True,
                     pearson=True, spearman=True):
        """Make scatter plots

        xs : iterable of iterables of x values

        ys : iterable of iterables of y values

        labels : list of names for distiributions
        (e.g. ["Logistic r", "Competition Model r"])

        ax_multiples : List for x and y axes. Axes will finish at the
        first multiple of (the corresponding value in) ax_multiples
        above the max value in the data.

        legend : (bool) Whether or not to show a legend.

        pearson : (bool) Whether or not to show Pearson correlation
        coefficient in the legend.

        """
        if ax_multiples is None:
            ax_multiples = [10, 10]
        colors = ["k", "r", "b", "m", "g", "c"]
        # colors = ["#00FF00", "#FFFF00", "c"]
        markers = ["x", "^", "+", "o", "v", "D"]

        fig = plt.figure(figsize=self.fig_settings["figsize"], dpi=500)

        ax = plt.gca()
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(self.labelsize)
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(self.labelsize)

        fig.suptitle(title, fontsize=self.title_font_size)
        plt.xlabel(xlab, fontsize=self.font_size, labelpad=self.xpad)
        plt.ylabel(ylab, fontsize=self.font_size, labelpad=self.ypad)

        if spearman:
            spearmans = [r"$\rho_S = {0:.3f}$".format(spearmans_rho([x, y])[-1][0])
                         for x, y in zip(xs, ys)]
        if pearson:
            ccoefs = []
            for x, y in zip(xs, ys):
                m = np.vstack((x, y))
                ccoef_m = np.corrcoef(m)
                ccoef = ccoef_m[0, 1]
                ccoefs.append(r"$\rho_P = {0:.3f}$".format(ccoef))
        if spearman or pearson:
            labels = [lab + " (" for lab in labels]
            if pearson:
                labels = [lab + ccoef for lab, ccoef in zip(labels, ccoefs)]
            if pearson and spearman:
                labels = [lab + ", " for lab in labels]
            if spearman:
                labels = [lab + rs for lab, rs in zip(labels, spearmans)]
            labels = [lab + ")" for lab in labels]

        for marker, color, x, y, lab in zip(markers, colors, xs, ys, labels):
            plt.plot(x, y, "x", ms=self.ms, mew=self.mew, color=color,
                     label=lab)

        # Change to cope with different size arrays (temporary
        # fix). Range dicided by first set of values in outer except.
        try:
            max_val = np.ceil(np.max([xs, ys])/10.0)*10
            plt.plot([0, max_val], [0, max_val], color="k")
            try:
                xmax = (np.max(xs)//ax_multiples[0] + 1) * ax_multiples[0]
            except ZeroDivisionError:
                xmax = np.max(xs)*1.1
            try:
                ymax = (np.max(ys)//ax_multiples[1] + 1) * ax_multiples[1]
            except ZeroDivisionError:
                ymax = np.max(ys)*1.1
        except ValueError:
            max_val = np.ceil(np.max([xs[0], ys[0]])/10.0)*10
            plt.plot([0, max_val], [0, max_val], color="k")
            try:
                xmax = (np.max(xs[0])//ax_multiples[0] + 1) * ax_multiples[0]
            except ZeroDivisionError:
                xmax = np.max(xs[0])*1.1
            try:
                ymax = (np.max(ys[0])//ax_multiples[1] + 1) * ax_multiples[1]
            except ZeroDivisionError:
                ymax = np.max(ys[0])*1.1

        plt.xlim([0.0, xmax])
        plt.ylim([0.0, ymax])

        # Need to make a legend with correlation coefficient
        if legend:
            plt.legend(loc="best", fontsize=self.legend_font_size)

        if outfile:
            plt.savefig(outfile)
        else:
            plt.show()
        plt.close()


if __name__ == "__main__":
    from cans2.plate import Plate
    from cans2.model import CompModel

    rows = 2
    cols = 2
    plate1 = Plate(rows, cols)
    plate1.times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    params = {
        "C_0": 1e-6,
        "N_0": 0.1,
        "kn": 1.5
    }
    plate1.set_sim_data(comp_model, b_mean=40.0, b_var=15.0,
                        custom_params=params)

    comp_plotter = Plotter(comp_model)
    comp_plotter.plot_est(plate1, plate1.sim_params, title="Simulated growth",
                          sim=True)
