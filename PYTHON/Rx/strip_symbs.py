import constants as c


# The purpose of this function is to remove all preamble STF and LTF's from the frame leaving just the symbol
# for the purpose of decoding
def strip_symbs(complex_data, pkt_startn, m):
    stf_len = c.stf_len
    ltf_len = c.ltf_len
    cyc_prefix_len = c.cyc_prefix_len
    symb_len = c.symb_len
    sig_len = c.sig_len

    # Create offset window from packet start location by STF and LTF length plus signal length and cyclic prefix length
    # stripping away unnecessary data leaving only the symbols in the frame
    v_start = pkt_startn + stf_len + ltf_len + sig_len + cyc_prefix_len + ((m - 1) * (cyc_prefix_len + symb_len))
    v_end = v_start + symb_len

    start_index = v_start
    end_index = v_end

    symbs = complex_data[int(start_index):int(end_index)]
    return symbs
