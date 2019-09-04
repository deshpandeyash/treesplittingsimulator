import numpy as np
from packet import Packet

"""
This is just a collection of useful functions to make operations on the packet list as this helps in readability
in the code above
"""


def dec_packet_count(sim, count):
    """
    decrements the count in the packet_count of each packet in the packet array
    :param sim: the simulation object instance
    :param count: the counts to decrement

    """
    for j in sim.active_array:
        j.packet_count -= count


def inc_uncollided_packet_count(sim):
    """
    decrements the count in the packet_count of each uncollided packet in the packet array
    :param sim: the simulation object instance

    """
    for j in sim.active_array:
        if j.packet_count != 0:
            j.packet_count += 1


def binsplit_uncollided_packet_count(sim):
    """
    performs a binary split with given branching probability, if the count is 0 , i,e the packets have collided
    :param sim: the simulation object instance

    """
    for j in sim.active_array:
        if j.packet_count == 0:
            j.packet_count += np.random.binomial(1, sim.sim_param.branchprob)


def unisplit_uncollided_packet_count(sim):
    """
    performs a uniform split where each packet chooses a random slot between 0 and the number of collided packets
    :param sim: the simulation object instance
    """
    for j in sim.active_array:
        if j.packet_count == 0:
            j.packet_count += np.random.randint(0, sim.slot.no_collided_packets)


def sort_packet_array(sim):
    """
    Sorts the packet array according to packet_count in an ascending order
    :param sim: the simulation object instance

    """
    sim.active_array.sort(key=lambda c: c.packet_count)


def extract_packet_count(sim):
    """

    :param sim: the simulation object instance
    :return: list of just the packet counts (integers) for the active string
    """
    return [x.packet_count for x in sim.active_array]

def extract_tx_packets(sim):
    """

    :param sim:
    :return:
    """
    tx_packet_array = []
    for j in sim.active_array:
        if j.packet_count == 0:
            tx_packet_array.append(j)
    return tx_packet_array

def extract_packet_id(tx_packet_array):
    """

    :param sim:
    :return:
    """
    return [x.packetID for x in tx_packet_array]


def add_packets_to_tree(sim):
    """
    Packets are added to the active array, the attributes of the packet are the arrival slot and its own number
    the number of packets are given by sim.packets_gen
    :param sim: the simulation object instance
    """
    for j in range(0, sim.packets_gen):
        sim.active_array.append(Packet(sim.slot_no, sim.sim_state.total_arrivals + j + 1))


def add_packets_to_queue(sim):
    """

    :param sim:
    :return:
    """
    for j in range(0, sim.packets_gen):
        sim.queue_array.append(Packet(sim.slot_no, sim.sim_state.total_arrivals + len(sim.queue_array) + j + 1))



def remove_successful_packet(sim):
    """
    The index 0 is removed from the active array and the removed packet is returned
    :param sim: the simulation object instance
    :return: the successful packet
    """

    pack = sim.active_array.pop(0)
    pack.life_time = sim.slot_no - pack.birth_time
    return pack



def update_transmissions(sim):
    """
    the number of transmissions attribute of the packet is increment if the count in is 0
    :param sim: the simulation object instance
    """
    for j in sim.active_array:
        if j.packet_count == 0:
            j.transmissions += 1




