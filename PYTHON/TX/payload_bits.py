import numpy as np
from hex2bi import hex2bi
from de2bi import de2bi


def payload_bits(FC,MAC1,MAC2,MAC3,TIME_STAMP,NDBPS,ppdu_length):
    service_field = np.zeros(16)
    preMAC = np.transpose(hex2bi(FC))
    preMAC = np.append(np.zeros(32 - len(preMAC)), preMAC)
    MAC1b = np.transpose(hex2bi(MAC1))
    MAC1b = np.append(np.zeros(48-len(MAC1b)), MAC1b)
    MAC2b = np.transpose(hex2bi(MAC2))
    MAC2b = np.append(np.zeros(48 - len(MAC2b)), MAC2b)
    MAC3b = np.transpose(hex2bi(MAC3))
    MAC3b = np.append(np.zeros(48 - len(MAC3b)), MAC3b)
    ppdu = np.zeros(8*ppdu_length)
    ppdu_tail = np.zeros(6)
    
    Nsym = np.ceil((16+(8*4)+(3*4*12)+16+(8*ppdu_length)+6)/NDBPS)
    Ndata = Nsym*NDBPS
    Npad = Ndata - (16+(8*4)+(3*4*12)+16+(8*ppdu_length)+6)
    
    ppdu[0:12] = de2bi(TIME_STAMP, 12)

    MACSb = np.append(np.append(MAC1b, MAC2b), MAC3b)

    bits_final = np.append(np.append(np.append(np.append(np.append(np.append(service_field, preMAC), MACSb), np.zeros(16)), ppdu), ppdu_tail), np.zeros(int(Npad)))

    return bits_final, Nsym