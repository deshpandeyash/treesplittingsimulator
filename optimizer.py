import math

import numpy as np
from matplotlib import pyplot as plt
import tikzplotlib
import decimal
from scipy.special import comb
from scipy.stats import poisson
from math import factorial as fact

"""
For now its just a scratch pad to try different optimizer functions, nothing important in terms of the simulator. 
"""
# decimal.getcontext().prec = 1000

from scipy import stats
from operator import add
import matplotlib.pyplot as plt
import numpy as np


def DoubleSicta(n):  # This recursively implements Double SICTA
    if n <= 1:
        return (1)
    elif n == 2:
        return (2)
    else:
        splits = stats.multinomial.rvs(n, p)
        return (DoubleSicta(splits[0]) + DoubleSicta(splits[1]))


def SICTAtest(n):  # This is SICTA
    if n <= 1:
        return (1)
    else:
        splits = stats.multinomial.rvs(n, p)
        return (SICTAtest(splits[0]) + SICTAtest(splits[1]))


def STAtest(n):  # This is STA
    if n <= 1:
        return (1)
    else:
        splits = stats.multinomial.rvs(n, p)
        return (1 + STAtest(splits[0]) + STAtest(splits[1]))


n = 25000
p = [0.5, 0.5]
rate = 0.92419624074


def SteadyStateDelayDoubleSICTA(NumberOfSlots,
                                ArrivalRate):  # This simulates the Markov Chain, returns the average delay per packet
    ArrivalsNumbers = stats.poisson.rvs(ArrivalRate, 0, NumberOfSlots)
    counterOld = 0
    counterNew = 1
    packetslefttoserve = sum(ArrivalsNumbers)
    Delays = 0
    length = 0
    while packetslefttoserve > 0:
        numberofwaitingpackets = sum(ArrivalsNumbers[counterOld:counterNew])
        ServiceTime = DoubleSicta(numberofwaitingpackets)
        Delays += numberofwaitingpackets * ServiceTime
        length += 1
        counterOld = counterNew
        counterNew += ServiceTime
        packetslefttoserve -= numberofwaitingpackets
    return (Delays / NumberOfSlots)


def SteadyStateDelaySICTA(NumberOfSlots, ArrivalRate):
    ArrivalsNumbers = stats.poisson.rvs(ArrivalRate, 0, NumberOfSlots)
    counterOld = 0
    counterNew = 1
    packetslefttoserve = sum(ArrivalsNumbers)
    Delays = 0
    length = 0
    while packetslefttoserve > 0:
        numberofwaitingpackets = sum(ArrivalsNumbers[counterOld:counterNew])
        ServiceTime = SICTAtest(numberofwaitingpackets)
        Delays += numberofwaitingpackets * ServiceTime
        length += 1
        counterOld = counterNew
        counterNew += ServiceTime
        packetslefttoserve -= numberofwaitingpackets
    return (Delays / NumberOfSlots)


def SteadyStateDelaySTA(NumberOfSlots, ArrivalRate):
    ArrivalsNumbers = stats.poisson.rvs(ArrivalRate, 0, NumberOfSlots)
    counterOld = 0
    counterNew = 1
    packetslefttoserve = sum(ArrivalsNumbers)
    Delays = 0
    length = 0
    while packetslefttoserve > 0:
        numberofwaitingpackets = sum(ArrivalsNumbers[counterOld:counterNew])
        ServiceTime = STAtest(numberofwaitingpackets)
        Delays += numberofwaitingpackets * ServiceTime
        length += 1
        counterOld = counterNew
        counterNew += ServiceTime
        packetslefttoserve -= numberofwaitingpackets
    return (Delays / NumberOfSlots)


fine = 100  # This gives the number of data points for the graph
plt.plot(rate * 0.99, 40, "--")
NumberOfAverages = 25  # This gives the number of times we repeat the process, to end up with an average
Double = [0] * NumberOfAverages
Normal = [0] * NumberOfAverages
STA = [0] * NumberOfAverages
for i in range(NumberOfAverages):
    Double[i] = [SteadyStateDelayDoubleSICTA(n, rate * (x / fine)) for x in range(1, fine)]
    Normal[i] = [min(SteadyStateDelaySICTA(n, rate * (x / fine)), 40) for x in range(1, fine)]
    STA[i] = [min(SteadyStateDelaySTA(n, rate * (x / fine)), 40) for x in range(1, fine)]
dataDouble = [0] * (fine - 1)
dataNormal = [0] * (fine - 1)
dataSTA = [0] * (fine - 1)
# print(Double)
for j in range(
        fine - 1):  # This averages the datapoints of the different Markov chains, at each data point. I didn't know how to implement it nicer, as you have lists of lists
    x = [0] * NumberOfAverages
    x = [Double[i][j] for i in range(NumberOfAverages)]
    dataDouble[j] = sum(x) / NumberOfAverages

    y = [0] * NumberOfAverages
    y = [Normal[i][j] for i in range(NumberOfAverages)]
    dataNormal[j] = sum(y) / NumberOfAverages

    z = [0] * NumberOfAverages
    z = [STA[i][j] for i in range(NumberOfAverages)]
    dataSTA[j] = sum(z) / NumberOfAverages

xaxis = [x * rate / fine for x in range(1, fine)]
plt.plot(xaxis, dataDouble, color='red', label="ATIC")
maxi = max(dataDouble)
plt.plot(xaxis, dataNormal, color='green', label="SICTA")
temp_maxi = max(dataNormal)
if temp_maxi > maxi:
    maxi = temp_maxi
plt.plot(xaxis, dataSTA, color='blue',  label='STA')
temp_maxi = max(dataSTA)
if temp_maxi > maxi:
    maxi = temp_maxi
log_2 = 0.693
plt.vlines(4*log_2/3, 0, maxi,  linestyles='dashed', color='red')
plt.vlines(log_2, 0, maxi,  linestyles='dashed', color='green')
plt.vlines(log_2/2, 0, maxi, linestyles='dashed', color='blue')
# print(dataDouble)
# print(dataNormal)
# print(dataSTA)
plt.title("Delay Analysis")
tikzplotlib.save(F"Delay_Fig.tex")
plt.legend()
plt.grid()
plt.show()
