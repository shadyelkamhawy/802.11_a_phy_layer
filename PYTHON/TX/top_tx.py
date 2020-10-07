import numpy as np
import math as m
import constants as c


def top_tx(R, MSC, PPDU, FC, MAC1, MAC2, MAC3, TIME_STAMP):
    ltf_fft = c.ltf_fft
    stf_fft = c.stf_fft
    symb_len = c.symb_len

    ################################
    # PREAMBLE:
    ################################
    sts = np.fft.ifft(np.fft.fftshift(stf_fft))
    sts = np.array(sts)
    sts_norm = sts/np.sqrt(sts.T * sts)
    stf = [sts_norm, sts_norm, sts_norm[0:31+1]]

    lts = np.fft.ifft(np.fft.fftshift(ltf_fft))
    lts = np.array(lts)
    lts_norm = lts / np.sqrt(lts.T * lts)
    ltf = [lts_norm, lts_norm, lts_norm[0:31 + 1]]

    return

top_tx('1/2', '16-QAM', 2000, 2, 'BEAC0907', 'BEAC0907', 'BEAC0907', 1000)

