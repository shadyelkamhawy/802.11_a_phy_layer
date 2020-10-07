import numpy as np
import math as m
import constants as c
from sig_field import sig_field
from payload_bits import payload_bits
from scrambler import scrambler
from conv_enc import conv_enc
from pilot_generator import pilot_generator
from interleave_symbs import interleave_symbs


def top_tx(R, MSC, PPDU_length, FC, MAC1, MAC2, MAC3, TIME_STAMP):
    ltf_fft = c.ltf_fft
    stf_fft = c.stf_fft
    symb_len = c.symb_len

    ################################
    # PREAMBLE:
    ################################
    sts = np.fft.ifft(np.fft.fftshift(stf_fft))
    sts_norm = sts/np.sqrt(np.dot(np.conjugate(np.transpose(sts)), sts))
    sts_norm = np.array(sts_norm)
    stf = np.append(sts_norm, sts_norm)
    stf = np.append(stf, sts_norm[0:31+1])

    lts = np.fft.ifft(np.fft.fftshift(ltf_fft))
    lts_norm = lts / np.sqrt(np.dot(np.conjugate(np.transpose(lts)), lts))
    lts_norm = np.array(lts_norm)
    ltf = np.append(lts_norm[32:63+1], lts_norm)
    ltf = np.append(ltf, sts_norm[32:63 + 1])

    sig, NCBPS, NDBPS = sig_field(R, MSC, PPDU_length)

    ##################################
    # PAYLOAD
    ##################################
    bits_final, Nsym = payload_bits(FC, MAC1, MAC2, MAC3, TIME_STAMP, NDBPS, PPDU_length)
    # scramble:
    seed = 93
    scrambled_bits = scrambler(bits_final, seed)

    # encode:
    bits_encoded = conv_enc(scrambled_bits, R)

    # samples for symbols
    ppdu_samples = np.zeros(int(80*Nsym))

    # pilot polarity for symbols:
    pilot_polarity = pilot_generator(int(Nsym + 1))

    for n in range(0, int(Nsym)):
        bits_inter = interleave_symbs(bits_encoded[(n * NCBPS) + 0: (n * NCBPS) + NCBPS], NCBPS)
        temp = 0
    return

top_tx('1/2', '16-QAM', 2000, '8000', 'BEAC0907', 'BEAC0907', 'BEAC0907', 1000)

