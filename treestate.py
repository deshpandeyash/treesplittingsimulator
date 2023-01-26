import packetlist


class TreeState(object):
    def __init__(self, sim):
        self.first_slot = sim.slot_no
        self.init_collided = len(sim.active_array)
        self.total_successes = 0
        self.last_slot = 0
        self.result_array = []
        self.k_feedback = []
        # IF it was a simple tree, this would have been a result array. Its useful when we have to look for definite
        # collisions
        self.ST_result_array = []
        self.gate_open = True
        self.number_in_slot = []
        self.ST_number_in_slot = []
        self.magic_counter = 0
        self.split_count = []

    def reset(self, sim):
        self.first_slot = sim.slot_no
        self.init_collided = len(sim.active_array)
        self.total_successes = 0
        self.result_array = []
        self.k_feedback = []
        self.ST_result_array = []
        self.last_slot = 0
        self.gate_open = True
        self.number_in_slot = []
        self.ST_number_in_slot = []
        self.magic_counter = 0
        self.split_count = []

    def update_metrics(self, sim):
        """
        Here we update the results of the ongoing tree and remove successful packets, update results
        in the simulation state according to the packets statistics

        :param sim: the simulation object instance
        """
        # Update the result of the slot in the result array
        self.result_array.append(sim.result)
        self.ST_result_array.append(sim.result)
        self.number_in_slot.append(sim.slot.no_collided_packets)
        self.ST_number_in_slot.append(sim.slot.no_collided_packets)
        self.split_count.append(sim.sim_param.SPLIT)
        self.k_feedback.append(sim.slot.resolved_packets)
        # Add the number of packets to statistical array for diagnosis
        sim.sim_state.arrival_stat_array.append(sim.packets_gen)
        if sim.result == 1:
            if sim.sim_param.sic:
                self.ST_result_array.pop()
                self.ST_number_in_slot.pop()
            if sim.slot.def_collision:
                self.ST_number_in_slot.append(sim.slot.no_in_skipped_slot)
                self.ST_result_array.append(2)
            go_on = True
            while go_on:
                # If the 0 th element of the active array is less than 0, it mans that packet is resolved, hence remove
                if sim.active_array[0].packet_count < 0:
                    # Update the total successes
                    self.total_successes += 1
                    # remove the packet from active array
                    successful_pack = packetlist.remove_successful_packet(sim)
                    # Load the features of the successfully transmitted packet for statistics
                    sim.sim_state.delay_stat_array.append(successful_pack.life_time)
                    sim.sim_state.tx_stat_array.append(successful_pack.transmissions)
                    # CHeck if the active array is resolved completely
                    if len(sim.active_array) == 0:
                        go_on = False
                # If the 0 th element is not 0 then we can continue with the next slot.
                else:
                    go_on = False
        elif sim.result == 0:
            if sim.slot.def_collision:
                # And update the simple tree result as a collision
                self.ST_result_array.append(2)
                self.ST_number_in_slot.append(sim.slot.no_in_skipped_slot)
        self.magic_counter = sim.slot.magic_counter
        if sim.sim_param.SPLIT == 2 and self.magic_counter > 0:
            print("Magic Counter error")
