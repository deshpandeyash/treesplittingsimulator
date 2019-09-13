from simulation import Simulation
from matplotlib import pyplot
import numpy as np


def simulate_simple_tree_dynamic(sim, modified=False, unisplit=False,sic=False):
    # Reset all the simulation
    sim.reset()
    # Do the simulation
    sim.do_simulation_simple_tree_dynamic(modified=modified,unisplit=unisplit,sic=sic)
    # print Results
    print("Throughput = " + str(sim.sim_result.throughput))
    print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
    print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
    print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
    print("Max packet retx = " + str(sim.sim_result.max_no_tx))
    print("Succ Rate = " + str(sim.sim_result.succ_rate))
    # Plots for distributions of arrivals and delays
    # pyplot.subplot(121)
    # pyplot.hist(sim.sim_state.delay_stat_array)
    # pyplot.subplot(122)
    # pyplot.hist(sim.sim_state.arrival_stat_array)
    # pyplot.show()


def simulate_simple_tree_static(modified=False, unisplit=False, sic=False):
    sim = Simulation()
    # Reset the simualtion
    sim.reset()
    # Perform simple tree which is static
    sim.do_simulation_simple_tree_static(3, modified=modified, unisplit=unisplit, sic=sic)
    print("Throughput = " + str(sim.sim_result.throughput))
    print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
    print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
    print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
    print("Max packet retx = " + str(sim.sim_result.max_no_tx))
    print("Succ Rate = " + str(sim.sim_result.succ_rate))


def simulate_simple_tree_static_multpile_runs(modified=False, unisplit=False,sic=False):
    sim = Simulation()
    throughput = []
    for _ in range(sim.sim_param.RUNS):
        # Reset the simulation
        sim.reset()
        sim.do_simulation_simple_tree_static(1000, modified=modified, unisplit=unisplit,sic=sic)
        throughput.append(sim.sim_result.throughput)
    print("Mean Throughput is = " + str(np.mean(throughput)))
    pyplot.hist(throughput, density=True)
    pyplot.show()


def simulate_simple_tree_dynamic_multiple_runs(modified=False, unisplit=False, sic=False):
    sim = Simulation()
    rate_array = np.arange(0.20, 0.50, 0.05)
    succ_rate = []
    delay = []
    for p in rate_array:
        counter1 = []
        counter2 = []
        for _ in range(sim.sim_param.RUNS):
            sim.reset()
            sim.sim_param.lmbda = p
            sim.do_simulation_simple_tree_dynamic(modified=modified, unisplit=unisplit, sic=sic)
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


def simulate_simple_tree_dynamic_multiple_runs_gated(modified=False, unisplit=False, sic=False):
    sim = Simulation()
    rate_array = np.arange(0.20, 0.90, 0.05)
    delay = []
    for p in rate_array:
        counter = []
        for _ in range(sim.sim_param.RUNS):
            sim.reset()
            sim.sim_param.lmbda = p
            sim.do_simulation_gated_access(modified=modified, unisplit=unisplit, sic=sic)
            counter.append(sim.sim_result.mean_packet_delay)
        delay.append(np.mean(counter))
    pyplot.plot(rate_array, delay, color='blue')
    pyplot.xlabel('Arrival rate (packets/slot)')
    pyplot.ylabel('Mean Packet Delay')
    pyplot.grid()
    pyplot.show()


if __name__ == '__main__':
    # Create the simulation object
    #sim = Simulation()
    # Seed for reproducibility
    np.random.seed(7)
    # Comment and uncomment the below methods as it suits
    # simulate_simple_tree_dynamic(sim,modified=False,unisplit=False, sic=False)
    # simulate_simple_tree_static(modified=False, unisplit=False, sic=False)
    simulate_simple_tree_static_multpile_runs(modified=True, unisplit=False, sic=True)
    # simulate_simple_tree_dynamic_multiple_runs(modified=True, unisplit=False, sic=False)
    # simulate_simple_tree_dynamic_multiple_runs_gated(modified=True, unisplit=False, sic=True)


