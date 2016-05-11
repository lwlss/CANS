import numpy as np
import matplotlib.pyplot as plt


from mpl_toolkits.axes_grid1 import AxesGrid


class Plotter:

    def __init__(self, model):
        self.model = model
        self.colours = ['b', 'y', 'r']


    def _find_ymax(self, amounts):
        ymax = np.amax(amounts)
        ymax = np.ceil(ymax*10)/10
        return ymax

    def _make_grid(self, rows, cols, title):
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
        return fig, grid


    def _add_to_grid(self, grid):
        # for i, ax in enumerate(grid):
        pass


    # Plate may have plate.inde_est and plate.comp_est so need to pass
    # one of these.
    def plot_estimate(self, plate, est_params, title='Estimated Growth',
                      sim=False):
        amounts = self.model.solve(plate, est_params)    # times?
        if sim:
            ymax = self._find_ymax(np.append(amounts, plate.sim_amounts))
        else:
            ymax = self._find_ymax(np.append(amounts, plate.c_meas))

        fig, grid = self._make_grid(plate.rows, plate.cols, title)

        for i, ax in enumerate(grid):
            ax.set_ylim(0.0, ymax)
            ax.grid()
            for j, species in enumerate(self.model.species):
                ax.plot(plate.times, amounts[:, i * self.model.no_species + j],
                        self.colours[j], label=species)
            if sim:
                for j, species in enumerate(self.model.species):
                    ax.plot(plate.times,
                            plate.sim_amounts[:, i*self.model.no_species + j],
                            'x', label=species)
            else:
                # just plot c_meas
                # may need to reshape c_meas
                ax.plot(plate.times, plate.c_meas[i::plate.no_cultures],
                        'x', label='Observed Cells')
            if i + 1 > (plate.rows - 1)*plate.cols:
                # Then in last row.
                plt.setp(ax.get_xticklabels()[-1], visible=False)
                # pass
            if not i % plate.cols:
                # Then in first column.
                plt.setp(ax.get_yticklabels()[-1], visible=False)
        plt.show()
        plt.close()


    def plot_data(self):
        pass


    def show(self):
        pass


    def save(self):
        pass




    # def plot(self, amounts, title):
    #     ymax = np.amax(amounts)
    #     ymax = np.ceil(ymax*10)/10
    #     fig = plt.figure()
    #     fig.suptitle(title, fontsize=20)
    #     # http://stackoverflow.com/a/36542971
    #     # Add big axes and hide frame.
    #     fig.add_subplot(111, frameon=False)
    #     # Hide tick and tick label of the big axes.
    #     plt.tick_params(labelcolor='none', top='off',
    #                     bottom='off', left='off', right='off')
    #     plt.xlabel('Time', fontsize=18)
    #     plt.ylabel('Amount', fontsize=18)
    #     grid = AxesGrid(fig, 111, nrows_ncols=(rows, cols),
    #                     axes_pad=0.1, aspect=False, share_all=True)

    #     for i, ax in enumerate(grid):
    #         ax.set_ylim(0.0, ymax)
    #         ax.plot(times, amounts[:, i*2], 'b', label='Cells')
    #         ax.plot(times, amounts[:, i*2 + 1], 'y', label='Nutrients')
    #         if data is not None:
    #             ax.plot(times, data[:, i*2], 'x', label='Cells Data')
    #             ax.plot(times, data[:, i*2 + 1], 'x', label='Nutrients Data')
    #             ax.grid()
    #         if i + 1 > (rows - 1)*cols:
    #             # Then in last row.
    #             plt.setp(ax.get_xticklabels()[-1], visible=False)
    #             # pass
    #         if not i % cols:
    #             # Then in first column.
    #             plt.setp(ax.get_yticklabels()[-1], visible=False)

    #     # grid[-1].legend(loc='best')
    #     if filename is None:
    #         plt.show()
    #     else:
    #         plt.savefig(filename)
    #     plt.close()




# class Plotter:

#     def __init__(self, model, plate):
#         self.model = model
#         self.plate = plate

#     def plot(self):
#         ymax = np.amax(self.plate.est_amounts)


#     def save_plot(self, filename):
#         pass
