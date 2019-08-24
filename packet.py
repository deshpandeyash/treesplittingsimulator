class Packet(object):
    """
    This class is to define the functions of a packet and what its attributes should be, how it must be sorted
    """

    def __init__(self, slot_number, packet_number):
        self.packetID = packet_number
        self.packet_count = 0
        self.birth_time = slot_number

    def __cmp__(self, other):
        if self.packet_count < other.packet_count:
            return True

