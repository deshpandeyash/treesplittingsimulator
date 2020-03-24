import numpy as np
from matplotlib import pyplot as plt
from decimal import Decimal as dc

prob_array = np.arange(0.1, 1.0, 0.1)
print(prob_array)

i = 30
result_array = []
d_sum = 0
for p in prob_array:
    for i in range(1,3):
        d_sum += p ** i
    result = 1 - power1 - power2
    result_array.append(result)
plt.plot(prob_array, result_array)
plt.show()

