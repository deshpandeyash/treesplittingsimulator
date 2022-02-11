import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot
from scipy.stats import skew
import graphdisplay
from make_stat import mean_confidence_interval, make_histogram_cont, make_histogram_discrete, create_ideal_by_regression
from make_stat import make_multiplot, plot_conf_interval
from simsetting import SimSetting
from simulation import Simulation
from theoretical_plots import TheoreticalPlots
import tikzplotlib
from file_helper import make_result_txt, make_result_folder, close_txt_file, still_print
import theorstudy
import math


def simulate_tree_branching(sim, setting, date_time_folder, txt_context):
    """
    To get the vizualization of 1 tree for the given settings and number of users as defined by simsettings and simparam
    also prints the obtained throughput, tree progression, result progression and tree depth
    """

    # Reset the simuations with the settings
    sim.reset(setting)
    # Make a simulation with the given users, and Tree Parameters
    sim.do_simulation_simple_tree_static(setting.vizwindow.users)
    print("Results(Feedback) were: ")
    # Print The result array.. (Basically the feedback from the Receiver)
    print(sim.tree_state.result_array)
    print("Tree Progression was: ")
    print(sim.branch_node.branch_array[:-1])
    print("Throughput is = " + str(sim.sim_result.throughput / sim.sim_param.K))

    print("Theoretically it should be = " + str.format('{0:.15f}', TheoreticalPlots().qarysic(setting.vizwindow.users,
                                                                                              sim.sim_param)))
    print("Magic Throughput " + str(sim.sim_result.magic_throughput))
    print("The Depth of the tree is: " + str(sim.sim_result.mean_tree_depth))
    # Use Graphviz to Render the Tree
    graphdisplay.displaygraph(sim, date_time_folder)


def simulate_simple_tree_satic_multiple_runs_over_p(sim, setting, date_time_folder, txt_context):
    start = time.time()
    p_range = np.arange(0.28, 0.40, 0.01)
    throughput = []
    throughput_mean = []
    for p in p_range:
        tpt = []
        for _ in range(100):
            sim.reset(setting)
            sim.sim_param.branchprob = p
            # Set branching probability for a split
            sim.sim_param.branch_biased = np.full(sim.sim_param.SPLIT, (1 - sim.sim_param.branchprob) / (sim.sim_param.SPLIT - 1))
            sim.sim_param.branch_biased[0] = sim.sim_param.branchprob
            users = 100
            sim.do_simulation_simple_tree_static(users)
            tpt.append(sim.sim_result.throughput / sim.sim_param.K)
        throughput.append(tpt)
        throughput_mean.append(np.mean(tpt))
    pyplot.boxplot(throughput)
    plt.show()
    plt.plot(p_range, throughput_mean)
    plt.show()
    print(F"Time taken is {time.time()-start} seconds")



