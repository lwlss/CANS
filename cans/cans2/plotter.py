import numpy as np
import matplotlib.pyplot as plt


from mpl_toolkits.axes_grid1 import AxesGrid


class Plotter:

    def __init__(self, model):
        self.model = model
        # Can decide on other colours when adding models with more species.
        self.colours = ['b', 'y', 'r']


    def _find_ymax(self, amounts):
        ymax = np.amax(amounts)
        ymax = np.ceil(ymax*10)/10
        return ymax


    def _make_grid(self, plate, amounts, sim, title):
        rows = plate.rows
        cols = plate.cols
        if sim:
            ymax = self._find_ymax(np.append(amounts, plate.sim_amounts))
        else:
            ymax = self._find_ymax(np.append(amounts, plate.c_meas))
        fig = plt.figure()
        fig.suptitle(title, fontsize=20)
        # http://stackoverflow.com/a/36542971
        # Add big axes and hide frame.
        fig.add_subplot(111, frameon=False)
        # Hide tick and tick label of the big axes.
        plt.tick_params(labelcolor='none', top='off',
                        bottom='off', left='off', right='off')
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Amount', fontsize=18)
        grid = AxesGrid(fig, 111, nrows_ncols=(rows, cols),
                        axes_pad=0.1, aspect=False, share_all=True)
        for i, ax in enumerate(grid):
            ax.set_ylim(0.0, ymax)
            ax.grid()
            # Remove last tick values.
            if i + 1 > (rows - 1)*cols:
                # Then in last row.
                plt.setp(ax.get_xticklabels()[-1], visible=False)
            if not i % cols:
                # Then in first column.
                plt.setp(ax.get_yticklabels()[-1], visible=False)
        return fig, grid


    # Plate may have plate.inde_est and plate.comp_est so need to pass
    # one of these.
    def plot_est(self, plate, est_params, title='Estimated Growth',
                 sim=False, filename=None, legend=False):
        # Smooth times for sims.
        sim_times = np.linspace(plate.times[0], plate.times[-1], 100)
        amounts = self.model.solve(plate, est_params, sim_times)

        fig, grid = self._make_grid(plate, amounts, sim, title)

        for i, ax in enumerate(grid):
            if not sim and i not in plate.empties:
                # Plot c_meas.
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', label='Observed Cells')
            for j, species in enumerate(self.model.species):
                ax.plot(sim_times, amounts[:, i * self.model.no_species + j],
                        self.colours[j], label=species)
                if j == 0 and i in plate.empties:
                    continue
                elif sim:
                    # Plot all true.
                    ax.plot(plate.times,
                            plate.sim_amounts[:, i*self.model.no_species + j],
                            'x' + self.colours[j], label=species)
                else:
                    continue
        if legend:
            grid[-1].legend(loc='best')
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.close()
