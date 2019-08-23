import numpy as np
from simparam import SimParam
import time


def oneslotprocess(arrival_array, printit=False):
    """
    this function simulates the reciever and transmitter behaviour for one time slot,
    the active packets and their waiting counts are kept in an arrival array and updated according to the event at the
    receiver ie Collisions, Idle or Success

    :param arrival_array: the array of all the active nodes in the system
    :param printit: whether to print for diagnostics
    :return: the updated array depending on the feedback
    """
    success = 0
    # Sort the array in ascending order
    arrival_array = np.sort(arrival_array)
    if printit:
        print(arrival_array)
    # If array is empty, it means no packet has arrived or is active in this slot
    if len(arrival_array) == 0:
        if printit:
            print("No Tx")
    # If array has just one element and it is 0 then transmit and clear the packet from the array
    elif len(arrival_array) == 1 and arrival_array[0] == 0:
        arrival_array = np.delete(arrival_array, 0)
        success = 1
        if printit:
            print("Success without waiting")
    # If the first element is 0 and the second element is not 0 then, we have no collision and a success
    elif arrival_array[0] == 0 and arrival_array[1] != 0:
        # On a success, all other packets reduce their count by 1 and we clear the transmitted packet
        arrival_array = arrival_array - 1
        arrival_array = np.delete(arrival_array, 0)
        # Success is used as a counter to count successful transmissions
        success = 1
        if printit:
            print("Success")
    # If the first element is not 0, it means that no one will will transmit even when there are active packets, ie IDLE
    elif arrival_array[0] != 0:
        # On an idle slot, all packets reduce their count by 1
        arrival_array = arrival_array - 1
        if printit:
            print("Idle")
    # If the first and second element ( at least) are 0 it means we have a collision
    elif arrival_array[0] == 0 and arrival_array[1] == 0:
        if printit:
            print("collision")
        # For collision, we must update the values in each packet
        for i in range(0, len(arrival_array)):
            # For packets which collided, we have to make a tree selection again
            if arrival_array[i] == 0:
                arrival_array[i] = arrival_array[i] + np.random.binomial(1, 0.5)
            # For other waiting packets, we just increase the count by 1
            else:
                arrival_array[i] = arrival_array[i] + 1
    # If anything else occurs, print immediately as its not expected.
    else:
        print("Error, unexpected array")
    return arrival_array, success


# Load simulation parameters
sim = SimParam()
np.random.seed(sim.seed)
# Create an array of integers of which will contain all active nodes.
active_array = np.zeros(0, dtype=int)
# These two keep a count of arrivals and succeses
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
    active_array, result = oneslotprocess(active_array, printit=False)
    # Keep track of successes
    total_successes = total_successes + result
# print throughput
print("Throughput = " + str(total_successes/total_arrivals))




