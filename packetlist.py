import numpy as np


class PacketList(object):
    """
    This is just a collection of useful functions to make operations on the packet list as this helps in readability
    in the code above
    """

    def dec_packet_count(self, packet_array):
        """
        decrements the count in the packet_count of each packet in the packet array
        :param packet_array: the list of all packets
        :return: list of all packets with the decremented packet_count
        """
        for j in packet_array:
            j.packet_count = j.packet_count - 1
        return packet_array

    def inc_uncollided_packet_count(self, packet_array):
        """
        decrements the count in the packet_count of each uncollided packet in the packet array
        :param packet_array: the list of all packets
        :return: list of all packets with the decremented packet_count
        """
        for j in packet_array:
            if j.packet_count != 0:
                j.packet_count = j.packet_count + 1
        return packet_array

    def binsplit_uncollided_packet_count(self, packet_array, branchprob):
        """
        performs a binary split with given branching probability, if the count is 0 , i,e the packets have collided
        :param packet_array: the array of active packets
        :param branchprob: the branching probability for the binary split
        :return: the updated array where the collided packets have drawn a 0 or 1 depending on the branching prob
        """
        for j in packet_array:
            if j.packet_count == 0:
                j.packet_count = j.packet_count + np.random.binomial(1, branchprob)
        return packet_array

    def sort_packet_array(self, packet_array):
        """
        Sorts the packet array according to packet_count in an ascending order
        :param packet_array: the list of all packets
        :return: the  sorted list of all packets
        """
        packet_array.sort(key=lambda c: c.packet_count)
        return packet_array

    def extract_packet_count(self, packet_array):
        return [x.packet_count for x in packet_array]

