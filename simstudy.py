import time
import numpy as np
from matplotlib import pyplot
from scipy.stats import skew
import graphdisplay
from make_stat import mean_confidence_interval, make_histogram_cont, make_histogram_discrete
from make_stat import make_multiplot, plot_conf_interval
from simparam import SimParam
from simsetting import SimSetting
from simulation import Simulation
from theoretical_plots import TheoreticalPlots
import tikzplotlib


def simulate_tree_branching(sim, setting):
    """
    To get the vizualization of 1 tree for the given settings and number of users as defined by simsettings and simparam
    also prints the obtained throughput, tree progression, result progression and tree depth
    """

    # os.environ["PATH"] += os.pathsep + r'C:\Users\Murat\Anaconda3\Library\bin\graphviz'
    sim.reset(setting)
    sim.do_simulation_simple_tree_static(setting.vizwindow.users)
    print("Results were: ")
    print(sim.tree_state.result_array)
    print("Tree Progression was: ")
    print(sim.branch_node.branch_array[:-1])
    print("Throughput is = " + str(sim.sim_result.throughput / sim.sim_param.K))

    print("Theoretically it should be = " + str.format('{0:.15f}', TheoreticalPlots().qarysic(setting.vizwindow.users,
                                                                                              sim.sim_param)))
    print("Magic Throughput " + str(sim.sim_result.magic_throughput))
    print("The Depth of the tree is: " + str(sim.sim_result.mean_tree_depth))
    graphdisplay.displaygraph(sim)


def simulate_simple_tree_static_multiple_runs(sim, setting):
    """
    Does a a number of runs with the same number of users, plots the distribution of throughput and prints out the
    theoretical throughput
    """
    print_result = True
    start = time.time()
    conf_intervals = []
    number_in_slot = []
    tx_stat_array = []
    throughput = []
    magic_throughput = []
    for _ in range(setting.statictreewindow.runs):
        # Reset the simulation
        sim.reset(setting)
        # users = np.random.poisson(setting.statictreewindow.users)
        users = setting.statictreewindow.users
        sim.do_simulation_simple_tree_static(users)
        throughput.append(sim.sim_result.throughput / sim.sim_param.K)
        number_in_slot += sim.tree_state.number_in_slot[1:]
        tx_stat_array += sim.sim_state.tx_stat_array
        magic_throughput.append(sim.sim_result.magic_throughput / sim.sim_param.K)
        if sim.tree_state.total_successes != users:
            print("Error total successes not equal to total users")
    conf_mean, conf_min, conf_max = mean_confidence_interval(throughput, 0.95)
    conf_intervals.append((conf_min, conf_max))
    theoretical_throughput = TheoreticalPlots().qarysic(1000, sim.sim_param)
    # Create F Strings for print
    std_dev = F"Standard Deviation = {np.std(np.asarray(throughput))}"
    skewness = F"Skewness in throughput distribution = {skew(np.asarray(throughput))}"
    mean_throughput = F"Mean Throughput = {np.mean(throughput)}"
    theoretical_mean_throughput = F"Theoretical Throughput = {theoretical_throughput:.6f}"
    left_skipped_throughput = F"Left Skipped Throughput = {np.mean(magic_throughput)}"
    if print_result:
        print(std_dev)
        print(skewness)
        print(mean_throughput)
        print(theoretical_mean_throughput)
        if sim.sim_param.sic and sim.sim_param.SPLIT > 2:
            print("This is the problem with the Giannakis Equation for d > 2 but, ")
            print(left_skipped_throughput)
    # Plots start here
    # First the throughput histogram
    make_histogram_cont(throughput, sim, xlabel='Throughput', conf_ints=(conf_min, conf_max),
                        theoretical_mean=theoretical_throughput, save_fig=True)
    # Then the Packet in a slot distribuiton
    number_in_slot = np.asarray(number_in_slot) / sim.sim_param.K
    make_histogram_discrete(number_in_slot, sim, setting, xlabel='Packets in a Slot', save_fig=False)
    # Then the retransmission Distribution
    make_histogram_discrete(tx_stat_array, sim, setting, xlabel='Transmissions per Packet', save_fig=False)
    end = time.time()
    print("Time for simulation: " + str(end - start))
    pyplot.show()


