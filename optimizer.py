import numpy as np
from matplotlib import pyplot as plt
import decimal
from scipy.special import comb
from scipy.stats import poisson


"""
For now its just a scratch pad to try different optimizer functions, nothing important in terms of the simulator. 
"""
# decimal.getcontext().prec = 1000
# num_result = decimal.Decimal(0)
# den_result = decimal.Decimal(0)
# d = 2
# n = 50
# p = decimal.Decimal(0.5)
# k = 1
# num_sum = decimal.Decimal(0)
# den_sum = decimal.Decimal(0)
# mul_sum = decimal.Decimal(0)
# number_array = range(1, n-k+1)
# num_result_array = []
# den_result_array = []
# for i in number_array:
#     # Numerator
#     num_result = decimal.Decimal(((-1)**i)) * decimal.Decimal(comb(n-k, i, exact=True)) * decimal.Decimal(i / (i+k))
#     num_sum += num_result
#     num_result_array.append(num_result)
#     # Denominator
#     branch_biased = np.full(d, (1 - p) / (d - 1))
#     branch_biased[0] = p
#     pj_array = branch_biased
#     d_sum = decimal.Decimal(0)
#     for u in range(1, d+1):
#         d_sum += decimal.Decimal(decimal.Decimal(pj_array[u - 1]) ** decimal.Decimal(i+k))
#     den_result = decimal.Decimal(1) - d_sum
#     den_result = decimal.Decimal(1) / den_result
#     den_sum += den_result
#     den_result_array.append(den_result)
#     add_num_result = decimal.Decimal(comb(n, k, exact=True)) * decimal.Decimal(d) * num_result
#     mul_sum += (add_num_result * den_result)
# plt.plot(number_array, num_result_array, color='red')
# plt.tick_params('y', colors='red')
# plt.xlabel('i')
# plt.ylabel('Numerator')
# plt.twinx()
# plt.plot(number_array, den_result_array, color='blue')
# plt.tick_params('y', colors='blue')
# plt.ylabel('1/ Denominator')
# plt.title(F"K = {k}")
# print(F"Sum Numerator = { decimal.Decimal(comb(n, k, exact=True)) * decimal.Decimal(d) * num_sum}")
# print(F"Sum Denominator = {den_sum}")
# figname = f"K{k}Seperate"
# plt.savefig(figname + '.png', dpi=300)
# final_length = decimal.Decimal(1) - mul_sum
# print(F"Bn = {final_length}")
# tpt = (n / (final_length*k))
# print(F"Throughput = {tpt}")
# print(F"----------considering denominator as 1 --------------")
# magin_len = decimal.Decimal(1) - (decimal.Decimal(comb(n, k, exact=True)) * decimal.Decimal(d) *num_sum*n)
# print(F"Bn = {magin_len}")
# magic_tpt = (n / (magin_len*k))
# print(F"Magic Throughput = {magic_tpt}")
#
# plt.show()

# summer_array = []
# bummer_array =[]
# for n in range(2,50):
#     summer = 0
#     bummer = 0
#     #print(F"-------------N = {n}---------------------------------------------------------------")
#     for j in range(2, n + 1):
#         comber = comb(n, j, exact=True)
#         signer = ((-1)**j)
#         #decimer = decimal.Decimal(j) / decimal.Decimal(j + 1)
#         decimer = j - 1
#         mull = 1/(1-(2**(1-(j+1))))
#         summer += comber * signer * decimer
#         bummer += comber * signer * decimer * mull * 2
#         #print(F" Comber = {comber} Signer {signer} Decimer {decimer} Muller {mull}")
#     #print(F"Sum is {summer}")
#     #print(F"Len is {bummer}")
#     summer_array.append(summer)
#     bummer_array.append(bummer)
# plt.plot(summer_array, label='Summer')
# plt.plot(bummer_array, label='Bummer')
# for i in range(1,len(bummer_array)):
#     print((bummer_array[i] - bummer_array[i-1])*i)
# plt.show()


# d_array = []
# for i in range(1,20):
#     d_array.append(1/(1-(2**(1-(i+2)))))
# plt.plot(d_array)
# plt.show()
# print(sum(d_array))
# for i in range(1,len(d_array)):
#     print((d_array[i]-d_array[i-1])*i*2)

summer = 0
mpr = 1
m = 10
n = 90
outer = (1 - (2**(-m)))**n
for k in range(mpr + 1, n + 1):
    comber = comb(n, k, exact=True)
    inner = 1 - (2**m)
    summer += comber*(inner**(-k))
print(summer)
print(summer*outer)
