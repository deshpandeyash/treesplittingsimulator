import time

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import skew
import graphdisplay
import theoretical_plots
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

    # Reset the simulations with the settings
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


def simulate_tree_branching_without_viz(sim, setting, date_time_folder, txt_context):
    """
    To get the vizualization of 1 tree for the given settings and number of users as defined by simsettings and simparam
    also prints the obtained throughput, tree progression, result progression and tree depth
    """

    users = 1000

    # Reset the simulations with the settings
    sim.reset(setting)
    # Make a simulation with the given users, and Tree Parameters
    sim.do_simulation_simple_tree_static(users)
    # Results
    print(F"Throughput is = {(sim.sim_result.throughput / sim.sim_param.K)}")
    print(F"Successes {sim.tree_state.result_array.count(1)}")
    print(F"Idles {sim.tree_state.result_array.count(0)}")
    print(F"Collisions {sim.tree_state.result_array.count(2)}")
    print(F"Mean Delay {sim.sim_result.mean_packet_delay}")
    print(F"Theoretically it should be = {TheoreticalPlots().qarysic(100, sim.sim_param):.4f}")
    # skipped_result_array = list(set(sim.branch_node.ghost_array) - set(sim.branch_node.branch_array))
    # print(skipped_result_array)
    # Use Graphviz to Render the Tree
    if users < 10:
        graphdisplay.displaygraph(sim, date_time_folder)


def simulate_simple_tree_satic_multiple_runs_over_p(sim, setting, date_time_folder, txt_context):
    print(F"Starting Test")
    start = time.time()
    string1 = [F"-{i}" for i in range(1, 8)]
    string1.reverse()
    string1.append('0')
    string2 = [F"+{i}" for i in range(1, 8)]
    range_string = string1 + string2
    split_range = [3, 4]
    runs = 10
    for sp in split_range:
        print(F"****** Testing for {sp}-ary split *********")
        center_prob = round((1 / sp), 2)
        p_range = [round(center_prob - (0.01 * i), 2) for i in range(0, 4)]
        q_range = [round(center_prob + (0.01 * i), 2) for i in range(1, 12)]
        p_range.reverse()
        p_range = p_range + q_range
        throughput = []
        throughput_mean = []
        for p in p_range:
            print(F"############ setting branch prob to {p}  #################### ")
            tpt = []
            for _ in range(runs):
                sim.reset(setting)
                sim.sim_param.branchprob = p
                sim.sim_param.SPLIT = sp
                # Set branching probability for a split
                sim.sim_param.branch_biased = np.full(sim.sim_param.SPLIT,
                                                      (1 - sim.sim_param.branchprob) / (sim.sim_param.SPLIT - 1))
                sim.sim_param.branch_biased[0] = sim.sim_param.branchprob
                users = 10
                sim.do_simulation_simple_tree_static(users)
                tpt.append(sim.sim_result.throughput / sim.sim_param.K)
                print(F"_____________________________Round {_} of {runs}________________________________")
                print(sim.branch_node.branch_array)
            throughput.append(tpt)
            throughput_mean.append(np.mean(tpt))
        plt.plot(range_string, throughput_mean, label=F"{sp}")
    plt.grid()
    plt.legend()
    figname = date_time_folder + F"P_sweep"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))
    print(F"Time taken is {time.time() - start} seconds")


