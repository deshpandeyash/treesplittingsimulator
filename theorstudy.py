from matplotlib import pyplot
from theoretical_plots import TheoreticalPlots
import tikzplotlib
import numpy as np
from make_stat import create_ideal_by_regression
import math
from scipy.special import comb
import pandas as pd


def compare_different_functions(sim, setting, date_time_folder):
    """
    Does Theoretical iterations similar to n_sweep for different tree algorithm formulas given by different papers

    """

    param = sim.sim_param
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
    figname = date_time_folder + F"K{sim.sim_param.K}Q{sim.sim_param.SPLIT}TheoreticalCalc"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    pyplot.show()


def length_throughput_plot(sim, setting, date_time_folder):
    """
    This plot allows for plotting Ln or Throuhghput, normalized or non-normalized and with a log scale on either axis
    """

    k_array = [setting.osctest.k1, setting.osctest.k2, setting.osctest.k3, setting.osctest.k4, setting.osctest.k5]
    # The stop In N_Sweep
    n_stop = setting.osctest.n_stop
    test_throughput = setting.osctick.test_values[0]
    x_scale_log = setting.osctick.test_values[1]
    y_scale_log = setting.osctick.test_values[2]
    n_start_one = setting.osctick.test_values[3]
    plot_max = setting.osctick.test_values[4]
    k_normalize = setting.osctick.test_values[5]
    multiple_theoretical = []
    maximum_array = []
    n_array = []
    for k in k_array:
        sim.sim_param.K = k
        if n_start_one:
            user_array = np.arange(1, n_stop)
        else:
            user_array = np.arange(sim.sim_param.K + 1, n_stop)
        theoretical = []
        for n in user_array:
            if test_throughput:
                theoretical.append(TheoreticalPlots().qarysic(n, sim.sim_param))
            else:
                theoretical.append(TheoreticalPlots().qarylen(n, sim.sim_param))
        multiple_theoretical.append(theoretical)
        maximum_array.append(max(theoretical))
        n_array.append(user_array[theoretical.index(max(theoretical))])
        pyplot.plot(user_array, theoretical, label=f"K = {k}")
        if not test_throughput and not k_normalize:
            slope_intercept = create_ideal_by_regression(user_array, theoretical)
            slope = slope_intercept[0][0]
            intercept = slope_intercept[1]
            print(F"----------------K = {k} ---------------------------------")
            print(F"First order Linear Approximation: of the line.. Slope = {slope} intercept = {intercept}")
            index_to_text = int(n_stop / 5)
            l2 = np.array((float(user_array[-index_to_text]), float(theoretical[-index_to_text])))
            trans_angle = pyplot.gca().transData.transform_angles(np.array((np.degrees(math.atan(slope)),)),
                                                                  l2.reshape((1, 2)))[0]
            pyplot.text(l2[0], l2[1], F"Slope={slope:.3f}", rotation=trans_angle, rotation_mode='anchor')
    if plot_max:
        pyplot.plot(n_array, maximum_array, 'r--', label='Maximum')
    print(F"N array is {n_array}")
    if x_scale_log:
        pyplot.xscale('log')
    if y_scale_log:
        pyplot.yscale('log')
    pyplot.xlabel('Users')
    if test_throughput:
        pyplot.ylabel('Throughput')
    else:
        pyplot.ylabel('Length')
    pyplot.legend()
    pyplot.grid()
    figname = date_time_folder + f"Q{sim.sim_param.SPLIT}allKplotsp"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex', encoding='utf-8')
    pyplot.show()


def show_optimal_branchprob(sim, setting, date_time_folder):
    """
    Shows what happens when you change the probability pj for a fixed number of users
    """
    k_array = [setting.branchtest.k1, setting.branchtest.k2, setting.branchtest.k3, setting.branchtest.k4,
               setting.branchtest.k5]
    pj_array = np.arange(setting.branchset.p_start, setting.branchset.p_stop + setting.branchset.p_step,
                         setting.branchset.p_step)
    users = int(setting.branchset.users)
    for k in k_array:
        theoretical = []
        sim.sim_param.K = k
        for p in pj_array:
            sim.sim_param.branchprob = p
            theoretical.append(TheoreticalPlots().qarysic(users, sim.sim_param))
        pyplot.plot(pj_array, theoretical, label=f"K = {k}")
    pyplot.legend()
    pyplot.xlabel("Probability to Choose 1st Slot")
    pyplot.ylabel(F"Throughput for {users} Users")
    figname = date_time_folder + f"unfairSplit"
    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex')
    pyplot.show()


