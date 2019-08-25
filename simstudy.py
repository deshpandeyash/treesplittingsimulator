import numpy as np
from simulation import Simulation
from matplotlib import pyplot

# Create the simulation object
sim = Simulation()
# Seed for repeatability
np.random.seed(sim.sim_param.seed)
# Do the simulation and load the output in arrays
total_arrivals, total_successes, delay_stat_array, tx_stat_array, arrival_stat_array = sim.do_simulation()
# print throughput
print("Throughput = " + str(total_successes / total_arrivals))
print("Mean Packet Delay = " + str(np.mean(delay_stat_array)))
print("Max packet delay = " + str(max(delay_stat_array)))
print("Mean number of retx = " + str(np.mean(tx_stat_array)))
print("Max packet retx = " + str(max(tx_stat_array)))
# Plots for distributions of arrivals and delays
pyplot.subplot(121)
pyplot.hist(delay_stat_array)
pyplot.subplot(122)
pyplot.hist(arrival_stat_array)
pyplot.show()
