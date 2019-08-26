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
print("Throughput = " + str(sim.sim_state.total_successes / sim.sim_state.total_arrivals))
print("Mean Packet Delay = " + str(np.mean(sim.sim_state.delay_stat_array)))
print("Max packet delay = " + str(max(sim.sim_state.delay_stat_array)))
print("Mean number of retx = " + str(np.mean(sim.sim_state.tx_stat_array)))
print("Max packet retx = " + str(max(sim.sim_state.tx_stat_array)))
# Plots for distributions of arrivals and delays
pyplot.subplot(121)
pyplot.hist(sim.sim_state.delay_stat_array)
pyplot.subplot(122)
pyplot.hist(sim.sim_state.arrival_stat_array)
pyplot.show()

