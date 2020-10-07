from depuncture_bits import depuncture_bits
from convdenc import convdenc
import numpy as np


def decode_symbs(bits_deinter, MSCn):
    bits_depunct = np.array(depuncture_bits(bits_deinter, MSCn))

    if MSCn == 0 or MSCn == 2 or MSCn == 4:
        bits_decode = convdenc(bits_depunct, '1/2')
    elif MSCn == 1 or MSCn == 3 or MSCn == 5 or MSCn == 7:
        bits_decode = convdenc(bits_depunct, '3/4')
    else:
        bits_decode = convdenc(bits_depunct, '2/3')

    return bits_decode

