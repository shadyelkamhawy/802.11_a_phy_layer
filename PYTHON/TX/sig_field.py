import numpy as np
from TX import de2bi
from TX import conv_enc
from TX import interleave_symbs


def sig_field(R, MSC, ppdu_length):
    RATE = np.zeros(4)
    if MSC == 'BPSK':
        RATE[0:2] = [1, 1]
        NDBPS = 24
        NCBPS = 48
    elif MSC == 'QPSK':
        RATE[0:2] = [0, 1]
        NDBPS = 48
        NCBPS = 96
    elif MSC == '16-QAM':
        RATE[0:2] = [1, 0]
        NDBPS = 96
        NCBPS = 192
    elif MSC =='64-QAM':
        RATE[0:2] = [0, 0]
        NDBPS = 192
        NCBPS = 288
    
    
    if R == '1/2':
        NDBPS = NDBPS*2*(1/2)
        RATE[2:4] = [0, 1]
    elif R == '3/4':
        NDBPS = NDBPS*2*(3/4)
        RATE[2:4] = [1, 1]
    elif R == '2/3':
        NDBPS = NDBPS*2*(2/3)
        RATE[2:4] = [0, 1]

    RES = 0  # reserved bit
    LENGTH = de2bi.de2bi(min(ppdu_length, (2**12)-1), 12)  # length bits in binary
    LENGTH = np.array(LENGTH)
    PARITY = np.mod(sum(np.append(RATE, LENGTH)), 2) # even parity
    TAIL = np.zeros(6)  # tail of 6 zeros
    sig_bits = np.append(np.append(np.append(np.append(RATE, [RES]), LENGTH), [PARITY]), TAIL)  # concatenate all 24 bits together
    
    sig_bits_encoded = conv_enc.conv_enc(sig_bits, '1/2')
    sig_bits_interleave = interleave_symbs.interleave_symbs(sig_bits_encoded, 48)
    sig_bits_interleave = np.array(sig_bits_interleave)
    
    sig_bits_modulated = 2*(sig_bits_interleave-0.5)  # BPSK modulation
    
    p_21 = 1
    p_7 = 1
    p7 = 1
    p21 = -1
    sig_fft = np.zeros(64)
    
    sig_fft[(33+(-27)):(33 + (-22))] = sig_bits_modulated[0:5]
    sig_fft[33+(-22)] = p_21
    sig_fft[(33+(-21)):33+(-8)] = sig_bits_modulated[5:18]
    sig_fft[33+(-8)] = p_7
    sig_fft[(33+(-7)):(33 + (-1))] = sig_bits_modulated[18:24]
    sig_fft[(33+0):(33 + 6)] = sig_bits_modulated[24:30]
    sig_fft[33+6] = p7
    sig_fft[(33+7):(33+20)] = sig_bits_modulated[30:43]
    sig_fft[33+20] = p21
    sig_fft[(33+21):(33+26)] = sig_bits_modulated[43:48]
    
    sig_symb = np.fft.ifft(np.fft.fftshift(sig_fft))
    sig = np.append(sig_symb[48:64], sig_symb)
    
    return sig, NCBPS, NDBPS
