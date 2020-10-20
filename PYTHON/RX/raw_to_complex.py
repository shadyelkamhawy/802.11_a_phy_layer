import numpy as np
import math


# Purpose of this function is to extract the raw data from the .bin file specified in "top.py"
# Binary data in pairs of rows, even rows contain in phase data, odd rows contain quadrature data, 1 sample is 2 rows
# Returns Complex Data as np.array list
def raw_to_complex(file_name, fraction):
    file = open(file_name, "rb")
    data = np.fromfile(file, '<f4')
    file.close()
    inphase_data = data[0:len(data):2]  # Extract just in phase data
    quadrature_data = data[1:len(data):2]  # Extract just quadrature data
    data_length = math.floor(fraction*min(len(inphase_data), len(quadrature_data)))
    complex_data = inphase_data[0:data_length] + (1j*quadrature_data[0:data_length])  # Combine components into complex data
    complex_data = complex_data/max(abs(complex_data))  # Normalize data
    complex_data = np.array(complex_data)
    return complex_data
