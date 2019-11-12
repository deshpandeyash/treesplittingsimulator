from simulation import Simulation
from matplotlib import pyplot
import numpy as np
import time
from theoretical_plots import TheoreticalPlots
from simparam import SimParam
from scipy.stats import skew
import graphdisplay

import os
#path = os.path.join(os.pathsep, r'C:\Users\deshp\Anaconda2\Library\bin\graphviz')
os.environ["PATH"] += os.pathsep + r'C:\Users\deshp\Anaconda2\Library\bin\graphviz'



def func(x, a, b, c):
    return a * np.exp(-b * x) + c


def simulate_tree_branching():
    sim = Simulation()
    sim.reset()
    sim.do_simulation_simple_tree_static(10)
    print("Results were: ")
    print(sim.tree_state.result_array)
    print("Tree Progression was: ")
    print(sim.branch_node.branch_array[:-1])
    print("Mean Throughput is = " + str(sim.sim_result.throughput))
    print("The Depth of the tree is: " + str(sim.sim_result.mean_tree_depth))
    graphdisplay.displaygraph(sim.branch_node.branch_array[:-1], sim.tree_state.result_array,
                              sim.tree_state.number_in_slot)
    print(sim.branch_node.branch_array)

def simulate_simple_tree_static_multiple_runs():
    start = time.time()
    sim = Simulation()
    throughput = []
    users = 100
    for _ in range(sim.sim_param.RUNS):
        # Reset the simulation
        sim.reset()
        sim.do_simulation_simple_tree_static(users)
        throughput.append(sim.sim_result.throughput)
        if sim.tree_state.total_successes != users:
            print("Error total successes not equal to total users")
    #print("Skewness in throughput distribution is :" + str(skew(np.asarray(throughput))))
    print("Mean Throughput:  " + str(np.mean(throughput)))
    pyplot.hist(throughput, density=True)
    pyplot.show()
    print("Theoretical Throughput: " + str(TheoreticalPlots().qarysic(38, sim.sim_param.K, sim.sim_param.SPLIT)))
    #print("Theoretical Throughput: " + str(TheoreticalPlots().qarysic(users)))
    end = time.time()
    print("Time for simulation: " + str(end-start))
    pyplot.show()


def simulate_sic_oscillations(n_stop, k, q):
    start = time.time()
    sim = Simulation()
    throughput_array = []
    theoretical_out_array = []
    sicta_out_array = []
    user_array = np.arange(k+1, n_stop)
    for n in user_array:
        throughput = []
        for _ in range(sim.sim_param.RUNS):
            # Reset the simulation
            sim.reset()
            sim.sim_param.K = k
            sim.sim_param.SPLIT = q
            sim.do_simulation_simple_tree_static(n)
            throughput.append(sim.sim_result.throughput/sim.sim_param.K)
        throughput_array.append(np.mean(throughput))
        theoretical_out_array.append(TheoreticalPlots().qarysic(n, k, q))
    theoretical_out = TheoreticalPlots().qarysic(n_stop, k, q)
    pyplot.plot(user_array, throughput_array,  'b-', label='simulation')
    pyplot.plot(user_array, theoretical_out_array, 'r', label='theoretical')
    pyplot.hlines(theoretical_out, sim.sim_param.K, n_stop, colors='green', label='Steady State')
    pyplot.legend()
    end = time.time()
    print("Time for simulation: ")
    print(end-start)
    pyplot.show()

def simulate_simple_tree_dynamic_multiple_runs():
    sim = Simulation()
    rate_array = np.arange(sim.sim_param.start, sim.sim_param.stop, sim.sim_param.step)
    succ_rate = []
    delay = []
    for p in rate_array:
        counter1 = []
        counter2 = []
        for _ in range(sim.sim_param.RUNS):
            sim.reset()
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


def simulate_simple_tree_dynamic_multiple_runs_gated():
    sim = Simulation()
    rate_array = np.arange(sim.sim_param.start, sim.sim_param.stop, sim.sim_param.step)
    delay = []
    for p in rate_array:
        counter = []
        for _ in range(sim.sim_param.RUNS):
            sim.reset()
            sim.sim_param.lmbda = p
            sim.do_simulation_gated_access()
            counter.append(sim.sim_result.mean_packet_delay)
        delay.append(np.mean(counter))
    pyplot.plot(rate_array, delay, color='blue')
    pyplot.xlabel('Arrival rate (packets/slot)')
    pyplot.ylabel('Mean Packet Delay')
    pyplot.grid()
    pyplot.show()

def do_theoretical_iter():
    param = SimParam()
    users = range(param.K, 12)
    theoretical = []
    for n in users:
        #output = TheoreticalPlots().qarysic(n)
        output = TheoreticalPlots().simpletree(n)
        theoretical.append(output)
        # print(output)
    pyplot.plot(users, theoretical)
    pyplot.hlines(0.35, param.K - 2, 12)
    pyplot.show()
    # print(TheoreticalPlots().mycomb(4,2))

def print_theoretical_result():
    start = time.time()
    theoretical = TheoreticalPlots()
    users = 30
    # Equation 16 or 32- Q ary with/without SIC with multipacket k
    #print(theoretical.qarysic(users))
    # Equation 30 from SICTA paper
    #print(theoretical.sicta(users))
    # Simple Tree from Massey Paper (recursive) Equation no- 3.13
    #print(theoretical.simpletree(users))
    # Equation 41 or 45 - Q ary with/without SIC with multipacket K but recursive
    print(theoretical.recquary(users))


if __name__ == '__main__':
    # Seed for reproducibility
    # np.random.seed(7)
    # Comment and uncomment the below methods as it suits
    simulate_tree_branching()
    #simulate_simple_tree_static_multiple_runs()
    #simulate_sic_oscillations(30, 2, 2)
    #simulate_simple_tree_dynamic_multiple_runs()
    # simulate_simple_tree_dynamic_multiple_runs_gated()
    #do_theoretical_iter()
    #print_theoretical_result()







