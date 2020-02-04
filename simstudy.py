from simulation import Simulation
from matplotlib import pyplot
import numpy as np
import time
from theoretical_plots import TheoreticalPlots
from simparam import SimParam
from scipy.stats import skew
import graphdisplay
from make_stat import mean_confidence_interval, plot_conf_interval
from simsetting import SimSetting

import os

def simulate_tree_branching(sim, setting):
    """
    To get the vizualization of 1 tree for the given settings and number of users as defined by simsettings and simparam
    also prints the obtained throughput, tree progression, result progression and tree depth
    """
    if os.environ.get('graphviz-2.38')  is None:
        print("Graphviz is not in the path")


    # os.environ["PATH"] += os.pathsep + r'C:\Users\Murat\Anaconda3\Library\bin\graphviz'
    sim.reset(setting)
    sim.do_simulation_simple_tree_static(setting.vizwindow.users)
    print("Results were: ")
    print(sim.tree_state.result_array)
    print("Tree Progression was: ")
    print(sim.branch_node.branch_array[:-1])
    print("Throughput is = " + str(sim.sim_result.throughput/sim.sim_param.K))
    print("Theoretically it should be = " + str(TheoreticalPlots().qarysic(setting.vizwindow.users, setting)))
    print("Magic Throughput " + str(sim.sim_result.magic_throughput))
    print("The Depth of the tree is: " + str(sim.sim_result.mean_tree_depth))
    graphdisplay.displaygraph(sim)

def simulate_simple_tree_static_multiple_runs(sim, setting):
    """
    Does a a number of runs with the same number of users, plots the distribution of throughput and prints out the
    theoretical throughput
    """
    start = time.time()
    conf_intervals = []
    for j in range(10):
        throughput = []
        magic_throughput = []
        for _ in range(setting.statictreewindow.runs):
            # Reset the simulation
            sim.reset(setting)
            users = np.random.poisson(setting.statictreewindow.users)
            sim.do_simulation_simple_tree_static(users)
            throughput.append(sim.sim_result.throughput/sim.sim_param.K)
            magic_throughput.append(sim.sim_result.magic_throughput/sim.sim_param.K)
            if sim.tree_state.total_successes != users:
                print("Error total successes not equal to total users")
        conf_mean, conf_min, conf_max = mean_confidence_interval(throughput, 0.95)
        conf_intervals.append((conf_min,conf_max))
    print("Standard Deviation is : " + str(np.std(np.asarray(throughput))))
    print("Skewness in throughput distribution is :" + str(skew(np.asarray(throughput))))
    print("Mean Throughput:  " + str(np.mean(throughput)))
    theoretical_throughput = TheoreticalPlots().qarysic(30, setting)
    print("Theoretical Throughput: " + str(theoretical_throughput))
    print("Theoretical Throughput and Mean throughput ratio = " + str(theoretical_throughput/np.mean(throughput)))
    print("Magic Throughput " + str(np.mean(magic_throughput)))
    print("Confidence Intervals : " + str(conf_min) + " , " + str(conf_max))
    #print("Theoretical Throughput: " + str(TheoreticalPlots().qarysic(users)))
    bin_height, bin_boundary = np.histogram(throughput, density=True)
    width = bin_boundary[1] - bin_boundary[0]
    bin_height = bin_height / float(sum(bin_height))
    pyplot.bar(bin_boundary[:-1], bin_height, width=width)
    #pyplot.hist(throughput, density=True)
    pyplot.vlines(theoretical_throughput, 0, max(bin_height), colors='r', label='Theoretical Throughput')
    pyplot.vlines(conf_min, 0, max(bin_height), colors='y', label='Conf Intervals')
    pyplot.vlines(conf_max, 0, max(bin_height), colors='y')
    pyplot.xlabel("Throughput")
    pyplot.legend()
    pyplot.savefig('K' + str(sim.sim_param.K) + 'Q' + str(sim.sim_param.SPLIT) + 'histogram_static.png', dpi=300)
    end = time.time()
    print("Time for simulation: " + str(end-start))
    pyplot.show()
    plot_conf_interval(conf_intervals,theoretical_mean=0.368)



def simulate_users(sim, setting):
    """
    Sweeps through number of users, taking an average over the runs defined in simsetting for each run.
    At the same time plots the theoretical results.
    :param n_stop: Till the number of users we wish to plot.
    """
    start = time.time()
    throughput_array = []
    theoretical_out_array = []
    magic_throughput_array = []
    user_array = np.arange(sim.sim_param.K + 1, setting.usersweep.n_stop)
    for n in user_array:
        throughput = []
        magic = []
        for _ in range(setting.usersweep.runs):
            # Reset the simulation
            sim.reset(setting)
            sim.do_simulation_simple_tree_static(np.random.poisson(n))
            #sim.do_simulation_simple_tree_static(n)
            throughput.append(sim.sim_result.throughput/sim.sim_param.K)
            magic.append(sim.sim_result.magic_throughput/sim.sim_param.K)
        throughput_array.append(np.mean(throughput))
        magic_throughput_array.append(np.mean(magic))
        theoretical_out_array.append(TheoreticalPlots().qarysic(n, setting))
        #theoretical_out_array.append(TheoreticalPlots().qsicta(n, setting))
    theoretical_out = TheoreticalPlots().qarysic(setting.usersweep.n_stop, setting)
    pyplot.plot(user_array, throughput_array,  'b-', label='simulation')
    pyplot.plot(user_array, theoretical_out_array, 'r', label='theoretical')
    print("Max Theoretical throughput is " + str(max(theoretical_out_array)) + " at Users "
          + str(user_array[theoretical_out_array.index(max(theoretical_out_array))]))
    print("Steady State Theoretical Value = " + str(theoretical_out))
    pyplot.plot(user_array, magic_throughput_array, 'g', label='Right Skipped Simulation')
    #pyplot.hlines(theoretical_out, sim.sim_param.K, n_stop, colors='green', label='Steady State')
    pyplot.xlabel("Mean Users")
    pyplot.ylabel("Throughput")
    pyplot.legend()
    end = time.time()
    print("Time for simulation: ")
    print(end-start)
    pyplot.show()

