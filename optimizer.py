import numpy as np
from matplotlib import pyplot as plt
from decimal import Decimal as dc
from decimal import *
from scipy.special import gamma
import math
import tikzplotlib


def return_A(K, m):
    imag_comp = dc((2 * math.pi * m) / math.log(2))
    prod_real = dc(-(imag_comp * imag_comp))
    prod_imag = dc(-imag_comp)
    outer_k_sum_real = dc(1)
    outer_k_sum_imag = dc(0)
    for k in range(1, K + 1):
        prod_real_temp = prod_real
        prod_img_temp = prod_imag
        for i in range(1, k-1):
            prod_real = (prod_real_temp * i) - (prod_img_temp * imag_comp)
            prod_imag = (prod_img_temp * i) + (prod_real_temp * imag_comp)
        denom = dc(math.factorial(k))
        prod_div_real = (prod_real / denom)
        prod_div_imag = (prod_imag / denom)
        outer_k_sum_real += prod_div_real
        outer_k_sum_imag += prod_div_imag
    return outer_k_sum_real, outer_k_sum_imag


def return_A_simple(K,m):

    imag_comp = (2j*math.pi*m) / math.log(2)
    outer_sum = 0
    for k in range(1,K+1):
        inner_prod = np.prod(np.asarray([(i-1)+imag_comp for i in range(0, k)]))
        outer_sum += (inner_prod / math.factorial(k))
    return 1 + outer_sum

def return_B_simple(K,m):
    return gamma(-1 + ((2j * math.pi * m) / math.log(2))) * return_A_simple(K, m)

def return_B(K, m):
    muller = gamma(-1 + ((2j * math.pi * m) / math.log(2)))
    multiplier_real = dc(muller.real)
    multiplier_imag = dc(muller.imag)
    A_real, A_img = return_A(K, m)
    term_real = (multiplier_real * A_real) - (multiplier_imag * A_img)
    term_img = (multiplier_imag * A_real) + (multiplier_real * A_img)
    return term_real, term_img


def make_tpt_analysis(n_range, k, m):
    b_real, b_imag = return_B(k, m)
    b_abs = float(Decimal.sqrt((b_real**2) + (b_imag**2)))
    b_arg = float(math.atan2(b_imag, b_real))
    tpt = []
    for n in range(1, n_range):
        tpt.append(math.log(2) / (1 - (2 * k * b_abs) * math.cos((2 * math.pi * math.log2(n)) + b_arg)))
    plt.plot(tpt)
    plt.show()

def make_b_k_analysis_simple(k_range_final, m):
    k_range = range(1, k_range_final)
    B_abs = []
    B_arg = []
    for k in k_range:
        b = return_B_simple(k, m)
        b_abs = abs(b)
        b_arg = math.atan2(b.imag, b.real)
        B_arg.append(b_arg)
        B_abs.append(2 * k * b_abs)
    plt.plot(k_range, B_abs)
    # plt.plot(k_range, B_arg)
    plt.yscale("log")
    plt.xlabel("K")
    plt.ylabel(F"2 K |B(K,1)|")
    plt.grid()
    plt.tight_layout()


def make_b_k_analysis(k_range_final, m):
    k_range = range(1, k_range_final)
    B_abs = []
    B_arg = []
    for k in k_range:
        b_real, b_imag = return_B(k, m)
        b_abs = Decimal.sqrt((b_real**2) + (b_imag**2))
        b_arg = math.atan2(b_imag, b_real)
        B_arg.append(b_arg)
        B_abs.append(2*k*b_abs)
    plt.plot(k_range, B_abs)
    # plt.plot(k_range, B_arg)
    plt.yscale("log")
    plt.xlabel("K")
    plt.ylabel(F"2 K |B(K,1)|")
    plt.grid()
    plt.tight_layout()


getcontext().prec = 100


make_b_k_analysis(300,1)
# make_tpt_analysis(100,32,1)
plt.show()
