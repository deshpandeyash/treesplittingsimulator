import math
import macholib
import numpy
from simparam import SimParam
from scipy.special import comb
import math


# Q-ary tree with SIC
if __name__ == '__main__':
    # Define Parameters
    param = SimParam()
    n = 2
    pj = 0.5
    ln = 0
    # for i in range(param.SPLIT, n+1):
    #     l = 0
    #     for j in range(0, param.SPLIT + 1):
    #         l += comb(i, j)*(math.pow(-1, i-j+1)/(pow(pj, n)))
    #     ln += comb(n, i)*l
    for i in range(param.SPLIT, n + 1):
        ln += comb(n,i)*(i-1)*(-1**i)
    print((1 + ln)/n)


