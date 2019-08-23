class SimParam(object):

    """
    Contains all important simulation parameters
    """

    def __init__(self):

        # current buffer spaces and minimal buffer spaces
        self.lmbda = 0.36787944117

        # number of Runs
        self.runs = 10000
        # set seed for random number generation
        self.seed = 9

        # set branching probabilty
        self.branchprob = 0.5

    def print_sim_config(self):
        """
        Print a basic system configuration string.
        """
        print("simulaiton Parameters are: ")
        print("Arrival Rate, Lambda = " + str(self.lmbda))
        print("No of runs = " + str(self.runs))
        print("Random Number seed = " + str(self.seed))
