import math

import numpy as np
from matplotlib import pyplot as plt
import decimal
from scipy.special import comb
from scipy.stats import poisson
from math import factorial as fact


"""
For now its just a scratch pad to try different optimizer functions, nothing important in terms of the simulator. 
"""
# decimal.getcontext().prec = 1000

lmbda = 0.69
k = 4
i = 1
muxer = lmbda*i*k
mux = math.e ** (-muxer)
summer = 0
for j in range(k):
    summer += (muxer ** j)/math.factorial(j)
final = mux * summer
print(final)
