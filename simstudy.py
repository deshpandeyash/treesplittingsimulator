import numpy as np
from simulation import Simulation
from matplotlib import pyplot

# Create the simulation object
sim = Simulation()
# Seed for repeatability
#np.random.seed(sim.sim_param.seed)
# Do the simulation and load the output in arrays
sim.do_simulation()
# print throughput
print("Throughput = " + str(sim.sim_result.throughput))
print("Mean Packet Delay = " + str(sim.sim_result.mean_packet_delay))
print("Max packet delay = " + str(sim.sim_result.max_packet_delay))
print("Mean number of retx = " + str(sim.sim_result.mean_no_tx))
print("Max packet retx = " + str(sim.sim_result.max_no_tx))
# Plots for distributions of arrivals and delays
pyplot.subplot(121)
pyplot.hist(sim.sim_state.delay_stat_array)
pyplot.subplot(122)
pyplot.hist(sim.sim_state.arrival_stat_array)
pyplot.show()

