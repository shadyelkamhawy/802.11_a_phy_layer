import numpy as np
import cmath as cm
# import matplotlib.pyplot as plt
from conv_enc import conv_enc
from interleave_symbs import interleave_symbs
from scrambler import scrambler
from pilot_generator import pilot_generator
from hex2bi import hex2bi
from modulate_symbs import modulate_symbs
from de2bi import de2bi


def transmit_packet(ppdu_length, code_rate, MSC, mac1, subtype): # ppdu_extra):
    # BPSK code rates = {1/2,3/4}
    # QPSK code rates = {1/2,3/4}
    # 16-QAM code rates = {1/2,3/4}
    # 64-QAM code rates = {2/3,3/4}
    ###########################################################################
    # SHORT TRAINING FIELD
    ###########################################################################
    sts_fft = np.zeros(64, dtype=complex)  # short training sequence in FFT domain 64 subcarriers
    sts_fft[32 + np.array([-24, -16, -4, 12, 16, 20, 24])] = cm.sqrt(13 / 6) * (1 + 1j) * np.ones(
        7)  # carriers -24, -16, -4, 12, 16, 20, 24 -> 1+1j
    sts_fft[32 + np.array([-20, -12, -8, 4, 8])] = -cm.sqrt(13 / 6) * (1 + 1j) * np.ones(
        5);  # carriers -20, -12, -8, 4, 8 -> -1-1j

    sts = np.fft.ifft((np.fft.fftshift(sts_fft)))  # inverse FFT to get 64 samples in time domain

    # NORMALIZE STS:
    sts = sts / np.sqrt(np.real(sum(sts * np.conjugate(sts))))

    stf = np.zeros(160, dtype=complex)
    stf[0:64] = sts
    stf[64:128] = sts
    stf[128:160] = sts[0:32]  # repeat the short training sequence 2.5 times -> 64 64 32 = 160
    # plt.plot(range(0,160),np.real(stf))

    # ###########################################################################
    # # LONG TRAINING FIELD
    # ###########################################################################

    lts_fft = np.array(
        [0, 0, 0, 0, 0, 0, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 0, 1,
         -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        dtype=complex)
    lts = np.fft.ifft(np.fft.fftshift(lts_fft));  # inverse FFT to get 64 samples in time domain
    # NORMALIZE LTS:
    lts = lts / np.sqrt(np.real(sum(lts * np.conjugate(lts))))
    ltf = np.zeros(160, dtype=complex)
    ltf[0:32] = lts[32:64]
    ltf[32:96] = lts
    ltf[96:160] = lts  # repeat the short training sequence 2.5 times -> 32 64 64 = 160
    # plt.plot(range(0,160),np.real(ltf))
    # ###########################################################################
    # # SIGNAL FIELD
    # ###########################################################################
    # ppdu_length = 2000; # payload length in Bytes < 2^12
    # code_rate = '3/4';
    # MSC = '64-QAM';
    RATE = np.zeros(4);

    if MSC == 'BPSK':
        RATE[0:2] = [1, 1]
        NDBPS = 24
        NCBPS = 48
        NBPSC = 1
    elif MSC == 'QPSK':
        RATE[0:2] = [0, 1]
        NDBPS = 48
        NCBPS = 96
        NBPSC = 2
    elif MSC == '16-QAM':
        RATE[0:2] = [1, 0]
        NDBPS = 96;
        NCBPS = 192;
        NBPSC = 4;
    elif MSC == '64-QAM':
        RATE[0:2] = [0, 0]
        NDBPS = 192
        NCBPS = 288
        NBPSC = 6

    if code_rate == '1/2':
        NDBPS = NDBPS * 2 * (1 / 2)
        RATE[2:4] = [0, 1]
    elif code_rate == '3/4':
        NDBPS = NDBPS * 2 * (3 / 4)
        RATE[2:4] = [1, 1]
    elif code_rate == '2/3':
        NDBPS = NDBPS * 2 * (2 / 3)
        RATE[2:4] = [0, 1]

    RES = np.zeros(1)  # reserved bit
    LENGTH = np.flip((np.array(de2bi(min(ppdu_length, (2 ** 12) - 1), 12))).T, 0)  # length bits in binary
    x = np.concatenate((RATE, LENGTH))
    PARITY = np.sum(x) % 2 * np.ones(1)  # even parity
    TAIL = np.zeros(6)  # tail of 6 zeros
    sig_bits = np.concatenate((RATE, RES, LENGTH, PARITY, TAIL))  # concatenate all 24 bits together

    # convolutional encoder
    sig_bits_encoded = conv_enc(sig_bits, '1/2')
    # interleaver
    # sig_bits_interleave = wlanBCCInterleave(sig_bits_encoded,'Non-HT',48);

    sig_bits_interleave = interleave_symbs(sig_bits_encoded, 48)

    sig_bits_modulated = 2 * (
                np.array(sig_bits_interleave).reshape(len(sig_bits_interleave)) - (1 / 2))  # BPSK modulation
    p_21 = 1
    p_7 = 1
    p7 = 1
    p21 = -1
    sig_fft = np.zeros(64)
    sig_fft[range(32 - 26, 32 - 22 + 1)] = sig_bits_modulated[0:5]
    sig_fft[32 + -21] = p_21
    sig_fft[range(32 - 20, 32 - 8 + 1)] = sig_bits_modulated[5:18]
    sig_fft[32 + -7] = p_7
    sig_fft[range(32 + -6, 32 - 1 + 1)] = sig_bits_modulated[18:24]
    sig_fft[range(32 + 1, 32 + 6 + 1)] = sig_bits_modulated[24:30]
    sig_fft[32 + 7] = p7
    sig_fft[range(32 + 8, 32 + 20 + 1)] = sig_bits_modulated[30:43]
    sig_fft[32 + 21] = p21
    sig_fft[range(32 + 22, 32 + 26 + 1)] = sig_bits_modulated[43:48]

    sig_symb = np.fft.ifft(np.fft.fftshift(sig_fft))
    # NORMALIZE:
    sig_symb = sig_symb / np.sqrt(np.real(sum(sig_symb * np.conjugate(sig_symb))))
    sig = np.concatenate((sig_symb[48:64], sig_symb))

    preamble = np.concatenate((stf, ltf, sig))

    # ###########################################################################
    # # PAYLAOD
    # ###########################################################################
    service_field = np.zeros(16)
    # preMAC = np.ones(8*4)
    # MAC1 = np.ones(12*4)
    # MAC2 = np.ones(12*4)
    # MAC3 = np.ones(12*4)

    # preMAC = transpose(hexToBinaryVector('08013000',8*4));
    # MAC1 = transpose(hexToBinaryVector('FFFFFFFFFFFF',12*4));
    # MAC2 = transpose(hexToBinaryVector('EEEEEEEEEEEE',12*4));
    # MAC3 = transpose(hexToBinaryVector('AAAAAAAAAAAA',12*4));

    if subtype == "Beacon":
        field = "08013000"  # [00 1000] management, beacon
    else:
        field = '20013000'  # [00 0000] data, data
    preMAC = hex2bi(field)  # Frame control field
    MAC1 = hex2bi(mac1)
    MAC2 = hex2bi('BEAC08BEAC08')
    MAC3 = hex2bi('BEAC07BEAC07')
    ppdu = np.zeros(8 * ppdu_length)
    ppdu_tail = np.zeros(6)

    Nsym = np.ceil((16 + (8 * 4) + (3 * 4 * 12) + 16 + (8 * ppdu_length) + 6) / NDBPS)
    Ndata = Nsym * NDBPS
    Npad = (Ndata - (16 + (8 * 4) + (3 * 4 * 12) + 16 + (8 * ppdu_length) + 6))

    bits_final = np.concatenate(
        (service_field, preMAC, MAC1, MAC2, MAC3, np.zeros(16), ppdu, ppdu_tail, np.zeros(int(Npad))))

    seed = 93
    scrambled_bits = scrambler(bits_final, seed)
    bits_encoded = conv_enc(scrambled_bits, code_rate)
    ppdu_samples = np.zeros(80 * int(Nsym), dtype=complex)
    pilot_polarity = pilot_generator(int(Nsym + 1))
    for n in range(1, int(Nsym)):
        m1 = int(((n - 1) * NCBPS))
        m2 = int(1 + NCBPS + ((n - 1) * NCBPS))
        symb_bits_encoded = [bits_encoded[m] for m in range(m1, m2)]
        bits_inter = interleave_symbs(symb_bits_encoded, NCBPS)
        iq_symb_fft = modulate_symbs(bits_inter, pilot_polarity[n], MSC)
        iq_symb = np.fft.ifft(np.fft.fftshift(iq_symb_fft))
        # NORMALIZE:
        iq_symb = iq_symb / np.sqrt(np.real(sum(iq_symb * np.conjugate(iq_symb))))

        cyclic_prefix = iq_symb[np.arange(48, 64)]
        iq_symb_80 = np.concatenate((cyclic_prefix, iq_symb))
        ppdu_samples[((n - 1) * 80) + np.arange(0, 80)] = iq_symb_80
        # cyclic prefix -> take last 16 samples put them at the front and add
        # to 64
        # concatenate in time domain

    s = np.concatenate((preamble, ppdu_samples))

    return s