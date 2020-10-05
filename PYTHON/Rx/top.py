from raw_to_complex import raw_to_complex
from detect_frames import detect_frames
from coarse_cfo_correct import coarse_cfo_correct
from ch_estim import ch_estim
from sig_field_decoder import sig_field_decoder
from check_sig_field import check_sig_field
import math as ma
import numpy as np
import constants as c
from msc_code_rate import msc_code_rate
from bi2de import bi2de
from demodulate_symbs import demodulate_symbs
from deinterleave_symbs import deinterleave_symbs
from viterbi_decoder import viterbi_decoder
from descrambler import descrambler
from decode_mac import decode_mac
from decode_type import decode_type


# This program is a post-processing receiver which takes raw data in the form of a sampled waveform and extracts frame
# information for the purpose of capturing wifi packets.
# Based off of the 802.11a - 1999 standards

stf_len = c.stf_len
sts_len = c.sts_len
ltf_len = c.ltf_len
cyc_prefix_len = c.cyc_prefix_len
symb_len = c.symb_len
sig_len = c.sig_len
G1 = c.G1
G2 = c.G2

bin_file = "../Bins/Receivetest.bin"
fraction = 1
complex_data = raw_to_complex(bin_file, fraction)
# Append 1000 zeros at front and back to pad complex data:
complex_data = np.concatenate((np.zeros(1000, dtype=complex), complex_data, np.zeros(1000, dtype=complex)))


PPDU_LENGTH = []
R = []
PKT_START = []
MSC = []
MAC1 = []
MAC2 = []
MAC3 = []
PKT_TYPE = []
NUMDBPS = []
data_len = len(complex_data)
loc = 0
n = 0
while(n <= data_len):
    if (n-1 + stf_len - 1) <= data_len:
        stf_start_window = n - 1
        stf_end_window = n - 1 + stf_len
        stf = complex_data[stf_start_window:stf_end_window]
        loc = detect_frames(stf)
        if loc == 1:
            df = coarse_cfo_correct(stf)
            if (n - 1 + stf_len + ltf_len) <= data_len:
                v_start = (n + stf_len)
                v_end = v_start + ltf_len
                v = np.arange(v_start, v_end)
                v = v.astype(int)
                ev = 1j * df * v
                ev = np.exp(ev)
                ltf = complex_data[min(v)-1:max(v)] * ev
                Hinv = ch_estim(ltf)
                if (n - 1 + stf_len + ltf_len + cyc_prefix_len + symb_len) <= data_len:
                    v_start = n - 1 + stf_len + ltf_len + cyc_prefix_len + 1
                    v_end = v_start + symb_len
                    v = np.arange(v_start, v_end)
                    v = v.astype(int)
                    ev = v * 1j * df
                    sig = np.exp(ev)
                    sig = sig * complex_data[int(v_start) - 1:int(v_end)-1]
                    rate, res, length, parity, tail = sig_field_decoder(sig, Hinv)
                    valid = check_sig_field(rate, res, length, parity, tail)
                    if valid:
                        msc, r, numDBPS = msc_code_rate(rate)
                        ppdu_length = bi2de(length)
                        PPDU_LENGTH = PPDU_LENGTH + [ppdu_length]
                        MSC = MSC + [msc]
                        R = R + [r]
                        NUMDBPS = NUMDBPS + [numDBPS]
                        PKT_START = PKT_START + [n]
                        mac1 = "000000000000"
                        mac2 = "000000000000"
                        mac3 = "000000000000"
                        pkt_type = "N/A"
                        mmax = ma.ceil(216 / numDBPS)
                        if (n - 1 + stf_len + ltf_len + sig_len + cyc_prefix_len + (
                                (mmax - 1) * (cyc_prefix_len + symb_len)) + symb_len) <= data_len:
                            bits_deinter = np.zeros(mmax*216)
                            for l in range(1, mmax+1):
                                v_start = int(n - 1 + stf_len + ltf_len + sig_len + cyc_prefix_len + ((l-1) * (cyc_prefix_len + symb_len)) + 1)
                                v_end = int(v_start + symb_len)
                                v = np.arange(v_start, v_end)
                                symb = v * 1j * df
                                symb = np.exp(symb)
                                symb = symb * complex_data[v_start-1:v_end-1]
                                bits_demod = demodulate_symbs(symb, msc, Hinv)
                                bits_deinter[(l-1) * 192: l * 192] = deinterleave_symbs(bits_demod, msc)
                            ppdu_scrambled = viterbi_decoder(bits_deinter, G1, G2, r)
                            ppdu_scrambled = ppdu_scrambled[0, :]
                            ppdu = descrambler(ppdu_scrambled)
                            mac1, mac2, mac3 = decode_mac(ppdu)
                            pkt_type = decode_type(ppdu[18 + np.arange(0, 6)])
                        PKT_TYPE = PKT_TYPE + [pkt_type]
                        MAC1 = MAC1 + [mac1]
                        MAC2 = MAC2 + [mac2]
                        MAC3 = MAC3 + [mac3]
                n = n + 160 + 160 + 80
    n = n + 1

top_row = ["Start Sample", "Payload length", "Bit Rate", "Modulation", "Code Rate", "MAC1", "MAC2", "MAC3", "Packet Type"]
top_row = np.array(top_row)
data = []
data.append([PKT_START, PPDU_LENGTH, NUMDBPS, MSC, R, MAC1, MAC2, MAC3, PKT_TYPE])
data = np.array(data)
data = data[0,:,:]
data = data.T

packet_data = np.vstack((top_row, data))
np.savetxt("Packet_Data.csv", packet_data, delimiter=",", fmt="%s")

