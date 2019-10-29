from simulation import Simulation
from matplotlib import pyplot
import numpy as np
import time
from theoretical_plots import TheoreticalPlots
from scipy.optimize import curve_fit


def func(x, a, b, c):
    return a * np.exp(-b * x) + c

def simulate_tree_branching():
    sim = Simulation()
    sim.reset()
    sim.do_simulation_simple_tree_static(5)
    print("Results were: ")
    print(sim.tree_state.result_array)
    print("Tree Progression was: ")
    print(sim.branch_node.branch_array[:-1])
    print("Mean Throughput is = " + str(sim.sim_result.throughput))
    print("The Depth of the tree is: " + str(sim.sim_result.mean_tree_depth))


def simulate_simple_tree_static_multiple_runs():
    start = time.time()
    sim = Simulation()
    throughput = []
    for _ in range(sim.sim_param.RUNS):
        # Reset the simulation
        sim.reset()
        sim.do_simulation_simple_tree_static(1000)
        throughput.append(sim.sim_result.throughput)
    print("Mean Throughput is = " + str(np.mean(throughput)))
    pyplot.hist(throughput, density=True)
    pyplot.show()
    print("Theoretical Output Should be: ")
    print(TheoreticalPlots().qarysic())
    end = time.time()
    print("Time for simulation: ")
    print(end-start)


def simulate_sic_oscillations(n_stop, k):
    start = time.time()
    sim = Simulation()
    throughput_array = []
    user_array = np.arange(k+1, n_stop)
    for n in user_array:
        throughput = []
        for _ in range(sim.sim_param.RUNS):
            # Reset the simulation
            sim.reset()
            sim.sim_param.K = k
            sim.do_simulation_simple_tree_static(n)
            throughput.append(sim.sim_result.throughput/sim.sim_param.K)
        throughput_array.append(np.mean(throughput))
    theoretical_out = TheoreticalPlots().qarysic(40)
    #popt, pcov = curve_fit(func, user_array, throughput_array)
    #fit = np.polyfit(np.asarray(user_array), np.log(throughput_array), 1)
    #y = np.exp(fit[1]) * np.exp(fit[0] * user_array)
    #print(fit)
    pyplot.plot(user_array, throughput_array,  'b-', label='data')
    pyplot.hlines(theoretical_out, sim.sim_param.K, n_stop, colors='green', label='Steady State')
    #pyplot.plot(user_array, func(user_array, *popt), 'r-', label = 'fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    #pyplot.plot(user_array, y, 'r-', label='fit')
    pyplot.legend()
    pyplot.show()
    print("Theoretical Output Should be: ")
    print(theoretical_out)
    end = time.time()
    print("Time for simulation: ")
    print(end-start)




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


if __name__ == '__main__':
    # Seed for reproducibility
    # np.random.seed(7)
    # Comment and uncomment the below methods as it suits
    # simulate_tree_branching()
    # simulate_simple_tree_static_multiple_runs()
    simulate_sic_oscillations(100, 4)
    #simulate_simple_tree_dynamic_multiple_runs()
    # simulate_simple_tree_dynamic_multiple_runs_gated()
    #print(TheoreticalPlots().qarysic())





