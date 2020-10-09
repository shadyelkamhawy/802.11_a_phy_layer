import numpy as np
import constants as c
from sig_field import sig_field
from payload_bits import payload_bits
from scrambler import scrambler
from conv_enc import conv_enc
from pilot_generator import pilot_generator
from interleave_symbs import interleave_symbs
from modulate_symbs import modulate_symbs


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
    ltf = np.append(ltf, lts_norm)

    sig, NCBPS, NDBPS = sig_field(R, MSC, PPDU_length)
    sig = sig/np.sqrt(np.dot(np.conjugate(np.transpose(sig)), sig))
    preamble = np.append(stf, np.append(ltf, sig))


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
    ppdu_samples = ppdu_samples + 0j

    # pilot polarity for symbols:
    pilot_polarity = pilot_generator(int(Nsym + 1))

    for n in range(1, int(Nsym)+1):
        bits_inter = interleave_symbs(bits_encoded[((n-1) * NCBPS) + 0: ((n-1) * NCBPS) + NCBPS], NCBPS)
        iq_symb_fft = modulate_symbs(bits_inter, pilot_polarity[n], MSC)
        iq_symb = np.fft.ifft(np.fft.fftshift(iq_symb_fft))
        iq_symb_norm = iq_symb/np.sqrt(np.dot(np.conjugate(np.transpose(iq_symb)), iq_symb))
        cyclic_prefix = iq_symb_norm[48:64]
        iq_symb_80 = np.append(cyclic_prefix, iq_symb_norm)
        ppdu_samples[((n-1)*(len(cyclic_prefix)+symb_len)+0):(n-1)*(len(cyclic_prefix)+symb_len)+(len(cyclic_prefix)+symb_len)] = iq_symb_80
        temp = 0

    s = np.append(preamble, ppdu_samples)
    return s

signal = top_tx('1/2', '16-QAM', 2000, '0800', 'BEAC0907', 'BEAC0907', 'BEAC0907', 1000)

