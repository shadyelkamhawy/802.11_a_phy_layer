import numpy as np
from RX import constants as c
from RX import viterbi_decoder

# The purpose of this function is to decode the SIG Field of the frame to determine packet parameters:
# Bit Rate and Code Rate (from rate field of PLCP), Payload length (from length field of PLCP)
# and checking packet validity.
def sig_field_decoder(sig, hinv):
    k48 = np.array(c.k48)-1

    rate = np.zeros((1, 4))
    length = np.zeros((1, 12))
    tail = np.zeros((1, 6))

    stf_len = c.stf_len
    ltf_len = c.ltf_len
    cyc_len = c.cyc_prefix_len
    symb_len = c.symb_len
    G1 = c.G1
    G2 = c.G2

    m_start = stf_len + ltf_len + cyc_len  # STF length + LTF length + cyclic prefix length
    m_start = int(m_start)

    m_end = stf_len + ltf_len + cyc_len + symb_len  # STF length + LTF length + cyclic prefix length + symbol length
    m_end = int(m_end)

    v = [-26, -25, -24, -23, -22, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26]
    v = np.array(v)  # center frequencies of sub-carriers

    sig_fft = np.fft.fftshift(np.fft.fft(sig))
    sig_fft = sig_fft * hinv

    sig_48 = np.real(sig_fft[32 + v])  # 32 = symb_len/2
    sig_48_bits = np.zeros((48, 1))

    for m in range(0, 48):  # Decode SIG field using BPSK (>1 gives 1, <1 gives 0)
        if sig_48[m] > 0:
            sig_48_bits[m] = 1
        else:
            sig_48_bits[m] = 0

    sig_48_deinter = sig_48_bits[k48]  # deinterleave bits
    decodedout = viterbi_decoder.viterbi_decoder(sig_48_deinter, G1, G2, '1/2')  # decode bits
    # PUT ARRAY INTO SINGLE ARRAY!!!!!!!!!!!!!
    # separate decoded bits into their respective fields
    decoded_bits = np.zeros(len(decodedout[0, :]))
    for i in range(0, len(decodedout[0, :])):
        decoded_bits[i] = decodedout[0, i]

    rate = decoded_bits[0:4]
    res = decoded_bits[4]
    length = decoded_bits[5:17]
    parity = decoded_bits[17]
    tail = decoded_bits[18:24]
    return rate, res, length, parity, tail
