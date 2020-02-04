import numpy as np
import scipy.stats
from matplotlib import pyplot as plt


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def plot_conf_interval(interval_array, theoretical_mean):
    for i in range(1, len(interval_array)+1):
        plt.plot([i, i], interval_array[i-1], color='b')
        plt.ylabel('Throughput')
        plt.xlabel('Runs')
    plt.axhline(y=theoretical_mean, linestyle='--', color='g', label='Theoretical Mean')
    plt.legend()
    plt.title('Alpha = 0.05')
    plt.savefig('conf_interval_plot.png', dpi=300)
    plt.show()
