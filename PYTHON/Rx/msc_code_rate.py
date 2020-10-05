import numpy as np


def msc_code_rate(rate):
    rate = np.array(rate)
    rate = rate.astype(int)

    if np.array_equal(rate[0:2], [1, 1]):
        MSC = 'BPSK'
        if np.array_equal(rate[2:4], [0, 1]):
            R = '1/2'
            numDBPS = 24
        else:
            R = '3/4'
            numDBPS = 36

    elif np.array_equal(rate[0:2], [0, 1]):
        MSC = 'QPSK'
        if np.array_equal(rate[2:4], [0, 1]):
            R = '1/2'
            numDBPS = 48
        else:
            R = '3/4'
            numDBPS = 72
        
    elif np.array_equal(rate[0:2], [1, 0]):
        MSC = '16-QAM'
        if np.array_equal(rate[2:4], [0, 1]):
            R = '1/2'
            numDBPS = 96
        else:
            R = '3/4'
            numDBPS = 144
        
    else:
        MSC = '64-QAM'
        if np.array_equal(rate[2:4] == [0, 1]):
            R = '2/3'
            numDBPS = 192
        else:
            R = '3/4'
            numDBPS = 216

    return MSC, R, numDBPS