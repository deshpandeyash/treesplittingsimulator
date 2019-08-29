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


def simulate_simple_tree_static(sim, modified=False,unisplit=False,sic=False):
    # Reset the simualtion
    sim.reset()
    # Perform simple tree which is static
    sim.do_simulation_simple_tree_static(1000, modified=modified,unisplit=unisplit,sic=sic)
    print("Throughput = " + str(sim.sim_result.throughput))
    print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
    print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
    print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
    print("Max packet retx = " + str(sim.sim_result.max_no_tx))
    print("Succ Rate = " + str(sim.sim_result.succ_rate))


def simulate_simple_tree_static_multpile_runs(sim, modified=False, unisplit=False,sic=False):
    throughput = []
    for _ in range(sim.sim_param.RUNS):
        # Reset the simulation
        sim.reset()
        sim.do_simulation_simple_tree_static(1000, modified=modified, unisplit=unisplit,sic=sic)
        throughput.append(sim.sim_result.throughput)
    print("Mean Throughput is = " + str(np.mean(throughput)))
    pyplot.hist(throughput, density=True)
    pyplot.show()


def simulate_simple_tree_dynamic_multiple_runs(sim,modified=False,unisplit=False,sic=False):
    rate_array = np.arange(0.15, 0.75, 0.05)
    succ_rate = []
    delay = []
    for sim.sim_param.lmbda in rate_array:
        counter1 = []
        counter2 = []
        for _ in range(sim.sim_param.RUNS):
            sim.reset()
            sim.do_simulation_simple_tree_dynamic(modified=modified,unisplit=unisplit, sic=sic)
            counter1.append(sim.sim_result.succ_rate)
            counter2.append(sim.sim_result.mean_packet_delay)
        succ_rate.append(counter1)
        delay.append(counter2)
    pyplot.subplot(121)
    pyplot.plot(rate_array, succ_rate)
    pyplot.subplot(122)
    pyplot.plot(rate_array, delay)
    pyplot.show()


if __name__ == '__main__':
    # Create the simulation object
    sim = Simulation()
    # Seed for reproducibility
    #np.random.seed(sim.sim_param.seed)
    # Comment and uncomment the below methods as it suits
    # simulate_simple_tree_dynamic(sim,modified=False,unisplit=False, sic=False)
    # simulate_simple_tree_static(sim, modified=False, unisplit=False, sic=True)
    # simulate_simple_tree_static_multpile_runs(sim, modified=False, unisplit=False)
    simulate_simple_tree_dynamic_multiple_runs(sim, modified=False, unisplit=False, sic=False)