def simulate_users(sim, setting):
    """
    Sweeps through number of users, taking an average over the runs defined in simsetting for each run.
    At the same time plots the theoretical results.
    :param n_stop: Till the number of users we wish to plot.
    """
    start = time.time()
    throughput_array = []
    theoretical_out_array = []
    magic_throughput_array = []
    user_array = np.arange(sim.sim_param.K + 1, setting.usersweep.n_stop)
    for n in user_array:
        throughput = []
        magic = []
        for _ in range(setting.usersweep.runs):
            # Reset the simulation
            sim.reset(setting)
            sim.do_simulation_simple_tree_static(np.random.poisson(n))
            # sim.do_simulation_simple_tree_static(n)
            throughput.append(sim.sim_result.throughput / sim.sim_param.K)
            magic.append(sim.sim_result.magic_throughput / sim.sim_param.K)
        throughput_array.append(np.mean(throughput))
        magic_throughput_array.append(np.mean(magic))
        theoretical_out_array.append(TheoreticalPlots().qarysic(n, sim.sim_param))
    theoretical_out = TheoreticalPlots().qarysic(setting.usersweep.n_stop, sim.sim_param)
    pyplot.plot(user_array, throughput_array, 'b-', label='simulation')
    pyplot.plot(user_array, theoretical_out_array, 'r', label='theoretical')
    print(F"Max Theoretical throughput is {max(theoretical_out_array):.6f}"
          F" at Users {user_array[theoretical_out_array.index(max(theoretical_out_array))]}")
    print(F"Steady State Theoretical Value =   {theoretical_out:.6f}")
    # pyplot.plot(user_array, magic_throughput_array, 'g', label='Right Skipped Simulation')
    pyplot.xlabel("Mean Users")
    pyplot.ylabel("Throughput")
    pyplot.legend()
    figname = F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}UserSweep"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print(F"Time for simulation: {end - start} Seconds")
    pyplot.show()


def simulate_simple_tree_dynamic_multiple_runs(sim, setting):
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
    figname = F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}FreeArrivalSweep"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))


def simulate_simple_tree_dynamic_multiple_runs_gated(sim, setting):
    start = time.time()
    rate_array = np.arange(setting.dynamictest.start, setting.dynamictest.stop + setting.dynamictest.step,
                           setting.dynamictest.step)
    delay = []
    for p in rate_array:
        counter = []
        for _ in range(setting.dynamictest.runs):
            sim.reset(setting)
            sim.sim_param.lmbda = p
            sim.do_simulation_gated_access()
            counter.append(sim.sim_result.mean_packet_delay)
        delay.append(np.mean(counter))
    pyplot.plot(rate_array, delay, color='blue')
    pyplot.xlabel('Arrival rate (packets/slot)')
    pyplot.ylabel('Mean Packet Delay')
    pyplot.grid()
    figname = F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}GatedArrivalSweep"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    pyplot.show()
    end = time.time()
    print("Time for Simulaiton: " + str(end - start))


def do_theoretical_iter(sim, setting):
    """
    :param n_stop: till the end of number of users we want to sweep till
    can be used to compare different formulas in different formulas in different papers.
    plots the throughput vs number of users
    :return:
    """

    param = SimParam(setting)
    users = range(param.K + 1, setting.theorsweep.n_stop + 1)
    theoretical = []
    theoretical1 = []
    theoretical2 = []
    theoretical3 = []
    theoretical4 = []
    theoretical5 = []
    for n in users:
        if setting.theorsweep.test_values[0]:
            theoretical.append(TheoreticalPlots().qarysic(n, param))
        if setting.theorsweep.test_values[1]:
            theoretical1.append(TheoreticalPlots().sicta(n, param))
        if setting.theorsweep.test_values[2]:
            theoretical2.append(TheoreticalPlots().simpletree(n))
        if setting.theorsweep.test_values[3]:
            theoretical3.append(TheoreticalPlots().recsicta(n))
        if setting.theorsweep.test_values[4]:
            theoretical4.append(TheoreticalPlots().recquary(n, param))
        if setting.theorsweep.test_values[5]:
            theoretical5.append(TheoreticalPlots().qsicta(n, param))
    if setting.theorsweep.test_values[0]:
        pyplot.plot(users, theoretical, 'b-', label='Quary Sic')
    if setting.theorsweep.test_values[1]:
        pyplot.plot(users, theoretical1, 'g-', label='SICTA')
    if setting.theorsweep.test_values[2]:
        pyplot.plot(users, theoretical2, 'r-', label='Simple Tree')
    if setting.theorsweep.test_values[3]:
        pyplot.plot(users, theoretical3, 'c-', label='Recursive SICTA')
    if setting.theorsweep.test_values[4]:
        pyplot.plot(users, theoretical4, 'm-', label='Recursive Quary')
    if setting.theorsweep.test_values[5]:
        pyplot.plot(users, theoretical5, 'y-', label='QSICTA Giannakkis')

    pyplot.xlabel('Users')
    pyplot.ylabel('Throughput')
    pyplot.legend()
    pyplot.grid()
    # pyplot.xscale('log')
    figname = F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}TheoreticalCalc"
    pyplot.savefig(figname + '.png', dpi=300)
    # tikzplotlib.save(figname + '.tex')
    pyplot.show()


