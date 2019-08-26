class SimResult(object):

    def __init__(self):
        # Arrays to see the distribution of arrivals and packet delays
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        # These two keep a count of arrivals and successes
        self.total_arrivals = 0
        self.total_successes = 0

    def reset(self):
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        self.total_arrivals = 0
        self.total_successes = 0
