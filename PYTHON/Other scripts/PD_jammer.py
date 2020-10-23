import numpy as np
from TX import top_tx

# Sample Rate:
# Minimum Back off time:
# Maximum Payload Length:
# Minimum Payload Length:

min_backoff = int(10)
min_ppdu = int(750)
TXOP = 1000  # in samples
number_of_packets = 10

complex_data = top_tx.top_tx("1/2", "BPSK", 2000, "08013000", "BEAC09BEAC09", "BEAC08BEAC08", "BEAC07BEAC07", 1000)
complex_data = np.array(complex_data, dtype=complex)

for n in range(0, number_of_packets):
    single_packet = top_tx.top_tx("3/4", "64-QAM", min_ppdu, "08013000", "BEAC09BEAC09", "BEAC08BEAC08", "BEAC07BEAC07", 1000)
    complex_data = np.concatenate((complex_data, np.zeros(min_backoff, dtype=complex), np.array(single_packet, dtype=complex)))

np.concatenate((np.zeros(1000, dtype=complex), complex_data, np.zeros(TXOP, dtype=complex)))