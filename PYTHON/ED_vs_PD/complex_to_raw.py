import struct


def complex_to_raw(filename, complex_list):
    complex_list_flat = []
    for n in range(0, len(complex_list)):
        complex_list_flat.append((complex_list[n]).real)
        complex_list_flat.append((complex_list[n]).imag)
    with open(filename, "wb") as f:
        for x in complex_list_flat:
            f.write(struct.pack('f', x))

