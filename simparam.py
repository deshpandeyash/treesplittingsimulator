from math import e


class SimParam(object):

    """
    Contains all important simulation parameters
    """

    def __init__(self):

        # current buffer spaces and minimal buffer spaces
        self.lmbda = 0.34           #0.375

        # number of slots to simulate
        self.SIMTIME = 100000
        # set seed for random number generation
        self.seed = 7

        # set branching probabilty
        self.branchprob = 0.5

        # No if runs in simstudy
        self.RUNS = 100

    def print_sim_config(self):
        """
        Print a basic system configuration string.
        """
        print("simulaiton Parameters are: ")
        print("Arrival Rate, Lambda = " + str(self.lmbda))
        print("No of runs = " + str(self.SIMTIME))
        print("Random Number seed = " + str(self.seed))
        print("Number of runs = " + str(self.RUNS))
