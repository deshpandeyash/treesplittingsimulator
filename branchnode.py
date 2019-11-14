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
        self.success_branch = ''
        self.ghost_array = []

    def reset(self):
        self.branch_array = []
        self.branch_status = ''
        self.success_branch = ''
        self.ghost_array = []

    def split(self, q):
        # A split will split the node to Q branches,  the branch to the rightmost ( Q-1 )th branch
        self.branch_status = self.branch_status + str(q - 1)

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
        if self.branch_status not in self.ghost_array:
            self.ghost_array.append(self.branch_status)

    def update_ghost(self):
        self.ghost_array.append(self.branch_status)

