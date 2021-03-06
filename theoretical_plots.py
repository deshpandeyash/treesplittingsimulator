from scipy.special import comb
import decimal
from math import log
import numpy as np

from simparam import SimParam


class TheoreticalPlots(object):

    decimal.getcontext().prec = 1000

    # Equation from quick template
    def qarysic(self, n, param):
        """
        Final Equation from the paper published by H. Murat Gursu, Yash Deshpande etc.
        Includes all parameters and additionaly a d parameter for a d-ary split which will be fixed after correction in
        the old Giannakis paper.
        Main addition in the K-MPR parameter.
        """
        param.branch_biased = np.full(param.SPLIT, (1 - param.branchprob) / (param.SPLIT - 1))
        param.branch_biased[0] = param.branchprob
        pj_array = param.branch_biased
        ln = decimal.Decimal(0)
        t = param.K
        d = param.SPLIT
        to_sub = d
        if param.sic:
            to_sub -= 1
        for i in range(1, n + 1):
            d_sum = decimal.Decimal(0)
            for u in range(1, d + 1):
                d_sum += decimal.Decimal(decimal.Decimal(pj_array[u - 1]) ** decimal.Decimal((i + t)))
            d_sum_sub = decimal.Decimal(1) - d_sum
            ln += comb(n - t, i, exact=True) * ((-1) ** (i + 1)) * i / (d_sum_sub * (i + t))
        ln = 1 + (ln * to_sub * comb(n, t, exact=True))
        throughput = n / ln
        if n > t:
            return throughput / t
        else:
            return 1



    def qsicta(self, n, param):
        """
        Equation from giannakis and yu for the d-ary SICTA
        """
        param.branch_biased = np.full(param.SPLIT, (1 - param.branchprob) / (param.SPLIT - 1))
        param.branch_biased[0] = param.branchprob
        pj_array = param.branch_biased
        if not param.biased_split:
            pj = 1 / param.SPLIT
        ln = decimal.Decimal(0)
        d = param.SPLIT
        to_sub = d
        if param.sic:
            to_sub -= 1
        for i in range(2, n + 1):
            d_sum = decimal.Decimal(0)
            for u in range(1, d + 1):
                d_sum += decimal.Decimal(decimal.Decimal(pj_array[u - 1]) ** decimal.Decimal(i))
            d_sum_sub = decimal.Decimal(1) - d_sum
            ln += (self.mycomb(n, i) * to_sub * (i - 1) * ((-1) ** i)) / d_sum_sub
        ln = 1 + ln
        throughput = n / ln
        if n > 2:
            return throughput
        else:
            return 1

    # Non Recursive Equation from SICTA paper
    def sicta(self, n, param):
        """
        Equation for the binary SICTA which also first appeared in the Giannakis paper
        """
        pj = param.branchprob
        ln = 0
        for i in range(2, n + 1):
            ln += (comb(n, i, exact=True) * ((i - 1) * ((-1) ** i))) / (1 - (pj ** i) - ((1 - pj) ** i))
        ln = 1 + ln
        throughput = n / ln
        return throughput

    # Recursive Equaiton from Quick Template
    def recquary(self, n, param):
        """
        Recursive Equation from the paper by H Murat Gürsu and Yash Deshpande, this is the recursive part which
        just returns the actual d ary recursive equation with SICTA and

        """
        pj = param.branchprob
        if not param.biased_split:
            pj = 1 / param.SPLIT
        d = param.SPLIT
        return n / self.recquaryrecursive(n, pj, d)

    def recquaryrecursive(self, n, pj, d):
        """
        THe actual recursive Equation from above
        """
        if n <= 1:
            return 1
        else:
            ln = 0
            for j in range(1, d + 1):
                l = 0
                for nj in range(0, n):
                    l += self.mycomb(n, nj) * (pj ** nj) * ((1 - pj) ** (n - nj)) * self.recquaryrecursive(nj, pj, d)
                ln += l
            ln = ln / ((1 - (pj ** n)) - ((d - 1) * (((1 - pj) / (d - 1)) ** n)))
            return ln

    # Recursive Equation from the SICTA paper
    def recsictarecursive(self, n, pj):
        """
        Actual Recursive Equation from below
        """
        if n <= 1:
            return 1
        else:
            ln = 0
            for i in range(0, n):
                ln += (self.binomialProb(n, i, pj) + self.binomialProb(n, n - i, pj)) * self.recsictarecursive(i, pj)
            den = 1 - (pj ** n) - ((1 - pj) ** n)
            ln = ln / den
            return ln

    def recsicta(self, n):
        """
        The Recursive equation from Giannakis and Yu paper
        """
        pj = 0.5
        return n / self.recsictarecursive(n, pj)

    # Recursive Equation from Capetanakis Paper
    def simpletreerecursive(self, n):
        """
        The actual recursive equation from the one below
        """
        if n <= 1:
            return 1
        else:
            k = 0
            for i in range(0, n):
                k += (self.mycomb(n, i) * (2 ** (-n))) * self.simpletreerecursive(i)
            return (1 + 2 * k) / (1 - (2 ** (-n + 1)))


    def simpletree(self, n):
        """
        The Original recursive Equation proposed by Capetanakis for a binary tree
        """
        return n / self.simpletreerecursive(n)

    # Bunch of Helpful Functions for better performance
    def binomialProb(self, n, i, pj):
        return self.mycomb(n, i) * (pj ** i) * ((1 - pj) ** (n - i))

    def mycomb(self, n, k):
        out = 1
        for i in range(0, k):
            out = out * (n - i) / (k - i)
        return out
