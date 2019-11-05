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


def inc_uncollided_packet_count(sim, count):
    """
    increments the count in the packet_count of each uncollided packet in the packet array
    :param sim: the simulation object instance
    :param count: decrement by this count

    """
    for j in sim.active_array:
        if j.packet_count > 0:
            j.packet_count += count

# Not used for now
def inc_uncolliding_packet_count(sim, count):
    """
    increments the count in the packet_count of each uncolliding packet in the packet array
    useful when modified trees are implemented
    :param sim: the simulation object instance
    :param count: the count by which to increment

    """
    for j in sim.active_array:
        if j.packet_count > 1:
            j.packet_count += count


def split_uncollided_packet_count(sim):
    """
    performs a uniform split where each packet chooses a random slot between 0 and the number of collided packets
    :param sim: the simulation object instance
    """
    for j in sim.active_array:
        if j.packet_count == 0:
            if sim.sim_param.SPLIT == 2:
                if sim.sim_param.biased_split:
                    drawn_count = np.random.binomial(1, sim.sim_param.branchprob)
                else:
                    drawn_count = np.random.binomial(1, 0.5)
            else:
                if sim.sim_param.biased_split:
                    drawn_count = np.random.choice(sim.sim_param.SPLIT, 1, p=sim.sim_param.branch_biased)
                else:
                    drawn_count = np.random.randint(sim.sim_param.SPLIT)
            j.packet_count += drawn_count
            j.selected_branch = str(sim.sim_param.SPLIT - 1 - drawn_count)


def split_colliding_packet_count(sim):
    """
    performs a uniform split where each packet chooses a random slot between 0 and the number of collided packets
    This is used when modified trees are to be implemented where we avoid a deterministic collision
    :param sim: the simulation object instance
    """

    for j in sim.active_array:
        if j.packet_count == 1:
            if sim.sim_param.SPLIT == 2:
                if sim.sim_param.biased_split:
                    j.packet_count = 0 + np.random.binomial(1, sim.sim_param.branchprob)
                else:
                    j.packet_count = 0 + np.random.binomial(1, 0.5)
            else:
                if sim.sim_param.biased_split:
                    j.packet_count = 0 + np.random.choice(sim.sim_param.SPLIT, 1, p=sim.sim_param.branch_biased)
                else:
                    j.packet_count = 0 + np.random.randint(sim.sim_param.SPLIT)


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

    :param sim: The simulation object instance
    :return: list of packets which are about to transmit, i.e whose count is 0
    """
    tx_packet_array = []
    for j in sim.active_array:
        if j.packet_count == 0:
            tx_packet_array.append(j)
    return tx_packet_array


def extract_packet_id(tx_packet_array):
    """
    extracts the packet IDs from a given input array
    :param tx_packet_array: the input array
    :return: a list of the packet IDs form the given input array
    """
    return [x.packetID for x in tx_packet_array]


def add_packets_to_tree(sim):
    """
    Packets are added to the active array, the attributes of the packet are the arrival slot and its own number

    :param sim: the simulation object instance
    """
    for j in range(0, sim.packets_gen):
        sim.active_array.append(Packet(sim.slot_no, sum(sim.sim_state.arrival_stat_array) + j + 1))


def add_packets_to_queue(sim):
    """
    Packets are added to the queue because an ongoing resolution during gated access simulation.
    The attributes of the packet are the arrival slot and its own number,

    :param sim:
    :return:
    """
    for j in range(0, sim.packets_gen):
        sim.queue_array.append(Packet(sim.slot_no, sum(sim.sim_state.arrival_stat_array) + j + 1))


def remove_successful_packet(sim):
    """
    The index 0 is removed from the active array and the removed packet is returned
    :param sim: the simulation object instance
    :return: the successful packet
    """

    pack = sim.active_array.pop(0)
    pack.life_time = sim.slot_no - pack.birth_time
    if not sim.sim_param.sic:
        if pack.selected_branch != sim.branch_node.success_branch:
            print("Error success branch different from selected branch at split")
    return pack


def update_transmissions(sim):
    """
    the number of transmissions attribute of the packet is increment if the count in is 0
    :param sim: the simulation object instance
    """
    for j in sim.active_array:
        if j.packet_count == 0:
            j.transmissions += 1




