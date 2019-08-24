import numpy as np
from simparam import SimParam

class Packet(object):

    def __init__(self):
        self.packetID = 0
        self.packet_count = 0
        self.birth_time = 0
        self.death_time = 0
        self.packet_delay = 0

    def create_packet(self, packet_number, slot_number):
        self.packetID = packet_number
        self.birth_time = slot_number
        