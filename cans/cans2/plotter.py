import numpy as np
import matplotlib.pyplot as plt
import copy


from mpl_toolkits.axes_grid1 import AxesGrid


from cans2.plate import Plate


def plot_scatter(x, y, title="", xlab="", ylab="", outfile=""):
    fig = plt.figure()
    fig.suptitle(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.plot(x, y, "x", ms=6.0, mew=1.0, color="k")
    max_val = np.ceil(np.max([x, y])/10.0)*10
    plt.plot([0, max_val], [0, max_val], color="k")
    if outfile:
        plt.savefig(outfile)
    else:
        plt.show()
    plt.close()


class Plotter(object):

    def __init__(self, model):
        self.model = model
        # Can decide on other colours when adding models with more species.
        self.colours = ['b', 'y', 'r', 'g']


    def _find_ymax(self, amounts):
        ymax = np.amax(amounts)
        ymax = np.ceil(ymax*10)/10
        return ymax


    def _make_grid(self, plate, amounts, sim, title, vis_ticks):
        rows = plate.rows
        cols = plate.cols
        if sim:
            ymax = self._find_ymax(np.append(amounts, plate.sim_amounts))
        else:
            ymax = self._find_ymax(np.append(amounts, plate.c_meas))
        fig = plt.figure()
        fig.suptitle(title, fontsize=26)
        # http://stackoverflow.com/a/36542971
        # Add big axes and hide frame.
        fig.add_subplot(111, frameon=False)
        # Hide tick and tick label of the big axes.
        plt.tick_params(labelcolor='none', top='off',
                        bottom='off', left='off', right='off')
        plt.xlabel('Time [days]', fontsize=20)
        plt.ylabel('Amount [arb. unit]', fontsize=20)
        grid = AxesGrid(fig, 111, nrows_ncols=(rows, cols),
                        axes_pad=0.1, aspect=False, share_all=True)
        for i, ax in enumerate(grid):
            ax.set_ylim(0.0, ymax)
            ax.grid()

            if not vis_ticks:
                plt.setp(ax.get_xticklabels(which="both"), visible=False)
                plt.setp(ax.get_yticklabels(which="both"), visible=False)

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


    # Plate may have plate.inde_est and plate.comp_est so need to pass
    # one of these.
    def plot_est_rr(self, plate, est_params, title='Estimated Growth',
                    sim=False, filename=None, legend=False, ms=6.0,
                    mew=0.5, lw=1.0, vis_ticks=True):
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
            if not sim and i not in plate.empties:
                # Plot c_meas.
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', label='Observed Cells', ms=ms, mew=mew)
            for j, species in enumerate(self.model.species):
                ax.plot(sim_times, est_amounts[j][:, i], self.colours[j],
                        label="Est " + species, lw=lw)
                if j == 0 and i in plate.empties:
                    # Do not plot c_meas for empty cultures.
                    continue
                elif sim:
                    # Plot all "true" amounts (e.g. including C and
                    # unobservable, but known, N.)
                    ax.plot(plate.times, sim_amounts[j][:, i],
                            'x' + self.colours[j],
                            label="True"+species, ms=ms, mew=mew)
                else:
                    continue

        self._hide_last_ticks(grid, plate.rows, plate.cols)

        if legend:
            grid[-1].legend(loc='best')
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    # Old plotter using odeint solver brought back for debugging.
    def plot_est(self, plate, est_params, title='Estimated Growth',
                 sim=False, filename=None, legend=False, ms=6.0,
                 mew=0.5, lw=1.0):
        # Smooth times for sims.
        sim_times = np.linspace(plate.times[0], plate.times[-1], 100)
        amounts = self.model.solve(plate, est_params, sim_times)
        amounts = np.split(amounts, self.model.no_species, axis=1)
        if sim:
            # Split by specie
            sim_amounts = np.split(plate.sim_amounts, self.model.no_species,
                                   axis=1)

        fig, grid = self._make_grid(plate, amounts, sim, title, vis_ticks=True)

        for i, ax in enumerate(grid):
            if not sim and i not in plate.empties:
                # Plot c_meas.
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', color="black", label='Observed Cells',
                        ms=ms, mew=mew)
            for j, species in enumerate(self.model.species):
                ax.plot(sim_times, amounts[j][:, i], self.colours[j],
                        label="Logistic "+species, lw=lw)
                if j == 0 and i in plate.empties:
                    continue
                if sim:
                    # Plot all true. These do not have noise added.
                    ax.plot(plate.times, sim_amounts[j][:, i],
                            'x' + self.colours[j],
                            label="True"+species, ms=ms, mew=mew)
                else:
                    continue
        if legend:
            grid[-1].legend(loc=2)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    def plot_correction(self, plate, est_params, comp_amounts,
                        title="Corrected Growth",
                        legend=False, filename=None, ms=6.0, mew=0.5, lw=1.0):
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
                        'x', color="black", label='Observed Cells', ms=ms,
                        mew=mew)
                for j, species in enumerate(self.model.species):
                    # plot comp_est_amounts
                    ax.plot(sim_times, comp_amounts[j][:, i], self.colours[j],
                            label="Comp "+species, lw=lw)
                    # plot correction
                    ax.plot(sim_times, corrected_amounts[j][:, i],
                            self.colours[j] + "--", label="Corrected "
                            + species, lw=lw)

        if legend:
            grid[-1].legend(loc=2)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()


    def plot_c_meas(self, plate, title="Measured cell intensity",
                    ms=6.0, mew=0.5):
        fig, grid = self._make_grid(plate, plate.c_meas, False, title)

        for i, ax in enumerate(grid):
            ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                    'x', label='Observed Cells', ms=ms, mew=mew)
        plt.show()
        plt.close()


    # Need to plot simulations when the independent (or another model)
    # is fit to individual cultures
    def plot_culture_fits(self, zone, model, title="Individual fits of cultures",
                          sim=False, ms=6.0, mew=0.5, lw=1.0, legend=False,
                          filename=None, est_name="est"):
        fig, grid = self._make_grid(zone, zone.c_meas, sim, title)

        sim_times = np.linspace(zone.times[0], zone.times[-1], 100)

        for i, ax in enumerate(grid):
            culture = zone.cultures[i]
            # Simulate culture amounts from the estimates.
            est = getattr(culture, est_name).x
            culture_amounts = model.solve(culture, est, sim_times)
            if model.name == "Neighbour model":
                # Do not want neighbouring - and + cultures
                culture_amounts = culture_amounts[:, [2, 3]]
            # Plot c_meas
            ax.plot(zone.times, zone.c_meas[i::zone.no_cultures], 'x',
                    label='Observed Cells', ms=ms, mew=mew)

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
