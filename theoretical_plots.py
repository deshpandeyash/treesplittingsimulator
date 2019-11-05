import math
import numpy
from simparam import SimParam
from scipy.special import comb
import math


class TheoreticalPlots(object):
    def mycomb(self,n, k):
        out = 1
        for i in range(0,k):
            out = out*(n-i)/(k-i)
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

    def qarysic(self, n):
        param = SimParam()
        pj = 0.5
        if not param.biased_split:
            pj = 1/param.SPLIT
        ln = 0
        t = param.K
        d = param.SPLIT
        to_sub = d
        if param.sic:
            to_sub -= 1
        for i in range(t + 1, n+1):
            d_sum = 0
            for u in range(1, d + 1):
                d_sum += pj ** i
            l = 0
            for j in range(0, t + 1):
                l += (self.mycomb(i, j)*to_sub*((-1)**(i-j+1)))/(1-d_sum)
            ln += self.mycomb(n, i)*l
        ln = 1 + ln
        throughput = n/ln
        return throughput/t

    def recquary(self, n):
        param = SimParam()








