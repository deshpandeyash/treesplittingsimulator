import numpy as np
from simparam import SimParam
from simpletreeslot import SimpleTreeSlot
from simresult import SimResult
import packetlist


class Simulation(object):

    def __init__(self):
        # Load simulation parameters
        self.sim_param = SimParam()
        # Load the variables for statistical simualtion
        self.sim_result = SimResult()
        # Load the methods governing simple tree resolution in this
        self.simpletree = SimpleTreeSlot(self.sim_param)
        # Create an array of integers of which will contain all active nodes.
        self.active_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)

    def reset(self):
        self.sim_param = SimParam()
        self.simpletree = SimpleTreeSlot(self.sim_param)
        self.active_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)

    def do_simulation(self):
        # Run simulation for the number of slots
        for slot_no in self.slot_array:
            # Generate a packet according to poisson distribution
            packets_gen = np.random.poisson(self.sim_param.lmbda)
            # Add the number of packets to statistical array for diagnosis
            self.sim_result.arrival_stat_array.append(packets_gen)
            # Add the number of packets to the active packet array
            active_array = packetlist.add_packets(slot_no, self.sim_result.total_arrivals, packets_gen, self.active_array)
            # Keep track of total arrivals
            self.sim_result.total_arrivals += packets_gen
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.active_array, result = self.simpletree.oneslotprocess(active_array, printit=False)
            # Keep track of successes
            if result == 1:
                self.sim_result.total_successes += 1
                self.active_array, successful_pack = packetlist.remove_successful_packet(active_array, slot_no)
                self.sim_result.delay_stat_array.append(successful_pack.life_time)
                self.sim_result.tx_stat_array.append(successful_pack.transmissions)



