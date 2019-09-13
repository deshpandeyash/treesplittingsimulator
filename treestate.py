import packetlist


class TreeState(object):

    def __init__(self, sim):
        self.first_slot = sim.slot_no
        self.init_collided = len(sim.active_array)
        self.total_collisions = 0
        self.total_idles = 0
        self.prev_result = 0
        self.last_slot = 0

    def reset(self, sim):
        self.first_slot = sim.slot_no
        self.init_collided = len(sim.active_array)
        self.total_collisions = 0
        self.total_idles = 0
        self.prev_result = 0
        self.last_slot = 0

    def update_metrics(self, sim):
        # Add the number of packets to statistical array for diagnosis
        sim.sim_state.arrival_stat_array.append(sim.packets_gen)
        # Keep track of total arrivals
        sim.sim_state.total_arrivals += sim.packets_gen
        if sim.result == 1:
            go_on = True
            while go_on:
                if sim.active_array[0].packet_count < 0:
                    # Update the total successes
                    sim.sim_state.total_successes += 1
                    # remove the packet from active array
                    successful_pack = packetlist.remove_successful_packet(sim)
                    # Load the features of the successfully transmitted packet for statistics
                    sim.sim_state.delay_stat_array.append(successful_pack.life_time)
                    sim.sim_state.tx_stat_array.append(successful_pack.transmissions)
                    if len(sim.active_array) == 0:
                        go_on = False
                else:
                    go_on = False
        # If an Idle slot
        if sim.result == 0:
            # Update parameters
            sim.sim_state.total_idles += 1
        # If a collision
        if sim.result == 2:
            # Update parameters
            sim.sim_state.total_collisions += 1

