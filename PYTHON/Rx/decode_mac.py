import numpy as np
from binv2str import binv2str


def decode_mac(bitstream):
    bitstream = bitstream.tolist()

    m = 12 * 4
    m1 = 16 + 32 + np.arange(0, m)
    m2 = (max(m1)+1) + np.arange(0, m)
    m3 = (max(m2)+1) + np.arange(0, m)

    mac1_bin = bitstream[min(m1):(max(m1)+1)]
    mac1_bin_str = binv2str(mac1_bin)
    mac1 = "{0:0>4X}".format(int(mac1_bin_str, 2))

    mac2_bin = bitstream[min(m2):(max(m2)+1)]
    mac2_bin_str = binv2str(mac2_bin)
    mac2 = "{0:0>4X}".format(int(mac2_bin_str, 2))

    mac3_bin = bitstream[min(m3):(max(m3)+1)]
    mac3_bin_str = binv2str(mac3_bin)
    mac3 = "{0:0>4X}".format(int(mac3_bin_str, 2))

    return mac1, mac2, mac3
