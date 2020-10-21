import numpy as np
from TX import top_tx
from RX import top_rx

complex_data = top_tx.top_tx("3/4", "QPSK", 2000, "08013000", "BEAC09BEAC09", "BEAC08BEAC08", "BEAC07BEAC07", 1000)
packet_data = top_rx.top_rx(complex_data)
np.savetxt("QPSK34_data.csv", packet_data, delimiter=",", fmt="%s")
