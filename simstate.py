class SimState(object):
    """
    This class has all the arrays where the results must be appended to when a particular tree is resolved.
    """

    def __init__(self):
        # Arrays to see the distribution of arrivals and packet delays
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        self.successes_array = []
        self.collision_array = []
        self.inti_collision_array = []
        self.idle_array = []
        self.slot_len_array = []
        self.throughput_array = []
        self.tree_depth_array = []

    def reset(self):
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        self.successes_array = []
        self.collision_array = []
        self.inti_collision_array = []
        self.idle_array = []
        self.slot_len_array = []
        self.throughput_array = []
        self.tree_depth_array = []

    def update_metrics(self, sim):
        success_slots = sim.tree_state.result_array.count(1)
        idle_slots = sim.tree_state.result_array.count(0)
        collision_slots = sim.tree_state.result_array.count(2)
        # Append all the parameters from tree state to the arrays in this class
        self.successes_array.append(sim.tree_state.total_successes)
        self.throughput_array.append((sim.tree_state.total_successes/(sim.slot_no - sim.tree_state.first_slot))/sim.sim_param.K)
        self.collision_array.append(collision_slots/(sim.slot_no - sim.tree_state.first_slot))
        self.idle_array.append(idle_slots/(sim.slot_no - sim.tree_state.first_slot))
        self.inti_collision_array.append(sim.tree_state.init_collided)
        self.slot_len_array.append(sim.slot_no - sim.tree_state.first_slot)
        if len(sim.branch_node.branch_array) <= 1:
            self.tree_depth_array.append(0)
        else:
            self.tree_depth_array.append(len(max(sim.branch_node.branch_array[:-1], key=len)))
        if (sim.tree_state.init_collided != sim.tree_state.total_successes) and not sim.freeaccess:
            print("Tree incomplete!")
        if not sim.sim_param.modified and not sim.sim_param.sic:
            if sim.tree_state.result_array != sim.tree_state.ST_result_array:
                print("Error Simple Tree Problem, result array not matching!")
            if sim.tree_state.number_in_slot != sim.tree_state.ST_number_in_slot:
                print("Error Simple Tree Problem, number in slot not matching!")
        if (success_slots + idle_slots + collision_slots) != sim.slot_no - sim.tree_state.first_slot:
            print("Error! Slots not Adding up!")






