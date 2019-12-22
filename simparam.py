import numpy as np


class SimParam(object):

    """
    Contains all important simulation parameters
    """

    def __init__(self, setting):

        # current buffer spaces and minimal buffer spaces
        self.lmbda = 0.34

        # set seed for random number generation

        # The branching split i,e Q
        self.SPLIT = int(setting.firstwindow.test_values[0])
        self.biased_split = setting.firstwindow.test_values[2]
        # set branching probability for binary split
        self.branchprob = float(setting.firstwindow.test_values[3])

        # Set branching probability for a split
        self.branch_biased = np.full(self.SPLIT, (1 - self.branchprob)/(self.SPLIT - 1))
        self.branch_biased[0] = self.branchprob

        # The number of packets that can be resolved in a multipacekt reception system in one slot.
        self.K = int(setting.firstwindow.test_values[1])


        # The type of Resolution Algorithm
        self.modified = setting.firstwindow.test_values[4]
        self.unisplit = setting.firstwindow.test_values[5]
        self.sic = setting.firstwindow.test_values[6]

