class BranchNode(object):
    """
    This class keeps the status of the tree, 0 is the left most and Q-1 is the right most branch.
    Currently the easiest method seems to be to keep it in a string. This process is not iterative right now.

    """
    def __init__(self):
        # Keeps the movement of the tree in array
        self.branch_array = []
        # Keeps the current node you are on
        self.branch_status = ''

    def reset(self):
        self.branch_array = []
        self.branch_status = ''

    def split(self, Q):
        # A split will split the node to Q branches,  the branch to the rightmost ( Q-1 )th branch
        self.branch_status = self.branch_status + str(Q - 1)

    def next_leaf(self):
        """
        For an IDLE or success, we find the next left slot
        """
        # of the length is greater than 0 and we are on the left most branch,
        while len(self.branch_status) > 0 and self.branch_status[-1] == '0':
            # We move one node back
            self.branch_status = self.branch_status[:-1]
        # If the length is still greater than 0
        if len(self.branch_status) > 0:
            # We decrement the last branch.
            last_branch = self.branch_status[-1]
            self.branch_status = self.branch_status[:-1]
            self.branch_status = self.branch_status + str(int(last_branch) - 1)

    def update_array(self):
        # Update the array to keep track of the tree
        self.branch_array.append(self.branch_status)

    def update_leaf(self, sim):
        if sim.result == 1:
            # If SIC is used
            if sim.sim_param.sic:
                if sim.slot.resolved_packets > 1:
                    for _ in range(sim.slot.resolved_packets - 1):
                        self.next_leaf()
                    self.split(sim.sim_param.SPLIT)
                else:
                    self.next_leaf()
                    self.split(sim.sim_param.SPLIT)
            # If not SIC, only one success is registered, so we find the next node
            else:
                self.next_leaf()
        elif sim.result == 0:
            # On an idle, we find the next leaf
            self.next_leaf()
            # If its a definite collision, we also update the next leaf as if it was a collision
            if sim.slot.def_collision or sim.sim_param.sic:
                self.split(sim.sim_param.SPLIT)
        elif sim.result == 2:
            # On a collision split the tree
            self.split(sim.sim_param.SPLIT)
        self.update_array()