def simulate_simple_tree_static_multiple_runs(sim, setting, date_time_folder, txt_context):
    """
    Does a a number of runs with the same number of users, plots the distribution of throughput and prints out the
    theoretical throughput, plots to see if the results are within confidence intervals
    """

    print_result = True
    start = time.time()
    # Append tuples of the intervals after each run
    conf_intervals = []
    # Alpha for the confidence interval plot
    alpha = 0.95
    # Number in slot is used as a Slot Degree Distribution Counter
    number_in_slot = []
    # The number of re-transmissions that a particular node had to do
    tx_stat_array = []
    # Throughput array
    throughput = []
    # Magic Throughput for the Giannakis mistake
    magic_throughput = []
    # Skipped Slots
    skipped_slots = []
    # Tree Length
    tree_length = []
    for _ in range(setting.statictreewindow.runs):
        # Reset the simulation
        sim.reset(setting)
        # Load users
        users = setting.statictreewindow.users
        # Make one Tree Simulation
        sim.do_simulation_simple_tree_static(users)
        # Append the throughput to the array
        throughput.append(sim.sim_result.throughput / sim.sim_param.K)
        # Degree Distribution Counter, we do not include the degree of the first collision
        number_in_slot += sim.tree_state.number_in_slot[1:]
        # Append the Number of retransmissions, directly
        tx_stat_array += sim.sim_state.tx_stat_array
        # Magic throughput until Giannakis Equation is solved
        magic_throughput.append(sim.sim_result.magic_throughput / sim.sim_param.K)
        # To check the number of skipped slots
        skipped_slots.append(sim.sim_result.skipped_slots)
        # To check the length of the tree
        tree_length.append(sim.sim_result.mean_tree_length)
        # Sanity Check to see if users are the same as successes, (Whether Tree is complete)
        if sim.tree_state.total_successes != users:
            print("Error total successes not equal to total users")
    # Get the mean and intervals for the throughput array
    conf_mean, conf_min, conf_max = mean_confidence_interval(throughput, alpha)
    # The confidence intervals for this run are appended as a tuples
    conf_intervals.append((conf_min, conf_max))
    # We just get the theoretical throughput in 'Steady State' for users. For Large K this is not accurate
    theoretical_throughput = TheoreticalPlots().qarysic(setting.statictreewindow.users, sim.sim_param)
    # Create F Strings for print
    std_dev = F"Standard Deviation = {np.std(np.asarray(throughput))}"
    skewness = F"Skewness in throughput distribution = {skew(np.asarray(throughput))}"
    mean_throughput = F"Mean Throughput = {np.mean(throughput)}"
    theoretical_mean_throughput = F"Theoretical Throughput = {theoretical_throughput:.6f}"
    left_skipped_throughput = F"Left Skipped Throughput = {np.mean(magic_throughput)}"
    total_skipped_slots = F"Mean Total Skipped Slots per run = {np.mean(skipped_slots)} "
    total_tree_length = F"Mean Tree Length per run = {np.mean(tree_length)}"
    if print_result:
        print(std_dev)
        print(skewness)
        print(mean_throughput)
        print(theoretical_mean_throughput)
        print(total_tree_length)
        print(total_skipped_slots)
        if sim.sim_param.sic and sim.sim_param.SPLIT > 2:
            print("This is the problem with the Giannakis Equation for d > 2 but, ")
            print(left_skipped_throughput)
    # Plots start here
    # First the throughput histogram
    make_histogram_cont(throughput, sim, xlabel='Throughput', conf_ints=(conf_min, conf_max),
                        theoretical_mean=theoretical_throughput, save_fig=True, folder=date_time_folder)
    # Then the Packet in a slot distribuiton
    number_in_slot = np.asarray(number_in_slot) / sim.sim_param.K
    make_histogram_discrete(number_in_slot, sim, setting, xlabel='Packets in a Slot', save_fig=False,
                            folder=date_time_folder)
    # Then the retransmission Distribution
    make_histogram_discrete(tx_stat_array, sim, setting, xlabel='Transmissions per Packet', save_fig=False,
                            folder=date_time_folder)
    end = time.time()
    print("Time for simulation: " + str(end - start))
    pyplot.show()


def simulate_users(sim, setting, date_time_folder, txt_context):
    """
    Sweeps through number of users, taking an average over the runs defined in simsetting for each run.
    At the same time plots the theoretical results.
    :param n_stop: Till the number of users we wish to plot.
    """
    start = time.time()
    # The array across users
    throughput_array = []
    # The theoretical (ideal) throughput
    theoretical_out_array = []
    # Magic Throughput until the Giannakis problem is solved
    magic_throughput_array = []
    # Create USer Array, starting from K + 1 till the stop value inputted from the GUI
    user_array = np.arange(sim.sim_param.K + 1, setting.usersweep.n_stop)
    for n in user_array:
        # Array to take mean from
        throughput = []
        magic = []
        for _ in range(setting.usersweep.runs):
            # Reset the simulation
            sim.reset(setting)
            # Make simulation and append throughputs
            sim.do_simulation_simple_tree_static(n)
            throughput.append(sim.sim_result.throughput / sim.sim_param.K)
            magic.append(sim.sim_result.magic_throughput / sim.sim_param.K)
        # Append the mean to the actual plot array
        throughput_array.append(np.mean(throughput))
        magic_throughput_array.append(np.mean(magic))
        theoretical_out_array.append(TheoreticalPlots().qarysic(n, sim.sim_param))
    # Get the theoretical Value
    theoretical_out = TheoreticalPlots().qarysic(setting.usersweep.n_stop, sim.sim_param)
    pyplot.plot(user_array, throughput_array, 'b-', label='simulation')
    pyplot.plot(user_array, theoretical_out_array, 'r', label='theoretical')
    print(F"Max Theoretical throughput is {max(theoretical_out_array):.6f}"
          F" at Users {user_array[theoretical_out_array.index(max(theoretical_out_array))]}")
    print(F"Steady State Theoretical Value =   {theoretical_out:.6f}")
    if sim.sim_param.sic and sim.sim_param.SPLIT > 2:
        pyplot.plot(user_array, magic_throughput_array, 'g', label='Right Skipped Simulation')
    pyplot.xlabel("N Users")
    pyplot.ylabel("Throughput")
    pyplot.legend()
    figname = date_time_folder + F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}UserSweep"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print(F"Time for simulation: {end - start} Seconds")
    pyplot.show()


