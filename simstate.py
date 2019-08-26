import packetlist


class SimState(object):

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

    def update_metrics(self, active_array, packets_gen, slot_no, result):
        # Add the number of packets to statistical array for diagnosis
        self.arrival_stat_array.append(packets_gen)
        # Keep track of total arrivals
        self.total_arrivals += packets_gen
        if result == 1:
            # Update the total successes
            self.total_successes += 1
            # remove the packet from active array
            active_array, successful_pack = packetlist.remove_successful_packet(active_array, slot_no)
            # Load the features of the successfully transmitted packet for statistics
            self.delay_stat_array.append(successful_pack.life_time)
            self.tx_stat_array.append(successful_pack.transmissions)
        return active_array

