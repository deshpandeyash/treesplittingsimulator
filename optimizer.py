import numpy as np
from matplotlib import pyplot as plt
from decimal import Decimal
from scipy.special import comb

"""
For now its just a scratch pad to try different optimizer functions, nothing important in terms of the simulator. 
"""

prob_array = np.arange(0.1, 1.0, 0.1)

d = 2
n = 9
number_array = range(2, n + 1)
result_array = []

result = Decimal(0)

for i in number_array:
    result_array = []
    for p in prob_array:
        branch_biased = np.full(d, (1 - p) / (d - 1))
        branch_biased[0] = p
        pj_array = branch_biased
        d_sum = Decimal(0)
        for u in range(1, 3):
            d_sum += Decimal(Decimal(pj_array[u - 1]) ** Decimal(i))
        #result = Decimal(1) / (Decimal(1) - d_sum)
        result = Decimal(1) - d_sum
        result_array.append(result)
    plt.plot(prob_array, result_array, label=F"{i}")
plt.legend()
plt.grid()
plt.show()

result_array = []
for i in number_array:
    result = comb(n, i) * (i-1) * ((-1)**i)
    result_array.append(result)
plt.plot(result_array)
print(sum(result_array))
plt.show()

