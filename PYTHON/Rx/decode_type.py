import numpy as np

# The purpose of this function is to determine what the type and subtype of the packet is.
# currently only checks if packe is management type, and beacon subtype.
def decode_type(sub_type_field):
    # Check if field is beacon:
    # 00001000 is the first octet of the frame control field for beacon subtype packets (first two bits are clipped off)
    if np.array_equal(sub_type_field, [0,0,1,0,0,0]):
        packet_type = 'Beacon'
    elif np.array_equal(sub_type_field, [1,0,0,0,0,0]):
        packet_type = 'Data'
    else:
        packet_type = 'N/A'
    return packet_type
