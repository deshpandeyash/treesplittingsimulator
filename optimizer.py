import numpy as np
from matplotlib import pyplot as plt
from decimal import Decimal as dc
from scipy.special import gamma
import math
import tikzplotlib


def return_A(K, m):
    imag_comp = (2j * math.pi * m) / math.log(2)
    outer_k_sum = 0
    for k in range(1, K + 1):
        inner_prod = [i - 1 + imag_comp for i in range(0, k)]
        prod = np.prod(np.asarray(inner_prod))
        outer_k_sum += prod / math.factorial(k)
    return 1 + outer_k_sum


m = 1
k_range = np.arange(1, 101)
B_array = np.asarray([abs(gamma(1 + (2j * math.pi * m) / math.log(2)) * return_A(k, m)) for k in k_range])
plt.plot(k_range, B_array)
max_value = np.max(B_array)
ind_at_max = k_range[np.argmax(B_array)]
plt.vlines(ind_at_max,0,max_value, colors='red', linestyles='dashed')
plt.xlabel("K")
plt.ylabel(F"|B(K,1)|")
plt.tight_layout()
tikzplotlib.save(F"ComplexAnalysis", encoding="UTF8")
print(max_value)
plt.show()
