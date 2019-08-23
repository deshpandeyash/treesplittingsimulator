import numpy as np
from simparam import SimParam
from simpletreeslot import SimpleTreeSlot
import time

# Load simulation parameters
sim = SimParam()
slot = SimpleTreeSlot()
np.random.seed(sim.seed)
# Create an array of integers of which will contain all active nodes.
active_array = np.zeros(0, dtype=int)
# These two keep a count of arrivals and successes
total_arrivals = 0
total_successes = 0
# Run simulation for the number of slots
for _ in range(0, sim.runs):
    # Generate a packet according to poisson distribution
    packets_gen = np.random.poisson(sim.lmbda)
    # Keep track of total arrivals
    total_arrivals = total_arrivals + packets_gen
    # Create and array for these new arrivals in a time slot
    new_packets = np.zeros(packets_gen, dtype=int)
    # Add these packets to the array of active packets
    active_array = np.concatenate((active_array, new_packets))
    # Transmit and update it in one slot
    active_array, result = slot.oneslotprocess(active_array, printit=False)
    # Keep track of successes
    total_successes = total_successes + result
# print throughput
print("Throughput = " + str(total_successes/total_arrivals))




