import packetlist


class TreeSlot(object):

    def __init__(self):
        self.no_collided_packets = 0
        self.no_active_packets = 0
        self.no_waiting_packets = 0
        self.resolved_packets = 0
        self.collided_array = []
        self.tx_packet_array = []
        self.packetID = []
        self.result_array = []
        self.def_collision = False

    def oneslotprocess(self, sim):
        """
        this simulates the process in a slot, the array of active packets is analyzed and then
        we transmit the packets which have count 0, and then wait for the feedback and update the count in the packets
        accordingly
        :param sim: the simulation parameters
        :param unisplit: if true then perform a uniform split
        :param modified: if true the simulator will run the modified tree where we eliminate a deterministic collision

        """
        # this parameter is changed to the result of the transmission feedback
        sim.result = 0
        # Sort the array in ascending order
        packetlist.sort_packet_array(sim)
        # Convert the array of Packet objects to just a list for easier and faster operation at transmitter
        test_array = packetlist.extract_packet_id(sim.active_array)
        count_array = packetlist.extract_packet_count(sim)
        self.tx_packet_array = packetlist.extract_tx_packets(sim)
        # Find out the packet count attributes for further statistics
        self.no_active_packets = len(sim.active_array)
        self.no_collided_packets = len(self.tx_packet_array)
        self.no_waiting_packets = self.no_active_packets - self.no_collided_packets
        # Update the number of transmissions in each packet
        packetlist.update_transmissions(sim)
        # Get the feedback form the receiver
        feedback, self.resolved_packets = self.rxprocess(sim.sim_param.sic, sim.sim_param.K)
        # If Success
        if feedback == 1:
            # On a success, all other packets reduce their count
            packetlist.dec_packet_count(sim, self.resolved_packets)
            # If SIC process is used, then
            if sim.sim_param.sic:
                # We increment the count of the uncollided packets
                packetlist.inc_uncollided_packet_count(sim, 1)
                # And split the packets which might collide in the next slot
                packetlist.split_uncollided_packet_count(sim)
                # Here we update the node of the of the tree according to the result,
                if sim.slot.resolved_packets > 1:
                    for _ in range(sim.slot.resolved_packets - 1):
                        sim.branch_node.next_leaf()
                    sim.branch_node.split(sim.sim_param.SPLIT)
                else:
                    sim.branch_node.next_leaf()
                    sim.branch_node.split(sim.sim_param.SPLIT)
            # If not SIC, only one success is registered, so we find the next node
            else:
                sim.branch_node.next_leaf()
            sim.result = feedback
        # If Idle
        elif feedback == 0:
            # On an idle, we find the next leaf
            sim.branch_node.next_leaf()
            # To identify if the next slot after this idle slot is a definite collision, Modified tree Tree
            self.def_collision = False
            # If modified anf the Simple Tree Result Array has enough elements
            if sim.sim_param.modified and len(sim.tree_state.ST_result_array) >= (sim.sim_param.SPLIT - 1):
                # If the Q-1th result was a collision
                if sim.tree_state.ST_result_array[-(sim.sim_param.SPLIT-1)] == 2:
                    self.def_collision = True
                # And subsequent slots were not idle, then it NOT a definite collision, so we set the flag down again.
                for k in range(1, sim.sim_param.SPLIT-1):
                    if sim.tree_state.ST_result_array[-k] != 0:
                        self.def_collision = False
            # If the modified tree algorithm is used, and we have a definite collision
            if self.def_collision or sim.sim_param.sic:
                # increment the count for uncollided packets
                packetlist.inc_uncolliding_packet_count(sim, sim.sim_param.SPLIT - 2)
                # Update the counts on the collided packets according to a binary split
                packetlist.split_colliding_packet_count(sim)
                # Then split the tree
                sim.branch_node.split(sim.sim_param.SPLIT)
            else:
                # if modified tree algorithm is not used,  On an idle slot, all packets reduce their count by 1
                packetlist.dec_packet_count(sim, 1)
            sim.result = feedback
        # If Collision
        elif feedback == 2:
            # increment the count for uncollided packets
            packetlist.inc_uncollided_packet_count(sim, sim.sim_param.SPLIT - 1)
            # If unisplit and if its the first collision
            if sim.sim_param.unisplit and sim.tree_state.total_collisions == 0:
                packetlist.unisplit_uncollided_packet_count(sim)
                # Split the tree with no of collided packets
                sim.branch_node.split(self.no_collided_packets)
            else:
                # Update the counts on the collided packets according to a Q-ary split
                packetlist.split_uncollided_packet_count(sim)
                # On a collision split the tree
                sim.branch_node.split(sim.sim_param.SPLIT)
            sim.result = feedback
        # This is an error and means that the RX process did not change the feedback
        elif feedback == 9:
            print("Rx Process did not change give a Feedback")
        sim.branch_node.update_array()

    def rxprocess(self, sic, K):
        """
        depending on the active packet array length and the count in each of its packets, this process decides whether
        there was in idle slot, collision or success after which it provides feedback,

        :param
        :return: feedback , 0 = Idle; 1 = Success; 2 = collision; 9 = Error
        """
        # This parameter is initialized to a 9, to make sure it is changed by the process. i.e the feedback is one of
        # the expected values
        feedback = 9
        resolved_packets = 0
        # If the length of the array is 0 then there are no active packets, and no transmissions hence, IDLE
        if len(self.tx_packet_array) == 0:
            feedback = 0
        # If array has just one element and it is 0 then its a success
        elif len(self.tx_packet_array) <= K:
            feedback = 1
            resolved_packets = 1
            if sic:
                resolved_packets += self.sic_process(K)
        elif len(self.tx_packet_array) > K:
            feedback = 2
            if sic:
                # Save the collision packet IDs
                self.collided_array.append(packetlist.extract_packet_id(self.tx_packet_array))
        # If anything else occurs, print immediately as its not expected.
        else:
            print("Error, unexpected array")
        return feedback, resolved_packets

    def sic_process(self, K):
        # The single packet that is decoded, we take its ID
        single_packet = packetlist.extract_packet_id(self.tx_packet_array)
        # Append this ID to the array of already Decoded IDs
        self.packetID.extend(single_packet)
        sic_resolved_packets = 0
        go_on = True
        # While we can succesively Decode the packets from previous collisons
        while go_on and len(self.collided_array) > 0:
            # Load the last collison
            last_coll = self.collided_array[-1]
            # Remove all the pacet IDS that have been resolved
            resolved_array = [x for x in last_coll if x not in self.packetID]
            # If no packet remains, it means its a left IDLE slot
            if len(resolved_array) == 0:
                # Delete this collision
                del self.collided_array[-1]
                # Increment the feedback
                sic_resolved_packets += 1
            # If only one packet remains, this can be resolved too
            elif len(resolved_array) <= K:
                # Delete this collision
                del self.collided_array[-1]
                # Add the resolved packet to the packet IDS tht have already been resolved
                self.packetID.extend(resolved_array)
                sic_resolved_packets += 1
            # This collision cannot be resolved
            else:
                # We still remove only the resolved packets from the last collision, and stop the SIC process
                del self.collided_array[-1]
                self.collided_array.append(resolved_array)
                go_on = False
        return sic_resolved_packets