def static_grid_run(sim, setting):
    """
    Static Grid Run Sweeps across k and and N to get slot distribution and other parameters as a function of n for
    different k

    """
    start = time.time()
    user_array = [10, 50, 100]
    k_array = range(1, 9)
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
            for _ in range(setting.statictreewindow.runs):
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

    make_multiplot(k_array, aggregate_slot_array, user_array, ylabel='K normalized mean Packets per slot', xlabel='K',
                   save_fig=True, figname='SlotDegreeDistribution')
    make_multiplot(k_array, aggregate_retx_array, user_array, ylabel='Mean No of Retransmissions per Packet',
                   xlabel='K',
                   save_fig=True, figname='RetxDegreeDistribution')
    make_multiplot(k_array, aggregate_delay_array, user_array, ylabel='Mean Packet Delay', xlabel='K',
                   save_fig=True, figname='DelayDegreeDistribution')
    end = time.time()
    print(F"Time for Simulaiton is {end - start} seconds")


def experimental_runs(sim, setting):
    """
    This function can be used to runs experimnetal code and tests within the framework of the GUI
    For now I am using this to figure out a formula for Q ary SIC and a closed form equation for a maximum of K

    """

    # ------------------------------------ For the Large Oscillation Plot -----------------------------------
    #start = time.time()
    # k_array = [1, 5, 10, 15, 30, 50]
    # multiple_theoretical = []
    # maximum_array = []
    # n_array = []
    # for k in k_array:
    #     sim.sim_param.K = k
    #     user_array = np.arange(sim.sim_param.K + 1, setting.usersweep.n_stop)
    #     theoretical = []
    #     for n in user_array:
    #         theoretical.append(TheoreticalPlots().qarysic(n, sim.sim_param))
    #     multiple_theoretical.append(theoretical)
    #     maximum_array.append(max(theoretical))
    #     n_array.append(user_array[theoretical.index(max(theoretical))])
    #     pyplot.plot(user_array, theoretical, label=f"K = {k}")
    # pyplot.plot(n_array, maximum_array, 'r--', label='Maximum')
    #
    # pyplot.xscale('log')
    # pyplot.legend()
    # pyplot.xlabel('Users')
    # pyplot.ylabel('Throughput')
    # figname = f"Q{sim.sim_param.SPLIT}allKplotsp"
    # pyplot.savefig(figname + '.png', dpi=300)
    # tikzplotlib.save(figname + '.tex')
    #
    # pyplot.show()
    # end = time.time()
    # print("Time for Simulations = " + str(end-start))

    # ----------------- For the plot that shows optimal pj --------------------------------------------------
    # start = time.time()
    # k_array = [1, 3, 5, 10]
    # pj_array = [0.1, 0.2, 0.3,  0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # for k in k_array:
    #     theoretical = []
    #     sim.sim_param.K = k
    #     for p in pj_array:
    #         sim.sim_param.branchprob = p
    #         theoretical.append(TheoreticalPlots().qarysic(100, sim.sim_param))
    #     pyplot.plot(pj_array,theoretical, label=f"K = {k}")
    # pyplot.legend()
    # pyplot.xlabel("Probability to Choose 1st Slot")
    # pyplot.ylabel("Throughput for 100 Users")
    # figname = f"unfairSplit"
    # pyplot.savefig(figname + '.png', dpi=300)
    # tikzplotlib.save(figname + '.tex')
    # pyplot.show()
    # end = time.time()
    # print("Time for Simulations = " + str(end-start))

    # -------------------------- Windowed Accesss ------------------------------------------------------
    start = time.time()
    z_array = np.arange(0, 5, 0.1)
    fz_array = TheoreticalPlots().windowed_sic(sim.sim_param, z_array)
    max_f = max(fz_array)
    min_f = min(fz_array)
    indexer = np.argmax(fz_array)
    optimum_z = z_array[indexer]
    pyplot.plot(z_array, fz_array)
    pyplot.vlines(optimum_z, min_f, max_f)
    end = time.time()
    pyplot.xlabel('z')
    pyplot.ylabel('fz')
    pyplot.show()
    print(F"Max Fz is {max_f:.4f} for Z = {optimum_z}")
    print(F"Time for Simulation is {end-start} seconds")


if __name__ == '__main__':
    # This array basically just has the functions, one of which is run by the GUI
    test_array = [simulate_tree_branching, simulate_simple_tree_static_multiple_runs, simulate_users,
                  simulate_simple_tree_dynamic_multiple_runs, simulate_simple_tree_dynamic_multiple_runs_gated,
                  do_theoretical_iter, experimental_runs, static_grid_run]
    setting = SimSetting()
    # Seed for reproducibility
    # np.random.seed(setting.seed)
    if sum(setting.secondwindow.test_values) > 1:
        print("Multiple Tests should be done by running the scrip multiple times")
        exit()
    sim = Simulation(setting)
    sim.sim_param.print_settings()
    # Comment and uncomment the below methods as it suits
    if True not in setting.secondwindow.test_values:
        print("No Test Selected")
    else:
        for test in test_array:
            if setting.secondwindow.test_values[test_array.index(test)]:
                sim.reset(setting)
                test(sim, setting)
