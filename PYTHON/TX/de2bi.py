import numpy as np


def de2bi(n, N):
    bseed= bin(n).replace("0b", "")
    fix = N-len(bseed)
    pad = np.zeros(fix)
    pad = pad.tolist()
    y = []
    for i in range(len(pad)):
        y = [int(pad[i])] + y
    for i in range(len(bseed)):
        y = [int(bseed[i])] + y
    return y