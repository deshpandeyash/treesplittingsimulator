import numpy as np


class SimResult(object):

    def __init__(self):
        self.throughput = 0
        self.mean_packet_delay = 0
        self.max_packet_delay = 0
        self.mean_no_tx = 0
        self.max_no_tx = 0

    def reset(self):
        self.throughput = 0
        self.mean_packet_delay = 0
        self.max_packet_delay = 0
        self.mean_no_tx = 0
        self.max_no_tx = 0

    def get_result(self, sim):
        # Throughput is the number of successful packets divided by the total number of slots
        self.throughput = sim.sim_state.total_successes / sim.slot_no
        # Mean of the delays of all successful packets
        self.mean_packet_delay = np.mean(sim.sim_state.delay_stat_array)
        # Max of the delay
        self.max_packet_delay = max(sim.sim_state.delay_stat_array)
        # Mean no of retransmissions of all successful packets
        self.mean_no_tx = np.mean(sim.sim_state.tx_stat_array)
        # Max of all the retransmissions of all successful packets
        self.max_no_tx = max(sim.sim_state.tx_stat_array)

