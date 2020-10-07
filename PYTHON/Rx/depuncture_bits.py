import numpy as np


def depuncture_bits(bits_deinter, R):
    bits_depunct = []
    N = len(bits_deinter)
    if R == "1/2":
        bits_depunct = bits_deinter
    elif R == "3/4":
        n = 1
        while 1:
            if (n+1) <= N:
                bits_depunct = [bits_depunct] + bits_deinter[n:(n+1)]
            else:
                break

            if n+2 <= N:
                bits_depunct = [bits_depunct] + bits_deinter[n:(n + 2)] + [0]
            else:
                break

            if n+3 <= N:
                bits_depunct = [bits_depunct] + bits_deinter[n:(n + 3)]
            else:
                break
            n = n + 4
    else:
        bits_depunct = []
        n = 1
        while 1:
            if (n+1) <= N:
                bits_depunct = [bits_depunct] + bits_deinter[n:(n+1)]
            else:
                break

            if (n+2) <= N:
                bits_depunct = [bits_depunct] + bits_deinter[n+2] + [0]
            else:
                break
            n = n + 3

    return bits_depunct

