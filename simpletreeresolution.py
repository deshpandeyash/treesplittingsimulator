import numpy as np
from simparam import SimParam
import time




def oneslotprocess(arrival_array, printit=False):
    success = 0
    arrival_array = np.sort(arrival_array)
    if printit:
        print(arrival_array)
    if len(arrival_array) == 0:
        if printit:
            print("No Tx")
    elif len(active_array) == 1 and active_array[0] == 0:
        arrival_array = np.delete(arrival_array, 0)
        success = 1
        if printit:
            print("Success without waiting")
    elif arrival_array[0] == 0 and arrival_array[1] != 0:
        arrival_array = arrival_array - 1
        arrival_array = np.delete(arrival_array, 0)
        success = 1
        if printit:
            print("Success")
    elif arrival_array[0] != 0:
        arrival_array = arrival_array - 1
        if printit:
            print("Idle")
    elif arrival_array[0] == 0 and arrival_array[1] == 0:
        if printit:
            print("collision")
        for i in range(0, len(arrival_array)):
            if arrival_array[i] == 0:
                arrival_array[i] = arrival_array[i] + np.random.binomial(1, 0.5)
            else:
                arrival_array[i] = arrival_array[i] + 1
    else:
        print("Error, unexpected array")
    return arrival_array, success


sim = SimParam()
np.random.seed(sim.seed)
active_array = np.zeros(0, dtype=int)
total_arrivals = 0
total_successes = 0
for _ in range(0, sim.runs):
    packets_gen = np.random.poisson(sim.lmbda)
    total_arrivals = total_arrivals + packets_gen
    new_packets = np.zeros(packets_gen, dtype=int)
    active_array = np.concatenate((active_array, new_packets))
    active_array, result = oneslotprocess(active_array, printit=False)
    total_successes = total_successes + result
print("Throughput = " + str(total_successes/total_arrivals))




