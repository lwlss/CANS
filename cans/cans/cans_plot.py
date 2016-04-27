"""Functions for plotting cans time-courses."""
import matplotlib.pyplot as plt
import numpy as np


from mpl_toolkits.axes_grid1 import AxesGrid


def plot_growth(rows, cols, amounts, times, filename=None):
    """Plot a grid of timecourses of C, N, and S for each culture."""
    ymax = np.amax(amounts)
    ymax = np.ceil(ymax*10)/10
    fig = plt.figure()
    fig.suptitle('CANS growth', fontsize=20)
    # http://stackoverflow.com/a/36542971
    # add a big axes, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off',
                    bottom='off', left='off', right='off')
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Amount', fontsize=18)

    for i in range(rows*cols):
        ax = fig.add_subplot(rows, cols, i+1, ylim=(0.0, ymax))
        plt.plot(times, amounts[:, i*3], 'b', label='cells')
        plt.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
        plt.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
        plt.grid()
        if i % cols:
            # Then not in first column.
            plt.setp(ax.get_yticklabels(), visible=False)
        if i < (rows - 1 )*cols:
            # Then not in last row.
            plt.setp(ax.get_xticklabels(), visible=False)

    plt.legend(loc='best')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


def plot_growth_grid(rows, cols, amounts, times, title='CANS Growth', filename=None):
    """Plot a grid of timecourses of C, N, and S for each culture.

    Uses AxesGrid from mpl_loolkits.axes_grid1.
    """
    ymax = np.amax(amounts)
    ymax = np.ceil(ymax*10)/10
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
        ax.plot(times, amounts[:, i*3], 'b', label='cells')
        ax.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
        ax.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
        ax.grid()
        if i + 1 > (rows - 1)*cols:
            # Then in last row.
            plt.setp(ax.get_xticklabels()[-1], visible=False)
            # pass
        if not i % cols:
            # Then in first column.
            plt.setp(ax.get_yticklabels()[-1], visible=False)
            # pass

    # grid[-1].legend(loc='best')
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
