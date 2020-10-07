import numpy as np
from constants import w48, w96, w192, w288
w48 = np.array(w48).reshape(48)
w96 = np.array(w96).reshape(96)
w192 = np.array(w192).reshape(192)
w288 = np.array(w288).reshape(288)

a48 = [(w48[j]-1) for j in range(0,48)]
a96 = [(w96[j]-1) for j in range(0,96)]
a192 = [(w192[j]-1) for j in range(0,192)]
a288 = [(w288[j]-1) for j in range(0,288)]


def interleave_symbs(bits, NCBPS):
    bits_inter = np.zeros(NCBPS)    
    if NCBPS == 48:
        bits_inter = [bits[j] for j in a48]
    elif NCBPS == 96:
        bits_inter = [bits[j] for j in a96]
    elif NCBPS == 192:
        bits_inter = [bits[j] for j in a192]
    elif NCBPS == 288:
        bits_inter = [bits[j] for j in a288]

    return bits_inter
