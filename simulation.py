import numpy as np
from simparam import SimParam
from simpletreeslot import SimpleTreeSlot
from packet import Packet
import time

# Load simulation parameters
sim = SimParam()
# Load the methods governing simple tree resolution in this
simpletree = SimpleTreeSlot()
np.random.seed(sim.seed)
# Create an array of integers of which will contain all active nodes.
active_array = []
delay_array = []
# These two keep a count of arrivals and successes
total_arrivals = 0
total_successes = 0
# Run simulation for the number of slots
for slot_no in range(0, sim.runs):
    # Generate a packet according to poisson distribution
    packets_gen = np.random.poisson(sim.lmbda)
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
        delay_array.append(packet_delay)
# print throughput
print("Throughput = " + str(total_successes/total_arrivals))
print("Mean Packet Delay = " + str(np.mean(delay_array)))




