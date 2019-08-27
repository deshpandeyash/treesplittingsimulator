import numpy as np
from simparam import SimParam
from simpletreeslot import SimpleTreeSlot
from modifiedtreeslot import ModifiedTreeSlot
from simstate import SimState
from simresult import SimResult
import packetlist


class Simulation(object):

    def __init__(self):
        # Load simulation parameters
        self.sim_param = SimParam()
        # Load the simulation state parameters
        self.sim_state = SimState()
        # Load the result parameters
        self.sim_result = SimResult()
        # Load the methods governing simple tree resolution in this
        self.simpletree = SimpleTreeSlot(self.sim_param)
        # Create an array of integers of which will contain all active nodes.
        self.active_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)
        self.packets_gen = 0
        self.result = 0
        self.slot_no = 0

    def reset(self):
        self.sim_param = SimParam()
        self.sim_state = SimState()
        self.sim_result = SimResult()
        self.simpletree = SimpleTreeSlot(self.sim_param)
        self.active_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)
        self.packets_gen = 0
        self.result = 0
        self.slot_no = 0

    def do_simulation_simple_tree_dynamic(self, modified=False):
        # Run simulation for the number of slots
        for self.slot_no in self.slot_array:
            # Generate a packet according to poisson distribution
            self.packets_gen = np.random.poisson(self.sim_param.lmbda)
            # Add the number of packets to the active packet array
            packetlist.add_packets(self)
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.simpletree.oneslotprocess(self, modified=modified)
            # Update the metrics in sim_state depending on the result
            self.sim_state.update_metrics(self)
        # Update the results
        self.sim_result.get_result(self)

    def do_simulation_simple_tree_static(self, collided_packets, modified=False):
        # Load active array with the collided packets
        self.packets_gen = collided_packets
        packetlist.add_packets(self)
        self.slot_no = 0
        # Run the simulation as long as all packets are processed
        while len(self.active_array) != 0:
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.simpletree.oneslotprocess(self, modified=modified)
            # Update the simstate metric according to the result of the simulation
            self.sim_state.update_metrics(self)
            # Increment the slot
            self.slot_no += 1
        # total arrivals is just equal to collided packets and we just add it here
        self.sim_state.total_arrivals = collided_packets
        # Update the results
        self.sim_result.get_result(self)

