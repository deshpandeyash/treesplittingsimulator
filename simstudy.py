from simulation import Simulation
from matplotlib import pyplot
import numpy as np
import time
from theoretical_plots import TheoreticalPlots
from simparam import SimParam
from scipy.stats import skew
import graphdisplay

from simsetting import SimSetting

import os

def simulate_tree_branching(sim, setting):
    """
    To get the vizualization of 1 tree for the given settings and number of users as defined by simsettings and simparam
    also prints the obtained throughput, tree progression, result progression and tree depth
    """
    # os.environ["PATH"] += os.pathsep + r'C:\Users\Murat\Anaconda3\Library\bin\graphviz'
    os.environ["PATH"] += os.pathsep + r'C:\Users\deshp\Anaconda3\Library\bin\graphviz'
    sim.reset(setting)
    sim.do_simulation_simple_tree_static(setting.vizwindow.users)
    print("Results were: ")
    print(sim.tree_state.result_array)
    print("Tree Progression was: ")
    print(sim.branch_node.branch_array[:-1])
    print("Mean Throughput is = " + str(sim.sim_result.throughput))
    print("The Depth of the tree is: " + str(sim.sim_result.mean_tree_depth))
    graphdisplay.displaygraph(sim)

def simulate_simple_tree_static_multiple_runs(sim, setting):
    """
    Does a a number of runs with the same number of users, plots the distribution of throughput and prints out the
    theoretical throughput
    """
    start = time.time()
    throughput = []
    for _ in range(setting.statictreewindow.runs):
        # Reset the simulation
        sim.reset(setting)
        sim.do_simulation_simple_tree_static(setting.statictreewindow.users)
        throughput.append(sim.sim_result.throughput/sim.sim_param.K)
        if sim.tree_state.total_successes != setting.statictreewindow.users:
            print("Error total successes not equal to total users")
    print("Skewness in throughput distribution is :" + str(skew(np.asarray(throughput))))
    print("Mean Throughput:  " + str(np.mean(throughput)))
    pyplot.hist(throughput, density=True)
    pyplot.show()
    print("Theoretical Throughput: " + str(TheoreticalPlots().qarysic(38, setting)))
    #print("Theoretical Throughput: " + str(TheoreticalPlots().qarysic(users)))
    end = time.time()
    print("Time for simulation: " + str(end-start))
    pyplot.show()


def simulate_users(sim, setting):
    """
    Sweeps through number of users, taking an average over the runs defined in simsetting for each run.
    At the same time plots the theoretical results.
    :param n_stop: Till the number of users we wish to plot.
    """
    start = time.time()
    throughput_array = []
    theoretical_out_array = []
    user_array = np.arange(sim.sim_param.K + 1, setting.usersweep.n_stop)
    for n in user_array:
        throughput = []
        for _ in range(setting.usersweep.runs):
            # Reset the simulation
            sim.reset(setting)
            sim.do_simulation_simple_tree_static(n)
            throughput.append(sim.sim_result.throughput/sim.sim_param.K)
        throughput_array.append(np.mean(throughput))
        theoretical_out_array.append(TheoreticalPlots().qarysic(n, setting))
    theoretical_out = TheoreticalPlots().qarysic(setting.usersweep.n_stop, setting)
    pyplot.plot(user_array, throughput_array,  'b-', label='simulation')
    pyplot.plot(user_array, theoretical_out_array, 'r', label='theoretical')
    #pyplot.hlines(theoretical_out, sim.sim_param.K, n_stop, colors='green', label='Steady State')
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
    if setting.theorsweep.test_values[0]:
        pyplot.plot(users, theoretical, 'b-', label='Quary Sic')
    if setting.theorsweep.test_values[1]:
        pyplot.plot(users, theoretical1, 'g-', label='SICTA')
    if setting.theorsweep.test_values[2]:
        pyplot.plot(users, theoretical2, 'r-', label='Simple Tree')
    if setting.theorsweep.test_values[3]:
        pyplot.plot(users, theoretical2, 'c-', label='Recursive SICTA')
    if setting.theorsweep.test_values[4]:
        pyplot.plot(users, theoretical2, 'm-', label='Recursive Quary')

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
    # Comment and uncomment the below methods as it suits
    if True not in setting.secondwindow.test_values:
        print("No Test Selected")
    else:
        for test in test_array:
            if setting.secondwindow.test_values[test_array.index(test)]:
                sim.reset(setting)
                test(sim, setting)








