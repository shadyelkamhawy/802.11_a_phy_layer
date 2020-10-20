import constants as c
import numpy as np
import cross_cor


# The purpose of this function is to determine the start and end samples of each frame by scanning the complex data
# for the STF of each frame and recording the index of each starting and ending sample
def detect_frames(stf):
    # CONSTANTS:
    # short training sequence length
    sts_len = c.sts_len
    # short training field length
    stf_len = c.stf_len
    symb_len = c.symb_len
    stf_fft = c.stf_fft

    x1 = stf[1:sts_len]
    x2_start = stf_len - sts_len + 1
    x2_end = x2_start + sts_len
    x2 = stf[x2_start:x2_end]

    # Perform correlation:
    correlation = cross_cor.cross_cor(x1, x2)
    # print(correlation)
    loc = 0
    if correlation > 0.90:
        x = np.fft.fft(stf[0:symb_len])
        x = np.fft.fftshift(x)

        # perform secondary correlation:
        correlation_2 = cross_cor.cross_cor(x, stf_fft)
        if correlation_2 > 0.7:
            loc = 1

    return loc