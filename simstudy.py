import numpy as np
from simulation import Simulation
from matplotlib import pyplot

# Create the simulation object
sim = Simulation()
# Seed for repeatability
np.random.seed(sim.sim_param.seed)
# Do the simulation and load the output in arrays
sim.do_simulation()
# print throughput
print("Throughput = " + str(sim.sim_result.total_successes / sim.sim_result.total_arrivals))
print("Mean Packet Delay = " + str(np.mean(sim.sim_result.delay_stat_array)))
print("Max packet delay = " + str(max(sim.sim_result.delay_stat_array)))
print("Mean number of retx = " + str(np.mean(sim.sim_result.tx_stat_array)))
print("Max packet retx = " + str(max(sim.sim_result.tx_stat_array)))
# Plots for distributions of arrivals and delays
pyplot.subplot(121)
pyplot.hist(sim.sim_result.delay_stat_array)
pyplot.subplot(122)
pyplot.hist(sim.sim_result.arrival_stat_array)
pyplot.show()
