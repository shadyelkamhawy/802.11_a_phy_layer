import numpy as np


# The purpose of this function is to demodulate symbols into bits based on the information provided
# in the Signal Field of the frame
def demodulate_symbs(symbs, MSCn, hinvn):
    bits_demod = []
    v = [-26, -25, -24, -23, -22, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -6, -5, -4, -3, -2, -1,
         1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26]
    v = np.array(v) + 32
    symb_fft = np.fft.fftshift(np.fft.fft(symbs)) * hinvn
    symb_fft_48 = [symb_fft[j] for j in v]

    if MSCn == "BPSK":  # BPSK modulation
        bits_demod = []
        for n in range(0, 47 + 1):
            re = np.real(symb_fft_48[n])
            if re > 0:
                bits_demod = bits_demod + [1]
            else:
                bits_demod = bits_demod + [0]        
    elif MSCn == "QPSK":  # QPSK Modulation
        for n in range(0, 47 + 1):
            re = np.real(symb_fft_48[n])
            im = np.imag(symb_fft_48[n])
            if re > 0:
                bits_demod = bits_demod + [1]
            else:
                bits_demod = bits_demod + [0]
            if im > 0:
                bits_demod = bits_demod + [1]
            else:
                bits_demod = bits_demod + [0]
    elif MSCn == "16-QAM":  # 16-QAM
        p_21 = abs(np.real(symb_fft[32+-21]))
        p_7 = abs(np.real(symb_fft[32+-7]))
        p7 = abs(np.real(symb_fft[32+7]))
        p21 = abs(np.real(symb_fft[32+21]))
        pth = np.mean([p_21, p_7, p7, p21])/2
        
        for n in range(0, 47 + 1):
            re = np.real(symb_fft_48[n])
            im = np.imag(symb_fft_48[n])
            if re > 0:
                if re > pth:
                    bits_demod = bits_demod + [1, 0]
                else:
                    bits_demod = bits_demod + [1, 1]
            else:
                if re < -pth:
                    bits_demod = bits_demod + [0, 0]
                else:
                    bits_demod = bits_demod + [0, 1]
            if im > 0:
                if im > pth:
                    bits_demod = bits_demod + [1, 0]
                else:
                    bits_demod = bits_demod + [1, 1]
            else:
                if im < -pth:
                    bits_demod = bits_demod + [0, 0]
                else:
                    bits_demod = bits_demod + [0, 1]

    else:
        p_21 = abs(np.real(symb_fft[32 + -21]))
        p_7 = abs(np.real(symb_fft[32 + -7]))
        p7 = abs(np.real(symb_fft[32 + 7]))
        p21 = abs(np.real(symb_fft[32 + 21]))
        pmax = np.mean([p_21, p_7, p7, p21])
        pth1 = (2 / 7) * pmax
        pth2 = (4 / 7) * pmax
        pth3 = (6 / 7) * pmax
        for n in range(0, 47 + 1):
            re = np.real(symb_fft_48[n])
            im = np.imag(symb_fft_48[n])
            if re > 0:
                if re > pth1:
                    if re > pth2:
                        if re > pth3:
                            bits_demod = bits_demod + [1, 0, 0]
                        else:
                            bits_demod = bits_demod + [1, 0, 1]
                    else:
                        bits_demod = bits_demod + [1, 1, 1]
                else:
                    bits_demod = bits_demod + [1, 1, 0]

            else:
                if re < -pth1:
                    if re < -pth2:
                        if re < -pth3:
                            bits_demod = bits_demod + [0, 0, 0]
                        else:
                            bits_demod = bits_demod + [0, 0, 1]
                    else:
                        bits_demod = bits_demod + [0, 1, 1]
                else:
                    bits_demod = bits_demod + [0, 1, 0]

            if im > 0:
                if im > pth1:
                    if im > pth2:
                        if im > pth3:
                            bits_demod = bits_demod + [1, 0, 0]
                        else:
                            bits_demod = bits_demod + [1, 0, 1]
                    else:
                        bits_demod = bits_demod + [1, 1, 1]
                else:
                    bits_demod = bits_demod + [1, 1, 0]

            else:
                if im < -pth1:
                    if im < -pth2:
                        if im < -pth3:
                            bits_demod = bits_demod + [0, 0, 0]
                        else:
                            bits_demod = bits_demod + [0, 0, 1]
                    else:
                        bits_demod = bits_demod + [0, 1, 1]
                else:
                    bits_demod = bits_demod + [0, 1, 0]
    bits_demod = np.array(bits_demod)

    return bits_demod