def simulate_simple_tree_dynamic_multiple_runs(sim, setting, date_time_folder, txt_context):
    """
    FREE ACCESS SIMULATION
    Sweep through different arrival rate, take average through no of runs. Plot delay, success rate vs arrival rate.

    """
    start = time.time()
    rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step,
                           setting.dynamictest.step)
    succ_rate = []
    delay = []
    for p in rate_array:
        counter1 = []
        counter2 = []
        for _ in range(setting.dynamictest.runs):
            sim.reset(setting)
            sim.sim_param.lmbda = p
            sim.do_simulation_simple_tree_dynamic()
            counter1.append(sim.sim_result.succ_rate)
            counter2.append(sim.sim_result.mean_packet_delay)
        succ_rate.append(np.mean(counter1))
        delay.append(np.mean(counter2))
    optimum_throughput = rate_array[delay.index(max(delay))]
    print("Optimum Throughput = " + str(optimum_throughput))
    pyplot.plot(rate_array, succ_rate, color='red')
    pyplot.xlabel('Arrival rate (packets/slot)')
    pyplot.ylabel('Success rate')
    pyplot.twinx()
    pyplot.plot(rate_array, delay, color='blue')
    pyplot.ylabel('Mean Packet Delay')
    pyplot.show()
    pyplot.grid()
    figname = date_time_folder + F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}FreeArrivalSweep"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))


def simulate_simple_tree_dynamic_multiple_runs_gated(sim, setting, date_time_folder, txt_context):
    """
    GATED ACCESS SIMULATION - plots cri length and mean packet delay should add a k sweep
    """
    start = time.time()
    rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step,
                           setting.dynamictest.step)

    delay = []
    cri_length = []
    for p in rate_array:
        delay_counter = []
        delta_length_counter = []
        for j in range(setting.dynamictest.runs):
            sim.reset(setting)
            sim.sim_param.lmbda = p * sim.sim_param.K
            sim.do_simulation_gated_access()
            delay_counter.append(sim.sim_result.mean_packet_delay)
            delta_length_counter.append(sim.sim_result.delta_cri)
        delay.append(np.mean(delay_counter))
        cri_length.append(np.mean(delta_length_counter))
    pyplot.plot(rate_array, delay)
    pyplot.xlabel('CRI')
    pyplot.ylabel('Init Collision')
    pyplot.title(F"Mean Packet Delay")
    pyplot.legend()
    pyplot.grid()
    figname = date_time_folder + F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}GatedArrivalSweep"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex', encoding='utf-8')
    pyplot.show()
    end = time.time()
    print("Time for Simulation: " + str(end - start))


def do_theoretical(sim, setting, date_time_folder, txt_context):
    """
    These Tests do not make any simulations, rather are used to show the behaviour of the theoretical equations from
    settings..
    """
    start = time.time()
    if setting.theortest.test_values[0]:
        theorstudy.compare_different_functions(sim, setting, date_time_folder)
    elif setting.theortest.test_values[1]:
        theorstudy.length_throughput_plot(sim, setting, date_time_folder)
    elif setting.theortest.test_values[2]:
        theorstudy.show_optimal_branchprob(sim, setting, date_time_folder)
    elif setting.theortest.test_values[3]:
        theorstudy.traffic_analysis(sim, setting, date_time_folder)
    end = time.time()
    print(F"Total time for Simulation is {end - start} Seconds")


