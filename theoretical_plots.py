import math
import numpy
from simparam import SimParam
from scipy.special import comb
import math


class TheoreticalPlots(object):

    # Equation from quick template
    def qarysic(self, n, setting):
        param = SimParam(setting)
        mystery_power = 1
        pj = param.branchprob
        if not param.biased_split:
            pj = 1 / param.SPLIT
        ln = 0
        t = param.K
        d = param.SPLIT
        to_sub = d
        if param.sic:
            to_sub -= 1
            mystery_power = 1
        for i in range(t + 1, n + 1):
            d_sum = 0
            for u in range(1, d + 1):
                d_sum += pj ** i
            l = 0
            for j in range(0, t + 1):
                l += self.mycomb(i, j) * ((-1) ** (i - j + 1))
            ln += self.mycomb(n, i) * l * (to_sub ** mystery_power) / (1 - d_sum)
        ln = 1 + ln
        throughput = n / ln
        return throughput / t

    # Non Recursive Equation from SICTA paper
    def sicta(self, n, setting):
        param = SimParam(setting)
        pj = param.branchprob
        ln = 0
        for i in range(2, n + 1):
            ln += (comb(n, i, exact=True)*((i-1)*((-1)**i)))/(1-(pj**i)-((1-pj)**i))
        ln = 1 + ln
        throughput = n/ln
        return throughput

    # Recursive Equaiton from Quick Template
    def recquary(self, n, setting):
        param = SimParam(setting)
        pj = param.branchprob
        if not param.biased_split:
            pj = 1/param.SPLIT
        d = param.SPLIT
        return n / self.recquaryrecursive(n, pj, d)

    def recquaryrecursive(self, n, pj, d):
        if n <= 1:
            return 1
        else:
            ln = 0
            for j in range(1, d + 1):
                l = 0
                for nj in range(0, n):
                    l += self.mycomb(n, nj)*(pj**nj)*((1-pj)**(n-nj))*self.recquaryrecursive(nj, pj, d)
                ln += l
            ln = ln / ((1-(pj**n))-((d-1)*(((1-pj)/(d-1))**n)))
            return ln

    # Recursive Equation from the SICTA paper
    def recsictarecursive(self, n, pj):
        if n <= 1:
            return 1
        else:
            ln = 0
            for i in range(0, n):
                ln += (self.binomialProb(n, i, pj) + self.binomialProb(n, n-i, pj))*self.recsictarecursive(i,pj)
            den = 1 - (pj**n) - ((1 - pj)**n)
            ln = ln/den
            return ln

    def recsicta(self, n):
        pj = 0.5
        return n / self.recsictarecursive(n, pj)


    # Recursive Equation from Capetanakis Paper
    def simpletreerecursive(self, n):
        if n <= 1:
            return 1
        else:
            k = 0
            for i in range(0, n):
                k += (self.mycomb(n, i) * (2 ** (-n))) * self.simpletreerecursive(i)
            return (1 + 2 * k) / (1 - (2 ** (-n + 1)))


    # Bunch of Helpful Functions for better performance
    def simpletree(self, n):
        return n / self.simpletreerecursive(n)

    def binomialProb(self, n, i, pj):
        return self.mycomb(n, i)*(pj**i)*((1-pj)**(n-i))

    def mycomb(self,n, k):
        out = 1
        for i in range(0,k):
            out = out*(n-i)/(k-i)
        return out



