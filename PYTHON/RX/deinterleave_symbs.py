import numpy as np
from TX.constants import k48, k96, k192, k288
k48 = np.array(k48).reshape(48)
k96 = np.array(k96).reshape(96)
k192 = np.array(k192).reshape(192)
k288 = np.array(k288).reshape(288)

a48 = [(k48[j]-1) for j in range(0, 48)]
a96 = [(k96[j]-1) for j in range(0, 96)]
a192 = [(k192[j]-1) for j in range(0, 192)]
a288 = [(k288[j]-1) for j in range(0, 288)]


# The purpose of this function is to reorder the message bits of the frame to their original sequence
def deinterleave_symbs(bits, msc):
    if msc == "BPSK":
        bits_deinter = [bits[j] for j in a48]
    elif msc == "QPSK":
        bits_deinter = [bits[j] for j in a96]
    elif msc == "16-QAM":
        bits_deinter = [bits[j] for j in a192]
    else:
        bits_deinter = [bits[j] for j in a288]

    return bits_deinter