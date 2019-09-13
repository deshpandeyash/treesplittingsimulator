class SimState(object):

    def __init__(self):
        # Arrays to see the distribution of arrivals and packet delays
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        # These variables keep the parameters of the simulation
        self.total_arrivals = 0
        self.total_successes = 0
        self.total_collisions = 0
        self.total_idles = 0
        self.prev_result = 0

    def reset(self):
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        self.total_arrivals = 0
        self.total_successes = 0
        self.prev_result = 0
        self.total_collisions = 0
        self.total_idles = 0






