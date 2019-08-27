import numpy as np
from packet import Packet

"""
This is just a collection of useful functions to make operations on the packet list as this helps in readability
in the code above
"""


def dec_packet_count(sim):
    """
    decrements the count in the packet_count of each packet in the packet array
    :param packet_array: the list of all packets
    :return: list of all packets with the decremented packet_count
    """
    for j in sim.active_array:
        j.packet_count -= 1


def inc_uncollided_packet_count(sim):
    """
    decrements the count in the packet_count of each uncollided packet in the packet array
    :param packet_array: the list of all packets
    :return: list of all packets with the decremented packet_count
    """
    for j in sim.active_array:
        if j.packet_count != 0:
            j.packet_count += 1


def binsplit_uncollided_packet_count(sim):
    """
    performs a binary split with given branching probability, if the count is 0 , i,e the packets have collided
    :param packet_array: the array of active packets
    :param branchprob: the branching probability for the binary split
    :return: the updated array where the collided packets have drawn a 0 or 1 depending on the branching prob
    """
    for j in sim.active_array:
        if j.packet_count == 0:
            j.packet_count += np.random.binomial(1, sim.sim_param.branchprob)


def sort_packet_array(sim):
    """
    Sorts the packet array according to packet_count in an ascending order
    :param packet_array: the list of all packets
    :return: the  sorted list of all packets
    """
    sim.active_array.sort(key=lambda c: c.packet_count)



def extract_packet_count(sim):
    return [x.packet_count for x in sim.active_array]


def add_packets(sim):
    for j in range(0, sim.packets_gen):
        sim.active_array.append(Packet(sim.slot_no, sim.sim_state.total_arrivals + j + 1))

def remove_successful_packet(sim):
    pack = sim.active_array.pop(0)
    pack.life_time = sim.slot_no - pack.birth_time
    return pack


def update_transmissions(sim):
    for j in sim.active_array:
        if j.packet_count == 0:
            j.transmissions += 1




