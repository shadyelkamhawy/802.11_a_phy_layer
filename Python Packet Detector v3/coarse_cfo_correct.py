import constants as c
import numpy as np


# The purpose of this function is to perform coarse correction to mitigate carrier frequency offset
def coarse_cfo_correct(complex_data):
    # Load constants:
    sts_len = c.sts_len
    stf_len = c.stf_len
    length = stf_len - sts_len
    v = np.arange(0, length)
    # For packet determine frequency offset and correct signal by applying complex offset
    # Calculate frequency offset, df:
    df_0 = (1 / sts_len)
    v_1 = np.array(v)
    v_2 = v_1 + sts_len
    df_1 = [complex_data[i] for i in v_1]
    df_2 = [complex_data[i] for i in v_2]
    df_2 = np.conj(df_2)
    df = df_0 * np.angle(np.sum(df_1 * df_2))  # df is the Coarse frequency offset
    return df
