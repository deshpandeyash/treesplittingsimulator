import numpy as np


class SimParam(object):
    """
    Contains all important simulation parameters
    """

    def __init__(self, setting):

        if setting is None:

            # current buffer spaces and minimal buffer spaces
            self.lmbda = 0.34

            # set seed for random number generation

            # The branching split i,e Q
            self.SPLIT = 9
            self.biased_split = False
            if self.biased_split:
                # set branching probability for binary split
                self.branchprob = 0.5
            else:
                self.branchprob = 1 / self.SPLIT
            # Set branching probability for a split
            self.branch_biased = np.full(self.SPLIT, (1 - self.branchprob) / (self.SPLIT - 1))
            self.branch_biased[0] = self.branchprob

            # The number of packets that can be resolved in a multipacekt reception system in one slot.
            self.K = 1

            # The type of Resolution Algorithm
            self.modified = False
            self.unisplit = False
            self.sic = False
            self.combi = False
            self.combi_splits = [3, 4]
            self.combi_split_ratio = 0.33

        else:
            # current buffer spaces and minimal buffer spaces
            self.lmbda = 0.34

            # set seed for random number generation

            # The branching split i,e Q
            self.SPLIT = int(setting.firstwindow.test_values[0])
            self.biased_split = setting.firstwindow.test_values[2]
            if self.biased_split:
                # set branching probability for binary split
                self.branchprob = float(setting.firstwindow.test_values[3])
            else:
                self.branchprob = 1 / self.SPLIT
            # Set branching probability for a split
            self.branch_biased = np.full(self.SPLIT, (1 - self.branchprob) / (self.SPLIT - 1))
            self.branch_biased[0] = self.branchprob

            # The number of packets that can be resolved in a multipacekt reception system in one slot.
            self.K = int(setting.firstwindow.test_values[1])

            # The type of Resolution Algorithm
            self.modified = setting.firstwindow.test_values[4]
            self.unisplit = setting.firstwindow.test_values[5]
            self.sic = setting.firstwindow.test_values[6]

    def print_settings(self):
        print("Q = " + str(self.SPLIT))
        print("K = " + str(self.K))
        print("Branch Prob = " + str(self.branchprob))
        if self.biased_split:
            print("Using Biased Split")
        if self.modified:
            print("Modified Tree")
        if self.sic:
            print("Successive Interference Cancellataion")
        if self.unisplit:
            print("Uniform First Split")
        if not self.modified and not self.sic:
            print("Simple Tree")
