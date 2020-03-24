import numpy as np
import scipy.stats
from matplotlib import pyplot as plt
import tikzplotlib


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


def plot_conf_interval(interval_array, theoretical_mean, save_fig=False):
    for i in range(1, len(interval_array)+1):
        plt.plot([i, i], interval_array[i-1], color='b')
        plt.ylabel('Throughput')
        plt.xlabel('Runs')
    plt.axhline(y=theoretical_mean, linestyle='--', color='g', label='Theoretical Mean')
    plt.legend()
    plt.title('Alpha = 0.05')
    if save_fig:
        plt.savefig('conf_interval_plot.png', dpi=300)
    plt.show()


def make_histogram_discrete(data, sim, setting, xlabel='Not Given', save_fig=False):
    data = np.array(data)
    d = np.diff(np.unique(data)).min()
    left_of_first_bin = data.min() - float(d) / 2
    right_of_last_bin = data.max() + float(d) / 2
    plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d, d), density=True)
    bin_height, bin_boundary = np.histogram(data, density=True)
    bin_height = bin_height / sum(bin_height)
    plt.vlines(np.mean(data), 0, max(bin_height)/2, colors='r', label='Mean')
    plt.legend()
    plt.xlabel(xlabel)
    if save_fig:
        plt.savefig(xlabel + str(setting.statictreewindow.users) + 'K' + str(sim.sim_param.K) + 'Q'
                    + str(sim.sim_param.SPLIT) + 'histogram_static.png', dpi=300)
    plt.show()


def make_histogram_cont(data,sim, xlabel='Not Given', conf_ints=None, theoretical_mean=None, save_fig=False):
    bin_height, bin_boundary = np.histogram(data, density=True)
    width = bin_boundary[1] - bin_boundary[0]
    bin_height = bin_height / float(sum(bin_height))
    plt.bar(bin_boundary[:-1], bin_height, width=width)
    if theoretical_mean:
        plt.vlines(theoretical_mean, 0, max(bin_height), colors='r', label='Theoretical Throughput')
    if conf_ints:
        plt.vlines(conf_ints[0], 0, max(bin_height), colors='y', label='Conf Intervals')
        plt.vlines(conf_ints[1], 0, max(bin_height), colors='y')
    plt.xlabel(xlabel)
    plt.legend()
    if save_fig:
        plt.savefig(xlabel + 'K' + str(sim.sim_param.K) + 'Q' + str(sim.sim_param.SPLIT) + 'histogram_static.png',
                    dpi=300)
    plt.show()

def make_multiplot(x_axis, y_axis, y_legend, ylabel='Not Given', xlabel='Not Given', save_fig=False, figname='Unkown'):
    for array, legend in zip(y_axis, y_legend):
        plt.plot(x_axis, array, label=f"Users = {legend}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    if save_fig:
        plt.savefig('Results/NewResults/' + figname + '.png', dpi=300)
        tikzplotlib.save('Results/NewResults/' + figname + '.tex')
    plt.show()

