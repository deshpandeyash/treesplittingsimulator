class BranchNode(object):
    def __init__(self):
        self.branch_array = []
        self.branch_status = ''

    def reset(self):
        self.branch_array = []
        self.branch_status = ''

    def split(self, Q):
        self.branch_status = self.branch_status + str(Q - 1)

    def next_leaf(self):
        while len(self.branch_status) > 0 and self.branch_status[-1] == '0':
            self.branch_status = self.branch_status[:-1]
        if len(self.branch_status) > 0:
            last_branch = self.branch_status[-1]
            self.branch_status = self.branch_status[:-1]
            self.branch_status = self.branch_status + str(int(last_branch) - 1)

    def update_array(self):
        self.branch_array.append(self.branch_status)
