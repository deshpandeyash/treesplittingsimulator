import numpy as np
from simparam import SimParam
from simpletreeslot import SimpleTreeSlot
from packet import Packet
from matplotlib import pyplot
from packetlist import PacketList
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
tx_stat_array = []
# These two keep a count of arrivals and successes
total_arrivals = 0
total_successes = 0
slot_array = np.arange(0, sim.runs)
# Run simulation for the number of slots
for slot_no in slot_array:
    # Generate a packet according to poisson distribution
    packets_gen = np.random.poisson(sim.lmbda)
    # Add the number of packets to statistical array for diagnosis
    arrival_stat_array.append(packets_gen)
    # Add the number of packets to the active packet array
    active_array = PacketList().add_packets(slot_no, total_arrivals, packets_gen, active_array)
    # Keep track of total arrivals
    total_arrivals += packets_gen
    # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
    active_array, result = simpletree.oneslotprocess(active_array, printit=False)
    # Keep track of successes
    if result == 1:
        total_successes += 1
        active_array, successful_pack = PacketList().remove_successful_packet(active_array, slot_no)
        delay_stat_array.append(successful_pack.life_time)
        tx_stat_array.append(successful_pack.transmissions)
# print throughput
print("Throughput = " + str(total_successes/total_arrivals))
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


