import numpy as np
import packetlist


class SimpleTreeSlot(object):

    def __init__(self, sim_param):
        self.sim_param = sim_param
        self.no_collided_packets = 0
        self.no_active_packets = 0
        self.no_waiting_packets = 0

    def oneslotprocess(self, sim, modified=False):
        """
        this simulates the process in a slot, the array of active packets in a slot fed to it,
        we transmit the packets which have count 0, and then wait for the feedback and update the count in the packets
        accordingly
        :param arrival_array: the array of active packets in the system
        :param printit: if printing needs to be done for diagnostics
        :return: the updated array and if this process resulted in a success
        """

        # this parameter is changed to 1 if the result from this slot is a success
        sim.result = 0
        # Sort the array in ascending order
        packetlist.sort_packet_array(sim)
        # Convert the array of Packet objects to just a list for easier and faster operation at transmitter
        packet_count_array = packetlist.extract_packet_count(sim)
        # Get the feedback form the receiver
        feedback = self.rxprocess(packet_count_array)
        # Find out the packet count attributes for further statistics
        self.no_active_packets = len(packet_count_array)
        self.no_waiting_packets = np.count_nonzero(packet_count_array)
        self.no_collided_packets = self.no_active_packets - self.no_waiting_packets
        # Update the number of transmissions in each packet
        packetlist.update_transmissions(sim)
        # If Success
        if feedback == 1:
            # On a success, all other packets reduce their count by 1
            packetlist.dec_packet_count(sim)
            sim.result = 1
        # If Idle
        elif feedback == 0:
            # On an idle slot, all packets reduce their count by 1
            packetlist.dec_packet_count(sim)
            if modified and sim.sim_state.prev_result == 2:
                # increment the count for uncollided packets
                packetlist.inc_uncollided_packet_count(sim)
                # Update the counts on the collided packets according to a binary split
                packetlist.binsplit_uncollided_packet_count(sim)
            sim.result = 0
        # If Collision
        elif feedback == 2:
            # increment the count for uncollided packets
            packetlist.inc_uncollided_packet_count(sim)
            # Update the counts on the collided packets according to a binary split
            packetlist.binsplit_uncollided_packet_count(sim)
            sim.result = 2
        # This is an error and means that the RX process did not change the feedback
        elif feedback == 9:
            print("Rx Process did not change give a Feedback")
        sim.sim_state.prev_result = sim.result

    def rxprocess(self, active_packet_array):
        """
        depending on the active packet array length and the count in each of its packets, this process decides whether there
        was in idle slot, collision or success after which it provides feedback,

        :param active_packet_array: the array that contains all the packets, this array is already sorted by the txprocess
        :param printit: if the feedback must be printed
        :return: feedback , 0 = Idle; 1 = Success; 2 = collision; 9 = Error
        """
        # This parameter is initialized to a 9, to make sure it is changed by the process. i.e the feedback is one of
        # the expected values
        feedback = 9
        # If the length of the array is 0 then there are no active packets, and no transmissions hence, IDLE
        # If the first element is not 0, it means that no one will transmit even when there are active packets, ie IDLE
        if len(active_packet_array) == 0 or active_packet_array[0] != 0:
            feedback = 0
        # If array has just one element and it is 0 then its a success
        elif len(active_packet_array) == 1 and active_packet_array[0] == 0:
            feedback = 1
        # If the first element is 0 and the second element is not 0 then, we have no collision and a success
        elif active_packet_array[0] == 0 and active_packet_array[1] != 0:
            feedback = 1
        # If the first and second element ( at least) are 0 it means we have a collision
        elif active_packet_array[0] == 0 and active_packet_array[1] == 0:
            feedback = 2
        # If anything else occurs, print immediately as its not expected.
        else:
            print("Error, unexpected array")
        return feedback
