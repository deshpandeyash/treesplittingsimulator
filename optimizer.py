import numpy as np
import math
from matplotlib import pyplot as plt
from decimal import Decimal as dc

k_array = np.arange(21)
m = 1

def get_A(k,m):
    complex_add = 2j*math.pi / math.log(2)
    print(complex_add)
    k_sum = []
    for k_i in range(1,k+1):
        prod_array = []
        for i in range(k_i):
            prod_array.append(complex((i - 1) + complex_add))
        prod = np.prod(np.asarray(prod_array))
        k_sum.append(prod/math.factorial(k_i))
    return 1 + sum(k_sum)

plot_array = [get_A(a,m) for a in k_array]
plt.plot(k_array,plot_array)
plt.show()