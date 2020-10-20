import numpy as np
from RX import constants as c


# This function provides channel estimation based off the LTF
def ch_estim(s):
    ltf_fft = c.ltf_fft
    stf_len = c.stf_len
    lts_len = c.lts_len

    window_1_start = (lts_len // 2)  # start sample index offset by STF length plus 32
    window_1_end = window_1_start + lts_len  # start sample index offset by STF length plus LTF length plus SIG field length
    ltf = s[window_1_start:window_1_end]
    s_fft1 = np.fft.fft(ltf)
    s_fft1 = np.fft.fftshift(s_fft1)

    window_2_start = lts_len // 2 + lts_len
    window_2_end = window_2_start + lts_len  # start sample index offset by STF length plus 32 plus SIG field length plus 64
    s_fft2 = np.fft.fft(s[window_2_start:window_2_end])
    s_fft2 = np.fft.fftshift(s_fft2)

    s_fft = (s_fft1 + s_fft2) / 2

    hinv = ltf_fft / s_fft

    return hinv