def simulate_simple_tree_dynamic_multiple_runs(sim,setting):
    """
    FREE ACCESS SIMULATION
    Sweep through different arrival rate, take average through no of runs. Plot delay, success rate vs arrival rate.

    """
    start = time.time()
    rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step, setting.dynamictest.step)
    succ_rate = []
    delay = []
    for p in rate_array:
        counter1 = []
        counter2 = []
        for _ in range(setting.dynamictest.runs):
            sim.reset(setting)
            sim.sim_param.lmbda = p
            sim.do_simulation_simple_tree_dynamic()
            counter1.append(sim.sim_result.succ_rate)
            counter2.append(sim.sim_result.mean_packet_delay)
        succ_rate.append(np.mean(counter1))
        delay.append(np.mean(counter2))
    optimum_throughput = rate_array[delay.index(max(delay))]
    print("Optimum Throughput = " + str(optimum_throughput))
    pyplot.plot(rate_array, succ_rate, color='red')
    pyplot.xlabel('Arrival rate (packets/slot)')
    pyplot.ylabel('Success rate')
    pyplot.twinx()
    pyplot.plot(rate_array, delay, color='blue')
    pyplot.ylabel('Mean Packet Delay')
    pyplot.show()
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))


def simulate_simple_tree_dynamic_multiple_runs_gated(sim, setting):
    start = time.time()
    rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step, setting.dynamictest.step)
    delay = []
    for p in rate_array:
        counter = []
        for _ in range(setting.dynamictest.runs):
            sim.reset(setting)
            sim.sim_param.lmbda = p
            sim.do_simulation_gated_access()
            counter.append(sim.sim_result.mean_packet_delay)
        delay.append(np.mean(counter))
    pyplot.plot(rate_array, delay, color='blue')
    pyplot.xlabel('Arrival rate (packets/slot)')
    pyplot.ylabel('Mean Packet Delay')
    pyplot.grid()
    pyplot.show()
    end = time.time()
    print("Time for Simulaiton: " + str(end-start))

def do_theoretical_iter(sim, setting):
    """
    :param n_stop: till the end of number of users we want to sweep till
    can be used to compare different formulas in different formulas in different papers.
    plots the throughput vs number of users
    :return:
    """

    param = SimParam(setting)
    users = range(param.K + 1, setting.theorsweep.n_stop + 1)
    theoretical = []
    theoretical1 = []
    theoretical2 = []
    theoretical3 = []
    theoretical4 = []
    theoretical5 = []
    for n in users:
        if setting.theorsweep.test_values[0]:
            theoretical.append(TheoreticalPlots().qarysic(n, setting))
        if setting.theorsweep.test_values[1]:
            theoretical1.append(TheoreticalPlots().sicta(n, setting))
        if setting.theorsweep.test_values[2]:
            theoretical2.append(TheoreticalPlots().simpletree(n))
        if setting.theorsweep.test_values[3]:
            theoretical3.append(TheoreticalPlots().recsicta(n))
        if setting.theorsweep.test_values[4]:
            theoretical4.append(TheoreticalPlots().recquary(n, setting))
        if setting.theorsweep.test_values[5]:
            theoretical5.append(TheoreticalPlots().qsicta(n, setting))
    if setting.theorsweep.test_values[0]:
        pyplot.plot(users, theoretical, 'b-', label='Quary Sic')
    if setting.theorsweep.test_values[1]:
        pyplot.plot(users, theoretical1, 'g-', label='SICTA')
    if setting.theorsweep.test_values[2]:
        pyplot.plot(users, theoretical2, 'r-', label='Simple Tree')
    if setting.theorsweep.test_values[3]:
        pyplot.plot(users, theoretical3, 'c-', label='Recursive SICTA')
    if setting.theorsweep.test_values[4]:
        pyplot.plot(users, theoretical4, 'm-', label='Recursive Quary')
    if setting.theorsweep.test_values[5]:
        pyplot.plot(users, theoretical5, 'y-', label='QSICTA Giannakkis')

    pyplot.xlabel('Users')
    pyplot.ylabel('Throughput')
    pyplot.legend()
    pyplot.show()


test_array = [simulate_tree_branching, simulate_simple_tree_static_multiple_runs, simulate_users,
              simulate_simple_tree_dynamic_multiple_runs, simulate_simple_tree_dynamic_multiple_runs_gated,
              do_theoretical_iter]

if __name__ == '__main__':
    setting = SimSetting()
    # Seed for reproducibility
    # np.random.seed(setting.seed)
    if sum(setting.secondwindow.test_values) > 1:
        print("Multiple Tests should be done by running the scrip multiple times")
        exit()
    sim = Simulation(setting)
    sim.sim_param.print_settings()
    # Comment and uncomment the below methods as it suits
    if True not in setting.secondwindow.test_values:
        print("No Test Selected")
    else:
        for test in test_array:
            if setting.secondwindow.test_values[test_array.index(test)]:
                sim.reset(setting)
                test(sim, setting)








