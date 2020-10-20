import numpy as np


# The purpose of this function is to check that the SIG field values determined from sig_field_decoder() are valid
# such that they follow the correct format of the plcp described in the 802.11a - 1999 standard

def check_sig_field(rate, res, length, parity, tail):
    # convert each field to a numpy array:
    rate = np.array(rate)
    rate = rate.astype(int)
    length = np.array(length)
    length = length.astype(int)
    tail = np.array(tail)
    tail = tail.astype(int)

    null_tail = np.zeros((1, 6))

    valid = 0

    if res != 0:
        valid = 0
    elif tail is null_tail:
        valid = 0
    elif np.remainder((sum(rate) + sum(length) + parity), 2) != 0:
        valid = 0
    else:
        if np.array_equal(rate, np.array([1, 1, 0, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([1, 1, 1, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([0, 1, 0, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([0, 1, 1, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([1, 0, 0, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([1, 0, 1, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([0, 0, 0, 1])):
            valid = 1
        elif np.array_equal(rate, np.array([0, 0, 1, 1])):
            valid = 1
        else:
            valid = 0
    return valid
