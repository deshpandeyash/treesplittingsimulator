import numpy as np


class SimResult(object):

    def __init__(self):
        self.throughput = 0
        self.mean_packet_delay = 0
        self.max_packet_delay = 0
        self.mean_no_tx = 0
        self.max_no_tx = 0
        self.succ_rate = 0
        self.no_trees = 0
        self.idle_rate = 0
        self.collision_rate = 0
        self.mean_tree_depth = 0
        self.mean_tree_length = 0
        self.delta_cri = 0
        self.magic_throughput = 0
        self.skipped_slots = 0

    def reset(self):
        self.throughput = 0
        self.mean_packet_delay = 0
        self.max_packet_delay = 0
        self.mean_no_tx = 0
        self.max_no_tx = 0
        self.succ_rate = 0
        self.no_trees = 0
        self.idle_rate = 0
        self.collision_rate = 0
        self.mean_tree_depth = 0
        self.mean_tree_length = 0
        self.delta_cri = 0
        self.magic_throughput = 0
        self.skipped_slots = 0

    def get_result(self, sim):
        # Throughput is the number of successful packets divided by the total number of slots, used for single tree
        self.throughput = np.mean(sim.sim_state.throughput_array)
        # Idle rate
        self.idle_rate = np.mean(sim.sim_state.idle_array)
        # Collision Rate
        self.collision_rate = np.mean(sim.sim_state.collision_array)
        # Mean of the delays of all successful packets
        self.mean_packet_delay = np.mean(sim.sim_state.delay_stat_array)
        # Max of the delay
        self.max_packet_delay = max(sim.sim_state.delay_stat_array)
        # Mean no of retransmissions of all successful packets
        self.mean_no_tx = np.mean(sim.sim_state.tx_stat_array)
        # Max of all the retransmissions of all successful packets
        self.max_no_tx = max(sim.sim_state.tx_stat_array)
        # Total arrivals/total succeses
        self.succ_rate = sum(sim.sim_state.successes_array) / sum(sim.sim_state.arrival_stat_array)
        # Total no of trees resolved
        self.no_trees = len(sim.sim_state.successes_array)
        # Average tree depth is the mean of the tree depth array in simstate
        self.mean_tree_depth = np.mean(sim.sim_state.tree_depth_array)
        # Average tree length
        self.mean_tree_length = np.mean(sim.sim_state.tree_length_array)
        # Delta CRI is the difference between the CRI of the last and second last tree
        if len(sim.sim_state.tree_length_array) > 5:
            self.delta_cri = sim.sim_state.tree_length_array[-3] - sim.sim_state.tree_length_array[-4]
        # To show the error in d > 2 in SICTA
        self.magic_throughput = np.mean(sim.sim_state.magic_throughput)
        # To see the 'gain' from skipped slots, its the difference between the normal tree and Ghost Tree
        self.skipped_slots = np.mean(sim.sim_state.skipped_slots)
