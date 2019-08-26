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
        self.modfiedtree = ModifiedTreeSlot(self.sim_param)
        # Create an array of integers of which will contain all active nodes.
        self.active_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)

    def reset(self):
        self.sim_param = SimParam()
        self.sim_state = SimState()
        self.sim_result = SimResult()
        self.simpletree = SimpleTreeSlot(self.sim_param)
        self.modfiedtree = ModifiedTreeSlot(self.sim_param)
        self.active_array = []
        self.slot_array = np.arange(0, self.sim_param.SIMTIME)

    def do_simulation_simple_tree_dynamic(self):
        # Run simulation for the number of slots
        for slot_no in self.slot_array:
            # Generate a packet according to poisson distribution
            packets_gen = np.random.poisson(self.sim_param.lmbda)
            # Add the number of packets to the active packet array
            self.active_array = packetlist.add_packets(slot_no, self.sim_state.total_arrivals, packets_gen,
                                                                                                     self.active_array)
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.active_array, result = self.simpletree.oneslotprocess(self.active_array, printit=False)
            # Update the metrics in sim_state depending on the result
            self.active_array = self.sim_state.update_metrics(self.active_array, packets_gen, slot_no, result)
        # Update the results
        self.sim_result.get_result(self.sim_state, self.sim_param.SIMTIME)

    def do_simulation_simple_tree_static(self, collided_packets):
        # Load active array with the collided packets
        self.active_array = packetlist.add_packets(0, 0, collided_packets, self.active_array)
        slot_no = 0
        # Run the simulation as long as all packets are processed
        while len(self.active_array) != 0:
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.active_array, result = self.simpletree.oneslotprocess(self.active_array, printit=False)
            # Update the simstate metric according to the result of the simulation
            self.active_array = self.sim_state.update_metrics(self.active_array, 0, slot_no, result)
            # Increment the slot
            slot_no += 1
        # total arrivals is just equal to collided packets and we just add it here
        self.sim_state.total_arrivals = collided_packets
        # Update the results
        self.sim_result.get_result(self.sim_state, slot_no)

    def do_simulation_modified_tree_static(self, collided_packets):
        # Load active array with the collided packets
        self.active_array = packetlist.add_packets(0, 0, collided_packets, self.active_array)
        slot_no = 0
        collision = False
        # Run the simulation as long as all packets are processed
        while len(self.active_array) != 0:
            # Simulate the processes that would happen in the tx and rx in one slot, update the active array accordingly
            self.active_array, result = self.modfiedtree.oneslotprocess(self.active_array, collision, printit=False)
            if result == 2:
                collision = True
            else:
                collision = False
            # Update the simstate metric according to the result of the simulation
            self.active_array = self.sim_state.update_metrics(self.active_array, 0, slot_no, result)
            # Increment the slot
            slot_no += 1
        # total arrivals is just equal to collided packets and we just add it here
        self.sim_state.total_arrivals = collided_packets
        # Update the results
        self.sim_result.get_result(self.sim_state, slot_no)
