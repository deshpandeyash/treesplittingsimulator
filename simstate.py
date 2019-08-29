import packetlist


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

    def update_metrics(self, sim):
        # Add the number of packets to statistical array for diagnosis
        self.arrival_stat_array.append(sim.packets_gen)
        # Keep track of total arrivals
        self.total_arrivals += sim.packets_gen
        # If a success
        if sim.result == 1:
            for _ in range(sim.slot.resolved_packets):
                # Update the total successes
                self.total_successes += 1
                # remove the packet from active array
                successful_pack = packetlist.remove_successful_packet(sim)
                # Load the features of the successfully transmitted packet for statistics
                self.delay_stat_array.append(successful_pack.life_time)
                self.tx_stat_array.append(successful_pack.transmissions)
        # If an Idle slot
        if sim.result == 0:
            # Update parameters
            self.total_idles += 1
        # If a collision
        if sim.result == 2:
            # Update parameters
            self.total_collisions += 1



