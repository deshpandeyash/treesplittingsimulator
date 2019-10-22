import math
import numpy
from simparam import SimParam
from scipy.special import comb
import math


class TheoreticalPlots(object):
    def mycomb(self,n, k):
        out = 1
        for i in range(1,n-k+1):
            out = out*((k+i)/(n-k+1-i))
        return out

    def sicta(self):
        n = 45
        pj = 0.5
        ln = 0
        for i in range(2, n + 1):
            ln += (comb(n, i, exact=True)*((i-1)*((-1)**i)))/(1-(pj**i)-((1-pj)**i))
        ln = 1 + ln
        throughput = n/ln
        return throughput

    def qarysic(self):
        param = SimParam()
        n = 40
        pj = 0.5
        ln = 0
        for i in range(param.SPLIT + 1, n+1):
            l = 0
            for j in range(1, param.SPLIT + 1):
                l += (comb(i, j, exact=True)*((-1)**(i-j-1))*(param.SPLIT - 1))/(1-((pj**n)**2))
            ln += comb(n, i, exact=True)*l
        ln = 1 + ln
        throughput = n/ln
        return throughput








