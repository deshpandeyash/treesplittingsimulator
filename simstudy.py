from simulation import Simulation
from matplotlib import pyplot
import numpy as np


def simulate_simple_tree_dynamic(sim, modified=False, unisplit=False):
    # Reset all the simulation
    sim.reset()
    # Do the simulation
    sim.do_simulation_simple_tree_dynamic(modified=modified,unisplit=unisplit)
    # print Results
    print("Throughput = " + str(sim.sim_result.throughput))
    print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
    print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
    print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
    print("Max packet retx = " + str(sim.sim_result.max_no_tx))
    # Plots for distributions of arrivals and delays
    # pyplot.subplot(121)
    # pyplot.hist(sim.sim_state.delay_stat_array)
    # pyplot.subplot(122)
    # pyplot.hist(sim.sim_state.arrival_stat_array)
    # pyplot.show()


def simulate_simple_tree_static(sim, modified=False,unisplit=False):
    # Reset the simualtion
    sim.reset()
    # Perform simple tree which is static
    sim.do_simulation_simple_tree_static(1000, modified=modified,unisplit=unisplit)
    print("Throughput = " + str(sim.sim_result.throughput))
    print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
    print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
    print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
    print("Max packet retx = " + str(sim.sim_result.max_no_tx))

def simulate_sic_tree_static(sim, modified=False,unisplit=False,sic=False):
    # Reset the simualtion
    sim.reset()
    # Perform simple tree which is static
    sim.do_simulation_sic_tree_static(1000, modified=modified,unisplit=unisplit,sic=sic)
    print("Throughput = " + str(sim.sim_result.throughput))
    print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
    print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
    print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
    print("Max packet retx = " + str(sim.sim_result.max_no_tx))


def simulate_simple_tree_static_multpile_runs(sim, modified=False, unisplit=False):
    throughput = []
    for _ in range(sim.sim_param.RUNS):
        # Reset the simulation
        sim.reset()
        sim.do_simulation_simple_tree_static(1000, modified=modified, unisplit=unisplit)
        throughput.append(sim.sim_result.throughput)
    print("Mean Throughput is = " + str(np.mean(throughput)))
    pyplot.hist(throughput, density=True)
    pyplot.show()



if __name__ == '__main__':
    # Create the simulation object
    sim = Simulation()
    # Seed for reproducibility
    #np.random.seed(sim.sim_param.seed)
    # Comment and uncomment the below methods as it suits
    # simulate_simple_tree_dynamic(sim,modified=False)
    # simulate_simple_tree_static(sim, modified=True,unisplit=True)
    # simulate_simple_tree_static_multpile_runs(sim, modified=False, unisplit=False)
    simulate_sic_tree_static(sim, modified=False, unisplit=False,sic=True)
    # simulate_sic_tree_static_multpile_runs(sim, modified=True, unisplit=False)


