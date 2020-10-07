import numpy as np
import math

def cross_cor(x1, x2):
    x1 = np.array(x1)
    x2 = np.array(x2)
    p1 = np.real(np.dot(np.conj(np.transpose(x1)), x1))
    p2 = np.real(np.dot(np.conj(np.transpose(x2)), x2))
    # print(p1)
    # print(p2)

    if p1 == 0 or p2 == 0:
        correlation = 0
    else:
        correlation = (np.abs(np.dot(np.conj(np.transpose(x1)), x2) / math.sqrt(p1 * p2)))

    return correlation
