import numpy as np


class SimParam(object):

    """
    Contains all important simulation parameters
    """

    def __init__(self):

        # current buffer spaces and minimal buffer spaces
        self.lmbda = 0.34

        # number of slots to simulate
        self.SIMTIME = 10000
        # set seed for random number generation
        self.seed = 21412

        # The branching split i,e Q
        self.SPLIT = 9
        self.biased_split = False
        # set branching probability for binary split
        self.branchprob = 0.5

        # Set branching probability for a split
        self.branch_biased = np.full(self.SPLIT, (1 - self.branchprob)/(self.SPLIT - 1))
        self.branch_biased[0] = self.branchprob

        # The number of packets that can be resolved in a multipacekt reception system in one slot.
        self.K = 2

        # No if runs in simstudy
        self.RUNS = 100

        # The type of Resolution Algorithm
        self.modified = False
        self.unisplit = False
        self.sic = True

        # The start, stop and step size of the arrival rate when we sweep through arrival rate
        self.start = 0.20
        self.stop = 0.60
        self.step = 0.05

    def print_sim_config(self):
        """
        Print a basic system configuration string.
        """
        print("simulaiton Parameters are: ")
        print("Arrival Rate, Lambda = " + str(self.lmbda))
        print("No of runs = " + str(self.SIMTIME))
        print("Random Number seed = " + str(self.seed))
        print("Number of runs = " + str(self.RUNS))
