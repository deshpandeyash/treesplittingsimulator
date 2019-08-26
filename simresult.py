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

    def get_result(self, sim_state, sim_time):
        self.throughput = sim_state.total_successes / sim_time
        self.mean_packet_delay = np.mean(sim_state.delay_stat_array)
        self.max_packet_delay = max(sim_state.delay_stat_array)
        self.mean_no_tx = np.mean(sim_state.tx_stat_array)
        self.max_no_tx = max(sim_state.tx_stat_array)

