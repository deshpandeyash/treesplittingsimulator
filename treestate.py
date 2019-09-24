import packetlist


class TreeState(object):

    def __init__(self, sim):
        self.first_slot = sim.slot_no
        self.init_collided = len(sim.active_array)
        self.total_successes = 0
        self.last_slot = 0
        self.result_array = []
        self.branch_array = []
        self.branch_status = ''

    def reset(self, sim):
        self.first_slot = sim.slot_no
        self.init_collided = len(sim.active_array)
        self.total_successes = 0
        self.result_array = []
        self.last_slot = 0
        self.branch_array = []
        self.branch_status = ''

    def update_metrics(self, sim):
        """
        Here we update the results of a the ongoing tree and remove successful packets, update results
        in the simulation state according to the the packets statistics

        :param sim: the simulation object instance
        """
        # Update the result of the slot in the result array
        self.result_array.append(sim.result)
        # Add the number of packets to statistical array for diagnosis
        sim.sim_state.arrival_stat_array.append(sim.packets_gen)
        if sim.result == 1:
            self.branch_status = self.branch_status + str(sim.sim_param.SPLIT - 1)
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
                    if len(sim.active_array) == 0:
                        go_on = False
                else:
                    go_on = False
        else:
            if self.branch_status[-1] == '0':
                self.branch_status = self.branch_status[:-1]
            last_branch = self.branch_status[-1]
            self.branch_status = self.branch_status[:-1]
            self.branch_status = self.branch_status + str(int(last_branch) - 1)







