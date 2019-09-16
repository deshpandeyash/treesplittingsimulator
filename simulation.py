import numpy as np
from simparam import SimParam
from simstate import SimState
from simresult import SimResult
from slot import TreeSlot
from treestate import TreeState
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
        self.slot = TreeSlot(self.sim_param)
        # Load the parameters for single tree resolution

        # Create an array of integers of which will contain all active nodes.
        self.active_array = []
        self.queue_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)
        self.packets_gen = 0
        self.result = 0
        self.slot_no = 0
        self.added_packets = 0
        self.tree_state = TreeState(self)

    def reset(self):
        self.sim_param = SimParam()
        self.sim_state = SimState()
        self.sim_result = SimResult()
        self.slot = TreeSlot(self.sim_param)

        self.active_array = []
        self.queue_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)
        self.packets_gen = 0
        self.result = 0
        self.slot_no = 0
        self.added_packets = 0
        self.tree_state = TreeState(self)

    def do_simulation_simple_tree_dynamic(self, modified=False, unisplit=False,sic=False):
        # Run simulation for the number of slots
        self.tree_state.reset(self)
        for self.slot_no in self.slot_array:
            # Generate a packet according to poisson distribution
            self.packets_gen = np.random.poisson(self.sim_param.lmbda)
            # Add the number of packets to the active packet array
            packetlist.add_packets_to_tree(self)
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.slot.oneslotprocess(self, modified=modified, unisplit=unisplit, sic=sic)
            # Update the metrics in sim_state depending on the result
            self.tree_state.update_metrics(self)
        # Update the results
        self.sim_state.update_metrics(self)
        self.sim_result.get_result(self)

    def do_simulation_simple_tree_static(self, collided_packets, modified=False, unisplit=False,sic=False,multipacket=True):
        # Load active array with the collided packets
        self.packets_gen = collided_packets
        packetlist.add_packets_to_tree(self)
        self.tree_state.reset(self)
        # Run the simulation as long as all packets are processed
        while len(self.active_array) != 0:
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.slot.oneslotprocess(self, modified=modified,unisplit=unisplit,sic=sic,multipacket=multipacket)
            # Update the simstate metric according to the result of the simulation
            self.tree_state.update_metrics(self)
            # Increment the slot
            self.slot_no += 1
        # update the metrics from a tree to the simulation state
        self.sim_state.update_metrics(self)
        # Update the results
        self.sim_result.get_result(self)

    def do_simulation_gated_access(self, modified=False, unisplit=False, sic=False):
        # Run simulation for the number of slots
        while len(self.active_array) > 0 or self.slot_no < self.sim_param.SIMTIME:
            self.slot_no += 1
            # Generate a packet according to poisson distribution
            self.packets_gen = np.random.poisson(self.sim_param.lmbda)
            # Add the packet to the queue
            if self.slot_no < self.sim_param.SIMTIME:
                packetlist.add_packets_to_queue(self)
            # if the active array is empty i.e the tree is resolved
            if len(self.active_array) == 0:
                # Update the Sim_state class for the previous tree
                self.sim_state.update_metrics(self)
                # Transfer the queue to the active array
                self.active_array = self.queue_array
                # Clear the queue
                self.queue_array = []
                # Reset all the parameters as we start a new tree
                self.tree_state.reset(self)
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.slot.oneslotprocess(self, modified=modified, unisplit=unisplit, sic=sic)
            # Update the metrics in sim_state depending on the result
            self.tree_state.update_metrics(self)
        # Update the results
        self.sim_result.get_result(self)