def simluate_simple_tree_static_multiple_runs_branch_prob(sim, setting, date_time_folder, txt_context):
    print(F"Starting Test")
    start = time.time()
    split_range = [2, 3, 4, 5, 6, 7, 8, 9]
    runs = 1000
    throughput_d = []
    idle_d = []
    idle_distr = []
    collisions_d = []
    collisions_distr = []
    succ_d = []
    succ_distr = []
    delay_d = []
    delay_distr = []
    throughput_distr = []
    for sp in split_range:
        print(F"****** Testing for {sp}-ary split *********")
        throughput = []
        delay = []
        packet_delay_distribution = []
        idles = []
        collisions = []
        successes = []
        slot_degree = []
        mean_degree = []
        for _ in range(runs):
            sim.reset(setting)
            sim.sim_param.biased_split = True
            sim.sim_param.SPLIT = sp
            sim.sim_param.branch_biased = [0.5 ** p for p in range(1, sp + 1)]
            sim.sim_param.branch_biased[-1] = sim.sim_param.branch_biased[-2]
            # print(F"The branching Probabilities are: {sim.sim_param.branch_biased}")
            users = 1000
            sim.do_simulation_simple_tree_static(users)
            throughput.append(sim.sim_result.throughput / sim.sim_param.K)
            delay.append(sim.sim_result.mean_packet_delay)
            packet_delay_distribution.append(sim.sim_state.delay_stat_array)
            idles.append(sim.tree_state.result_array.count(0) / len(sim.tree_state.result_array))
            collisions.append(sim.tree_state.result_array.count(2) / len(sim.tree_state.result_array))
            successes.append(sim.tree_state.result_array.count(1) / len(sim.tree_state.result_array))
            slot_degree.append(sim.tree_state.number_in_slot)
            # print(F"_____________________________Round {_} of {runs}________________________________")
        mean_degree = np.hstack(slot_degree)
        mean_degree = [value for value in mean_degree if value != 1]
        mean_degree = [value for value in mean_degree if value != 0]
        mean_tpt = np.mean(throughput)
        mean_delay = np.mean(delay)
        mean_idle = np.mean(idles)
        mean_collisions = np.mean(collisions)
        mean_succ = np.mean(successes)
        throughput_d.append(mean_tpt)
        idle_d.append(mean_idle)
        collisions_d.append(mean_collisions)
        succ_d.append(mean_succ)
        delay_d.append(mean_delay)
        delay_distr.append(delay)
        throughput_distr.append(throughput)
        idle_distr.append(idles)
        collisions_distr.append(collisions)
        succ_distr.append(successes)
        result = plt.hist(np.asarray(packet_delay_distribution).flatten(), density=True, color='green', alpha=0.65)
        plt.axvline(mean_delay, color='k', linestyle='dashed', linewidth=1)
        figname = date_time_folder + F"Delay Distribution d = {sp}"
        plt.savefig(figname + '.png', dpi=300)
        tikzplotlib.save(figname + '.tex')
        plt.close()
        result = plt.hist(mean_degree, density=True, color='green', alpha=0.65, bins=max(mean_degree))
        figname = date_time_folder + F"Degreee Distribution d = {sp}"
        plt.savefig(figname + '.png', dpi=300)
        tikzplotlib.save(figname + '.tex')
        plt.close()
        print(F"Mean throughput for d= {sp} is {mean_tpt}")
        print(F"Mean delay for d = {sp} is {mean_delay}")
        print(F"Median Degree is {np.median(mean_degree)}")
        print(F"Mean Degree is {np.mean(mean_degree)}")

    # Plot a stacked bar graph
    width = 0.30
    print(succ_d)
    print(idle_d)
    print(collisions_d)
    plt.bar(split_range, succ_d, width, label='Successes')
    plt.bar(split_range, idle_d, width, bottom=succ_d, label='Idle')
    plt.bar(split_range, collisions_d, width, bottom=np.asarray(idle_d) + np.asarray(succ_d), label='Collisions')
    plt.legend()
    figname = date_time_folder + F"Opt_TX_PLOT"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    plt.close()
    # Plot Mean tpt
    plt.plot(split_range, throughput_d)
    plt.grid()
    figname = date_time_folder + F"Opt_TPT"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    plt.close()
    # Plot Mean Delay
    plt.plot(split_range, delay_d)
    plt.grid()
    figname = date_time_folder + F"Opt_DELAY"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    plt.close()
    # Plot Delay Distr
    plt.boxplot(delay_distr, positions=split_range)
    plt.grid()
    figname = date_time_folder + F"distr_delay"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    plt.close()
    # Throughput Distribution
    plt.boxplot(throughput_distr, positions=split_range)
    plt.grid()
    figname = date_time_folder + F"distr_tpt"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    plt.close()
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))
    print(F"Time taken is {time.time() - start} seconds")


