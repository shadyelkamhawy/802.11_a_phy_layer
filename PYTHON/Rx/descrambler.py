import numpy as np


# The Purpose of this function is to de-scramble the message bits after initially
# being scrambled on the transmitter side
def descrambler(bits):
    bit_count = len(bits)
    descrambled_bits = np.arange(0, bit_count) * 0
    bits = np.array(bits)
    bits = bits.astype(int)

    x1 = bits[6] ^ bits[2]
    x2 = bits[5] ^ bits[1]
    x3 = bits[4] ^ bits[0]
    x4 = (bits[3] ^ bits[6]) ^ bits[2]
    x5 = (bits[2] ^ bits[5]) ^ bits[1]
    x6 = (bits[1] ^ bits[4]) ^ bits[0]
    x7 = bits[0] ^ ((bits[3] ^ bits[6]) ^ bits[2])

    for n in range(0, bit_count):
        x1t = x1
        x2t = x2
        x3t = x3
        x4t = x4
        x5t = x5
        x6t = x6
        x7t = x7
        in_bits = x4t ^ x7t
        in_bits = int(in_bits)
        descrambled_bits[n] = in_bits ^ bits[n]
        x1 = in_bits
        x2 = x1t
        x3 = x2t
        x4 = x3t
        x5 = x4t
        x6 = x5t
        x7 = x6t

    return descrambled_bits



