import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid


from cans import *



def plot_growth(rows, cols, amounts, times, filename=None):
    """Plot a grid of timecourses of C, N, and S for each culture."""
    ymax = np.amax(true_amounts)
    ymax = np.ceil(ymax*10)/10
    fig = plt.figure()
    fig.suptitle('CANS growth')
    # http://stackoverflow.com/a/36542971
    # add a big axes, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off',
                    bottom='off', left='off', right='off')
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Amount', fontsize=30)

    for i in range(rows*cols):
        fig.add_subplot(rows, cols, i+1, ylim=(0.0, ymax))
        plt.plot(times, amounts[:, i*3], 'b', label='cells')
        plt.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
        plt.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
        plt.grid()
    plt.legend(loc='best')
    if filename is None:
        plt.show()
    else:
        # plt.legend(loc='best')
        plt.savefig(filename)


def plot_growth_grid(rows, cols, amounts, times, filename=None):
    """Plot a grid of timecourses of C, N, and S for each culture."""
    ymax = np.amax(true_amounts)
    ymax = np.ceil(ymax*10)/10
    fig = plt.figure()

    # http://stackoverflow.com/a/36542971
    # add a big axes, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off',
                    bottom='off', left='off', right='off')
    plt.xlabel('Time')
    plt.ylabel('Amount')

    grid = AxesGrid(fig, 111,
                    nrows_ncols=(rows, cols),
                    axes_pad=0.2, aspect=False, share_all=True)
    for i, ax in enumerate(grid):
        #ax.ylim = (
        ax.plot(times, amounts[:, i*3], 'b', label='cells')
        ax.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
        ax.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
        ax.grid()

    plt.legend(loc='best')
    if filename is None:
        plt.show()
    else:
        # plt.legend(loc='best')
        plt.savefig(filename)




        # if not i % cols:
        #     # Then in first column
        #     ax.set_ylabel('Amount')
        # if i + 1 > (rows-1)*cols:
            # Then in last row
    #     #     ax.set_xlabel('t')

    # plt.legend(loc='best')
    # plt.show()
    #     fig.add_subplot(rows, cols, i+1, ylim=(0.0, ymax), axes=ax)
    #     plt.plot(times, amounts[:, i*3], 'b', label='cells')
    #     plt.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
    #     plt.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
    #     plt.xlabel('t')
    #     plt.grid()
    # if filename is None:
    #     plt.show()
    # else:
    #     # plt.legend(loc='best')
    #     plt.savefig(filename)



    # fig = plt.figure()
    # for i in range(rows*cols):
    #     fig.add_subplot(rows, cols, i+1, ylim=(0.0, ymax))
    #     plt.plot(times, amounts[:, i*3], 'b', label='cells')
    #     plt.plot(times, amounts[:, i*3 + 1], 'y', label='nutrients')
    #     plt.plot(times, amounts[:, i*3 + 2], 'r', label='signal')
    #     plt.xlabel('t')
    #     plt.grid()
    # if filename is None:
    #     plt.show()
    # else:
    #     # plt.legend(loc='best')
    #     plt.savefig(filename)


rows = 2
cols = 2
no_cultures = rows*cols
neighbourhood = find_neighbourhood(rows, cols)
params = gen_params(no_cultures)
init_amounts = gen_amounts(no_cultures)
times = np.linspace(0, 20, 201)
true_amounts = solve_model(init_amounts, times, params, neighbourhood)
plot_growth(rows, cols, true_amounts, times)
plot_growth_grid(rows, cols, true_amounts, times)
