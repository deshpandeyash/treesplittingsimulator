class SimState(object):

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

    def reset(self):
        self.delay_stat_array = []
        self.arrival_stat_array = []
        self.tx_stat_array = []
        self.successes_array = []
        self.collision_array = []
        self.inti_collision_array = []
        self.idle_array = []
        self.slot_len_array = []

    def update_metrics(self, sim):
        self.successes_array.append(sim.tree_state.total_successes)
        self.collision_array.append(sim.tree_state.total_collisions)
        self.inti_collision_array.append(sim.tree_state.init_collided)
        self.idle_array.append(sim.tree_state.total_idles)
        self.slot_len_array.append(sim.slot_no - sim.tree_state.first_slot)