def simulate_simple_tree_static_single_run_direct(sim, setting, date_time_folder, txt_context):
    print(F"Starting Test")
    start = time.time()
    sim.reset(setting)
    sim.sim_param.sic = False
    sim.sim_param.biased_split = False
    sim.sim_param.SPLIT = 2
    sim.sim_param.branch_biased = [0.5 ** p for p in range(1, sim.sim_param.SPLIT + 1)]
    sim.sim_param.branch_biased[-1] = sim.sim_param.branch_biased[-2]
    print(F"The branching Probabilities are: {sim.sim_param.branch_biased}")
    users = 100
    sim.do_simulation_simple_tree_static(users)
    print(F"Mean throughput {sim.sim_result.throughput}")
    print(F"Mean delay is {sim.sim_result.mean_packet_delay}")
    result = plt.hist(sim.sim_state.delay_stat_array, bins=max(sim.sim_state.delay_stat_array), density=True,
                      color='red', alpha=0.65)
    plt.axvline(sim.sim_result.mean_packet_delay, color='k', linestyle='dashed', linewidth=1)
    figname = date_time_folder + F"Delay Distribution1"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    plt.close()
    end = time.time()
    print("Time for Simulation: " + str(end - start))
    print(F"Time taken is {time.time() - start} seconds")