def traffic_analysis(sim, setting, date_time_folder):
    """
    Finds upper and lower bounds and also plots the optimal Stability arrival rate for windowed access
    """
    if setting is None:
        k_array = [1, 2, 4, 8, 16, 32, 64]
        alpha_opt = [1.4427, 0.7214, 0.3607, 0.1808, 0.0919, 0.0480, 0.0254]
        beta_opt = [1.4427, 0.7213, 0.3606, 0.1799, 0.0884, 0.0421, 0.0199]
        m_array = [50, 100, 200, 400, 400, 400, 500]
        ld_array_end_points = [20, 20, 20, 20, 15, 30, 60]
        m = 50
        lambda_delta_array = np.linspace(0.00, 400, 2000)
    else:
        k_array = [setting.boundstest.k1, setting.boundstest.k2, setting.boundstest.k3, setting.boundstest.k4,
                   setting.boundstest.k5]
        m = int(setting.boundsset.m)
        lambda_delta_array = np.linspace(setting.boundsset.start, setting.boundsset.stop,
                                         setting.boundsset.no_of_readings)
    bounds_table = pd.DataFrame()
    alpha_array_bound = []
    beta_array_bound = []
    alpha_k_array_bound = []
    beta_k_array_bound = []
    lambda_lower_array_bound = []
    lambda_upper_array_bound = []
    lambda_delta_array_bound = []
    delta_array_bound = []

    if sim.sim_param.sic:
        to_add = 0
    else:
        to_add = 1
    df = pd.read_csv('SIC_K_d_2')
    print(F"m = {m} ")
    for item in range(len(k_array)):
        k = k_array[item]
        sim.sim_param.K = k
        n_array = np.arange(m + 1, m + 500)
        alpha_plot = []
        for n in n_array:
            numerator = 0
            denominator = 0
            for i in range(0, m):
                # li_p = TheoreticalPlots().qarylen(i, sim.sim_param)
                li = df[F"{k}"][i]
                comber = comb(n, i, exact=True)
                numerator += comber * (float(li) + to_add)
                denominator += comber * i
            alpha_plot.append(numerator / denominator)
        # alpha_lb = min(alpha_plot)
        # alpha_ub = max(alpha_plot)
        alpha_lb = alpha_opt[item]
        alpha_ub = beta_opt[item]
        print(F"............................................................")
        print(F"For k = {k} ")
        print(F"Lower Bound {alpha_lb:.7f} and Upper Bound = {alpha_ub:.7f}")
        print(F"Normalizing with K")
        print(F"Lower Bound {alpha_lb * k:.7f} and Upper Bound {alpha_ub * k:.7f}")

        alpha_array_bound.append(round(float(alpha_lb), 6))
        beta_array_bound.append(round(float(alpha_ub), 6))
        alpha_k_array_bound.append(round(float(alpha_lb * k), 6))
        beta_k_array_bound.append(round(float(alpha_ub * k), 6))

        # Now onto the Windowed Access Results
        lambda_upper_array = []
        lambda_lower_array = []

        m_item = m_array[item]

        t_plots = TheoreticalPlots(csv_name='SIC_K_d_2')

        lambda_delta_array = np.arange(0, ld_array_end_points[item], 0.001)

        for lambda_delta in lambda_delta_array:
            f_upper = t_plots.windowed_bound(sim.sim_param, alpha_ub, m_item, lambda_delta)
            lambda_upper_array.append(lambda_delta / float(f_upper))
            f_lower = t_plots.windowed_bound(sim.sim_param, alpha_lb, m_item, lambda_delta)
            lambda_lower_array.append(lambda_delta / float(f_lower))
        lambda_upper_array = np.asarray(lambda_upper_array) / k
        lambda_lower_array = np.asarray(lambda_lower_array) / k
        lambda_upper = max(lambda_upper_array)
        lambda_lower = max(lambda_lower_array)
        arg_index = np.argmax(lambda_upper_array)
        optimum_lambda_delta = lambda_delta_array[arg_index]
        optimum_window = optimum_lambda_delta / lambda_upper
        pyplot.plot(lambda_delta_array, lambda_upper_array, label=F"K{k}")
        print(F"Lower Bound on Lambda is {lambda_lower:.7f} and upper bound is {lambda_upper:.7f}")
        print(F"Optimum lambda-Delta is {optimum_lambda_delta} and optimum window size is {optimum_window}")
        lambda_lower_array_bound.append(round(float(lambda_lower), 6))
        lambda_upper_array_bound.append(round(float(lambda_upper), 6))
        lambda_delta_array_bound.append(round(float(optimum_lambda_delta), 6))
        delta_array_bound.append(round(float(optimum_window), 6))
    figname = date_time_folder + f"WindowedAccessPLots"
    bounds_table['K'] = k_array
    bounds_table['alpha'] = alpha_array_bound
    bounds_table['beta'] = beta_array_bound
    bounds_table['alphaK'] = alpha_k_array_bound
    bounds_table['betaK'] = beta_k_array_bound
    bounds_table['lambdaUpper'] = lambda_upper_array_bound
    bounds_table['lambdaLower'] = lambda_lower_array_bound
    bounds_table['lambdaDelta'] = lambda_delta_array_bound
    bounds_table['Delta'] = delta_array_bound
    with open(figname + 'table.tex', 'w') as tf:
        tf.write(bounds_table.to_latex())
    pyplot.xlabel("Lambda_Delta")
    pyplot.ylabel("Lambda")
    pyplot.legend()
    pyplot.grid()

    pyplot.savefig(figname + '.png', dpi=300)
    tikzplotlib.save(figname + '.tex', encoding='utf-8')
    # pyplot.show()
