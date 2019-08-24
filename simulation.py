import numpy as np
from simparam import SimParam
from simpletreeslot import SimpleTreeSlot
from packet import Packet
from matplotlib import pyplot
import math
import time

# Load simulation parameters
sim = SimParam()
# Load the methods governing simple tree resolution in this
simpletree = SimpleTreeSlot()
np.random.seed(sim.seed)
# Create an array of integers of which will contain all active nodes.
active_array = []
# Arrays to see the distribution of arrivals and packet delays
delay_stat_array = []
arrival_stat_array = []
# These two keep a count of arrivals and successes
total_arrivals = 0
total_successes = 0
slot_array = np.arange(0,sim.runs)
# Run simulation for the number of slots
for slot_no in slot_array:
    # Generate a packet according to poisson distribution
    packets_gen = np.random.poisson(sim.lmbda)
    arrival_stat_array.append(packets_gen)
    # Keep track of total arrivals
    for _ in range(0, packets_gen):
        total_arrivals = total_arrivals + 1
        active_array.append(Packet(slot_no, total_arrivals))
    # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
    active_array, result = simpletree.oneslotprocess(active_array, printit=False)
    # Keep track of successes
    if result == 1:
        total_successes = total_successes + 1
        popper = active_array.pop(0)
        packet_delay = slot_no - popper.birth_time
        delay_stat_array.append(packet_delay)
# print throughput
print("Throughput = " + str(total_successes/total_arrivals))
print("Mean Packet Delay = " + str(np.mean(delay_stat_array)))
print("Max packet delay = " + str(max(delay_stat_array)))
# Plots for distributions of arrivals and delays
pyplot.subplot(121)
pyplot.hist(delay_stat_array)
pyplot.subplot(122)
pyplot.hist(arrival_stat_array)
pyplot.show()


