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
        self.throughput = sim.sim_state.total_successes / sim.slot_no
        self.mean_packet_delay = np.mean(sim.sim_state.delay_stat_array)
        self.max_packet_delay = max(sim.sim_state.delay_stat_array)
        self.mean_no_tx = np.mean(sim.sim_state.tx_stat_array)
        self.max_no_tx = max(sim.sim_state.tx_stat_array)