def static_grid_run(sim, setting, date_time_folder, txt_context):
    """
    Static Grid Run Sweeps across k and and N to get slot distribution and other parameters as a function of n for
    different k

    """
    start = time.time()
    user_array = [setting.grid_test.n1, setting.grid_test.n2, setting.grid_test.n3]
    k_array = range(setting.grid_test.k_start, setting.grid_test.k_stop + 1, setting.grid_test.k_step)
    aggregate_slot_array = []
    aggregate_retx_array = []
    aggregate_delay_array = []
    for users in user_array:
        mean_slot_dist = []
        mean_retx_dist = []
        mean_delay_dist = []
        for k in k_array:
            number_in_slot = []
            tx_stat_array = []
            delay_array = []
            throughput = []
            for _ in range(setting.grid_test.runs):
                # Reset the simulation
                sim.reset(setting)
                sim.sim_param.K = k
                sim.do_simulation_simple_tree_static(users)
                throughput.append(sim.sim_result.throughput / sim.sim_param.K)
                number_in_slot += sim.tree_state.number_in_slot[1:]
                tx_stat_array += sim.sim_state.tx_stat_array
                delay_array.append(sim.sim_result.mean_packet_delay)
                if sim.tree_state.total_successes != users:
                    print("Error total successes not equal to total users")
            number_in_slot = np.asarray(number_in_slot) / sim.sim_param.K
            mean_slot_dist.append(np.mean(number_in_slot))
            mean_retx_dist.append(np.mean(tx_stat_array))
            mean_delay_dist.append(np.mean(delay_array))
        aggregate_slot_array.append(mean_slot_dist)
        aggregate_retx_array.append(mean_retx_dist)
        aggregate_delay_array.append(mean_delay_dist)

    figname = date_time_folder + 'SlotDegreeDistribution'
    make_multiplot(k_array, aggregate_slot_array, user_array, ylabel='K normalized mean Packets per slot', xlabel='K',
                   save_fig=True, figname=figname)
    figname = date_time_folder + 'RetxDegreeDistribution'
    make_multiplot(k_array, aggregate_retx_array, user_array, ylabel='Mean No of Retransmissions per Packet',
                   xlabel='K',
                   save_fig=True, figname=figname)
    figname = date_time_folder + 'DelayDegreeDistribution'
    make_multiplot(k_array, aggregate_delay_array, user_array, ylabel='Mean Packet Delay', xlabel='K',
                   save_fig=True, figname=figname)
    end = time.time()
    print(F"Time for Simulaiton is {end - start} seconds")


def experimental_runs(sim, setting, date_time_folder, txt_context):
    """
    This function can be used to runs experimnetal code and tests within the framework of the GUI
    All other parameters must be inputted by User, just the parameters from the tree will remain

    """

    k_array = [1, 2, 4, 8, 10, 16, 20, 30, 40, 50, 100, 200, 500, 1000]
    stability = [0.42951, 0.47068, 0.51751, 0.56779, 0.5850039, 0.62388, 0.6435351, 0.6802734, 0.7063453, 0.7262098,
                 0.7835304, 0.8324254, 0.8832808, 0.9123721]
    # a = 0.01
    # fixed = 0.35
    # theoretical_array = fixed +  (1 - math.e**(-a*np.asarray(k_array)))
    pyplot.plot(k_array, stability)
    # pyplot.plot(k_array, theoretical_array, label='Fit')
    pyplot.xlabel("K")
    pyplot.hlines(1.0, 0, 1000, colors='red', linestyles='dashed')
    pyplot.ylabel("Normalized Optimum Stable Arrival Rate")
    pyplot.title("BTA Windowed Access")
    pyplot.legend()
    figname = date_time_folder + F"Asymptotic_K"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex', encoding='utf-8')
    pyplot.show()
    pass


if __name__ == '__main__':
    date_time_folder = make_result_folder()
    txt_context = make_result_txt(date_time_folder)
    # # This array basically just has the functions, one of which is run by the GUI
    # test_array = [simulate_tree_branching, simulate_simple_tree_static_multiple_runs, simulate_users,
    #               simulate_simple_tree_dynamic_multiple_runs, simulate_simple_tree_dynamic_multiple_runs_gated,
    #               do_theoretical, experimental_runs, static_grid_run]
    # setting = SimSetting()
    # # Seed for reproducibility
    # # np.random.seed(setting.seed)
    # if sum(setting.secondwindow.test_values) > 1:
    #     print("Multiple Tests should be done by running the script multiple times")
    #     exit()
    # sim = Simulation(setting)
    # sim.sim_param.print_settings()
    # # Comment and uncomment the below methods as it suits
    # if True not in setting.secondwindow.test_values:
    #     print("No Test Selected")
    # else:
    #     for test in test_array:
    #         if setting.secondwindow.test_values[test_array.index(test)]:
    #             print("-----------------------------------------------")
    #             print("Test Name : - " + setting.secondwindow.test_names[test_array.index(test)])
    #             sim.reset(setting)
    #             test(sim, setting, date_time_folder, txt_context)
    #             close_txt_file(txt_context)
    #             still_print(date_time_folder)
    setting = None
    sim = Simulation(setting)
    simulate_simple_tree_satic_multiple_runs_over_p(sim, setting, date_time_folder, txt_context)
