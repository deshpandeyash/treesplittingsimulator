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

d = 3
n = 100

p = 1/d
q = 1/d
r = 1/d

summer = 0
for i in range(2, (n+1)):
    first_term = ((-1)**i)*comb(n,i)
    second_term_numerator = (i-1)*(((1-p)**i)+(r**i))
    second_term_denominator = 1 - ((p**i)*(q**i)*(r**i))
    second_term = second_term_numerator / second_term_denominator
    summer += (first_term * second_term)

print(F"Throughput = {n/((summer*2)+1)}")