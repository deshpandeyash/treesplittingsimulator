import numpy as np
from simparam import SimParam
import time


def binsplit(packet_array, branchprob):
    """
    performs a binary split with given branching probability, if the count is 0 , i,e the packets have collided
    :param packet_array: the array of active packets with counts
    :param branchprob: branching probability
    :return: the updated array where the collided packets have drawn a 0 or 1 depending on the branching prob
    """
    # For collision, we must update the values in each packet
    packet_array = np.where(packet_array == 0, np.random.binomial(1, branchprob, len(packet_array)), packet_array)
    return packet_array


def txprocess(arrival_array, printit=False):
    """
    this simulates the process in a slot, the array of active packets in a slot fed to it,
    we transmit the packets which have count 0, and then wait for the feedback and update the count in the packets
    accordingly
    :param arrival_array: the array of active packets in the system
    :param printit: if printing needs to be done for diagnostics
    :return: the updated array and if this process resulted in a success
    """

    # this parameter is changed to 1 if the result from this slot is a success
    success = 0
    # Sort the array in ascending order
    arrival_array = np.sort(arrival_array)
    if printit:
        print("Arrival Array Before Tx")
        print(arrival_array)
    # Get the feedback form the receiver
    feedback = rxprocess(arrival_array, printit=False)
    if printit:
        print("Feedback" + str(feedback))
    # If Success
    if feedback == 1:
        # On a success, all other packets reduce their count by 1 and we clear the transmitted packet
        arrival_array = arrival_array - 1
        arrival_array = np.delete(arrival_array, 0)
        success = 1
    # If Idle
    elif feedback == 0:
        # On an idle slot, all packets reduce their count by 1
        arrival_array = arrival_array - 1
    # If Collision
    elif feedback == 2:
        # increment the count for uncollided packets
        arrival_array = np.where(arrival_array != 0, arrival_array + 1, arrival_array)
        # Update the counts on the collided packets according to a binary split
        arrival_array = binsplit(arrival_array, 0.5)


    # This is an error and means that the RX process did not change the feedback
    elif feedback == 9:
        print("Rx Process did not change give a Feedback")
    if printit:
        print("Arrival Array updated after feedback")
        print(arrival_array)

    return arrival_array, success

def rxprocess(active_packet_array, printit=False):
    """
    depending on the active packet array length and the count in each of its packets, this process decides whether there
    was in idle slot, collision or success after which it provides feedback,

    :param active_packet_array: the array that contains all the packets, this array is already sorted by the txprocess
    :param printit: if the feedback must be printed
    :return: feedback , 0 = Idle; 1 = Success; 2 = collision; 9 = Error
    """
    # This parameter is initialized to a 9, to make sure it is changed by the process. i.e the feedback is one of the
    # expected values
    feedback = 9
    # If the length of the array is 0 then there are no active packets, and no transmissions hence, IDLE
    # If the first element is not 0, it means that no one will transmit even when there are active packets, ie IDLE
    if len(active_packet_array) == 0 or active_packet_array[0] != 0:
        feedback = 0
        if printit:
            print("Idle")
    # If array has just one element and it is 0 then its a success
    elif len(active_packet_array) == 1 and active_packet_array[0] == 0:
        feedback = 1
        if printit:
            print("Success without waiting")
    # If the first element is 0 and the second element is not 0 then, we have no collision and a success
    elif active_packet_array[0] == 0 and active_packet_array[1] != 0:
        feedback = 1
        if printit:
            print("Success")
    # If the first and second element ( at least) are 0 it means we have a collision
    elif active_packet_array[0] == 0 and active_packet_array[1] == 0:
        feedback = 2
        if printit:
            print("collision")
    # If anything else occurs, print immediately as its not expected.
    else:
        print("Error, unexpected array")
    return feedback


# Load simulation parameters
sim = SimParam()
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
    active_array, result = txprocess(active_array, printit=False)
    # Keep track of successes
    total_successes = total_successes + result
# print throughput
print("Throughput = " + str(total_successes/total_arrivals))




