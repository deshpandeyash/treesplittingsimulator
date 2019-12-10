import numpy.random


class Packet(object):
    """
    This class is to define the functions of a packet and what its attributes should be, how it must be sorted
    """

    def __init__(self, slot_number, packet_number, branch_status):
        self.packetID = packet_number
        self.packet_count = 0
        self.birth_time = slot_number
        self.life_time = 0
        self.transmissions = 0
        self.rng = numpy.random.RandomState()
        if len(branch_status) == 0:
            self.selected_branch = branch_status
        else:
            self.selected_branch = branch_status[-1]

    # To better sort the array of packets
    def __cmp__(self, other):
        if self.packet_count < other.packet_count:
            return True

    def split(self, sim):
        if self.packet_count == 0:
            if sim.sim_param.SPLIT == 2:
                if sim.sim_param.biased_split:
                    drawn_count = self.rng.binomial(1, sim.sim_param.branchprob)
                else:
                    drawn_count = self.rng.binomial(1, 0.5)
            else:
                if sim.sim_param.biased_split:
                    drawn_count = self.rng.random.choice(sim.sim_param.SPLIT, 1, p=sim.sim_param.branch_biased)
                else:
                    drawn_count = self.rng.randint(sim.sim_param.SPLIT)
            self.packet_count += drawn_count
            self.selected_branch = str(sim.sim_param.SPLIT - 1 - drawn_count)

    def unisplit(self,sim):
        if self.packet_count == 0:
            drawn_count = self.rng.random.randint(0, sim.slot.no_collided_packets)
            self.packet_count += drawn_count
            self.selected_branch = str(sim.slot.no_collided_packets - 1 - drawn_count)

    def inc_count(self, count):
        if self.packet_count > 0:
            self.packet_count += count

    def dec_count(self, count):
        self.packet_count -= count