def simulate_simple_tree_static_multiple_runs(sim, setting, date_time_folder, txt_context):
    """
    Does a number of runs with the same number of users, plots the distribution of throughput and prints out the
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
    plt.show()


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
    plt.plot(user_array, throughput_array, 'b-', label='simulation')
    plt.plot(user_array, theoretical_out_array, 'r', label='theoretical')
    print(F"Max Theoretical throughput is {max(theoretical_out_array):.6f}"
          F" at Users {user_array[theoretical_out_array.index(max(theoretical_out_array))]}")
    print(F"Steady State Theoretical Value =   {theoretical_out:.6f}")
    if sim.sim_param.sic and sim.sim_param.SPLIT > 2:
        plt.plot(user_array, magic_throughput_array, 'g', label='Right Skipped Simulation')
    plt.xlabel("N Users")
    plt.ylabel("Throughput")
    plt.legend()
    figname = date_time_folder + F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}UserSweep"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print(F"Time for simulation: {end - start} Seconds")
    plt.show()


def simulate_simple_tree_dynamic_multiple_runs(sim, setting, date_time_folder, txt_context):
    """
    FREE ACCESS SIMULATION
    Sweep through different arrival rate, take average through no of runs. Plot delay, success rate vs arrival rate.

    """
    start = time.time()
    if setting is None:
        rate_array = np.arange(0.60, 0.75, 0.2) * sim.sim_param.K
        runs = 1
    else:
        rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step,
                               setting.dynamictest.step)
        runs = setting.dynamictest.runs
    succ_rate = []
    delay = []
    for p in rate_array:
        counter1 = []
        counter2 = []

        for _ in range(runs):
            sim.reset(setting)
            sim.sim_param.lmbda = p
            sim.do_simulation_simple_tree_dynamic()
            counter1.append(sim.sim_result.succ_rate)
            counter2.append(sim.sim_result.mean_packet_delay)
        succ_rate.append(np.mean(counter1))
        delay.append(np.mean(counter2))
    optimum_throughput = rate_array[delay.index(max(delay))]
    print("Optimum Throughput = " + str(optimum_throughput))
    plt.plot(rate_array, succ_rate, color='red')
    plt.xlabel('Arrival rate (packets/slot)')
    plt.ylabel('Success rate')
    plt.twinx()
    plt.plot(rate_array, delay, color='blue')
    plt.ylabel('Mean Packet Delay')
    plt.show()
    plt.grid()
    figname = date_time_folder + F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}FreeArrivalSweep"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))


def simulate_simple_tree_dynamic_multiple_runs_gated(sim, setting, date_time_folder, txt_context):
    """
    GATED ACCESS SIMULATION - plots cri length and mean packet delay should add a k sweep
    """
    start = time.time()
    if setting is None:
        rate_array = np.arange(0.60, 0.75, 0.05)
        runs = 10
    else:
        rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step,
                               setting.dynamictest.step)
        runs = setting.dynamictest.runs
    # k_range = [1, 2, 4, 8, 16, 32]
    k_range = [1, 2, 4]

    delay_across_k = []
    for k in k_range:
        delay = []
        for p in rate_array:
            delay_counter = []
            delta_length_counter = []
            init_collided = []
            cri_lengths = []
            for j in range(runs):
                sim.reset(setting)
                sim.sim_param.K = k
                sim.sim_param.lmbda = p * sim.sim_param.K
                sim.do_simulation_gated_access()
                delay_counter.append(sim.sim_result.mean_packet_delay)
                cri_lengths.append(sim.sim_state.tree_length_array)
                init_collided.append(sim.sim_state.init_collision_array)
            delay.append(np.mean(delay_counter))
            # Plot the Distribution of CRI Lengths for each K and Rate
            cri_length = np.hstack(cri_lengths)
            plt.hist(cri_length, bins=np.unique(cri_length))
            figname = date_time_folder + F"K{k}lambda{p:.2f}cri_lengths"
            plt.savefig(figname + '.png', dpi=300)
            plt.clf()
            init_collided_dist = np.hstack(init_collided)
            plt.hist(init_collided_dist, bins=np.unique(cri_length))
            figname = date_time_folder + F"K{k}lambda{p:.2f}init_collided"
            plt.savefig(figname + '.png', dpi=300)
            plt.clf()
        delay_across_k.append(delay)
    for count, the_delay in enumerate(delay_across_k):
        plt.plot(rate_array, the_delay, label=F"K={k_range[count]}")
    plt.xlabel('Lambda/K')
    plt.ylabel('Delay in Slots')
    plt.title(F"Mean Packet Delay")
    plt.legend()
    plt.grid()
    figname = date_time_folder + F"K{k_range[count]}Q{sim.sim_param.SPLIT}GatedArrivalSweep"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex', encoding='utf-8')
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
    Static Grid Run Sweeps across k and N to get slot distribution and other parameters as a function of n for
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
    plt.plot(k_array, stability)
    # plt.plot(k_array, theoretical_array, label='Fit')
    plt.xlabel("K")
    plt.hlines(1.0, 0, 1000, colors='red', linestyles='dashed')
    plt.ylabel("Normalized Optimum Stable Arrival Rate")
    plt.title("BTA Windowed Access")
    plt.legend()
    figname = date_time_folder + F"Asymptotic_K"
    plt.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex', encoding='utf-8')
    plt.show()
    pass


def experimental_run_1(sim, setting, date_time_folder):
    start = time.time()
    theorstudy.traffic_analysis(sim, setting, date_time_folder)
    end = time.time()
    print(F"Time for Simulaiton is {end - start} seconds")


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
    # simulate_simple_tree_satic_multiple_runs_over_p(sim, setting, date_time_folder, txt_context)
    # simluate_simple_tree_static_multiple_runs_branch_prob(sim, setting, date_time_folder, txt_context)

    # simulate_simple_tree_static_single_run_direct(sim, setting, date_time_folder, txt_context)
    # simulate_tree_branching_without_viz(sim, setting, date_time_folder, txt_context)
    # simulate_simple_tree_dynamic_multiple_runs_gated(sim, setting, date_time_folder, txt_context)
    experimental_run_1(sim, setting, date_time_folder)
