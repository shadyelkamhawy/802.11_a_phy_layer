import math as ma
import numpy as np
from RX import detect_frames
from RX import coarse_cfo_correct
from RX import ch_estim
from RX import sig_field_decoder
from RX import check_sig_field
from RX import constants as c
from RX import msc_code_rate
from RX import bi2de
from RX import demodulate_symbs
from RX import deinterleave_symbs
from RX import viterbi_decoder
from RX import descrambler
from RX import decode_mac
from RX import decode_type
from RX import depuncture_bits
from RX import normalize



# This program is a post-processing receiver which takes raw data in the form of a sampled waveform and extracts frame
# information for the purpose of capturing wifi packets.
# Based off of the 802.11a - 1999 standards
def top_rx(complex_data):
    stf_len = c.stf_len
    sts_len = c.sts_len
    ltf_len = c.ltf_len
    cyc_prefix_len = c.cyc_prefix_len
    symb_len = c.symb_len
    sig_len = c.sig_len
    G1 = c.G1
    G2 = c.G2

    # Append 1000 zeros at front and back to pad complex data:
    complex_data = np.concatenate((np.zeros(1000, dtype=complex), complex_data, np.zeros(1000, dtype=complex)))


    PPDU_LENGTH = []
    R = []
    PKT_START = []
    PKT_END = []
    MSC = []
    MAC1 = []
    MAC2 = []
    MAC3 = []
    PKT_TYPE = []
    NUMDBPS = []
    data_len = len(complex_data)
    loc = 0
    n = 0
    while n <= data_len:
        if (n-1 + stf_len - 1) <= data_len:
            stf_start_window = n - 1
            stf_end_window = n - 1 + stf_len
            stf = complex_data[stf_start_window:stf_end_window]
            loc = detect_frames.detect_frames(stf)
            if loc == 1:
                df = coarse_cfo_correct.coarse_cfo_correct(stf)
                if (n - 1 + stf_len + ltf_len) <= data_len:
                    v_start = (n + stf_len)
                    v_end = v_start + ltf_len
                    v = np.arange(v_start, v_end)
                    v = v.astype(int)
                    ev = 1j * df * v
                    ev = np.exp(ev)
                    ltf = complex_data[min(v)-1:max(v)] * ev
                    Hinv = ch_estim.ch_estim(ltf)
                    if (n - 1 + stf_len + ltf_len + cyc_prefix_len + symb_len) <= data_len:
                        v_start = n - 1 + stf_len + ltf_len + cyc_prefix_len + 1
                        v_end = v_start + symb_len
                        v = np.arange(v_start, v_end)
                        v = v.astype(int)
                        ev = v * 1j * df
                        sig = np.exp(ev)
                        sig = sig * complex_data[int(v_start) - 1:int(v_end)-1]
                        rate, res, length, parity, tail = sig_field_decoder.sig_field_decoder(sig, Hinv)
                        valid = check_sig_field.check_sig_field(rate, res, length, parity, tail)
                        if valid:
                            msc, r, numDBPS = msc_code_rate.msc_code_rate(rate)
                            ppdu_length = bi2de.bi2de(length)
                            PPDU_LENGTH = PPDU_LENGTH + [ppdu_length]
                            MSC = MSC + [msc]
                            R = R + [r]
                            NUMDBPS = NUMDBPS + [numDBPS]
                            PKT_START = PKT_START + [n]
                            # Packet End:
                            pkt_samples_len = stf_len + ltf_len + cyc_prefix_len + symb_len + (ppdu_length*8*numDBPS*80)
                            noise_power = sum((normalize.normalize(complex_data[n-64:n-64+63]))**2)
                            for k in range(min((data_len - symb_len), n+pkt_samples_len), data_len - symb_len + 1):
                                x_power = sum((normalize.normalize(complex_data[k:k+63]))**2)
                                if x_power <= 1.1*noise_power:
                                    pkt_end = k
                                    break
                            PKT_END = PKT_END + [pkt_end]
                            mac1 = "000000000000"
                            mac2 = "000000000000"
                            mac3 = "000000000000"
                            pkt_type = "N/A"
                            mmax = ma.ceil(220 / numDBPS)
                            if (n - 1 + stf_len + ltf_len + sig_len + cyc_prefix_len + (
                                    (mmax - 1) * (cyc_prefix_len + symb_len)) + symb_len) <= data_len:
                                bits_deinter = []
                                for l in range(1, mmax+1):
                                    v_start = int(n - 1 + stf_len + ltf_len + sig_len + cyc_prefix_len + ((l-1) * (cyc_prefix_len + symb_len)) + 1)
                                    v_end = int(v_start + symb_len)
                                    v = np.arange(v_start, v_end)
                                    symb = v * 1j * df
                                    symb = np.exp(symb)
                                    symb = symb * complex_data[v_start-1:v_end-1]
                                    bits_demod = demodulate_symbs.demodulate_symbs(symb, msc, Hinv)
                                    bits_deinter = bits_deinter + deinterleave_symbs.deinterleave_symbs(bits_demod, msc)
                                bits_depunct = depuncture_bits.depuncture_bits(bits_deinter, r)
                                ppdu_scrambled = viterbi_decoder.viterbi_decoder(bits_depunct, G1, G2, r)
                                ppdu_scrambled = ppdu_scrambled[0, :]
                                ppdu = descrambler.descrambler(ppdu_scrambled)
                                mac1, mac2, mac3 = decode_mac.decode_mac(ppdu)
                                pkt_type = decode_type.decode_type(ppdu[18 + np.arange(0, 6)])
                            PKT_TYPE = PKT_TYPE + [pkt_type]
                            MAC1 = MAC1 + [mac1]
                            MAC2 = MAC2 + [mac2]
                            MAC3 = MAC3 + [mac3]
                    n = n + 160 + 160 + 80
        n = n + 1

    top_row = ["Start Sample", "End Sample", "Payload length", "Bit Rate", "Modulation", "Code Rate", "MAC1", "MAC2", "MAC3", "Packet Type"]
    top_row = np.array(top_row)
    data = []
    data.append([PKT_START, PKT_END, PPDU_LENGTH, NUMDBPS, MSC, R, MAC1, MAC2, MAC3, PKT_TYPE])
    data = np.array(data)
    data = data[0,:,:]
    data = data.T

    packet_data = np.vstack((top_row, data))
    return packet_data


