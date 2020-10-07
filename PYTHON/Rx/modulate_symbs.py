import numpy as np


def modulate_symbs(bits_inter,pilot_polarity,MSC):
    iq_symb_fft_64 = np.zeros(64,dtype=complex)
    bits_modulated = np.zeros(48,dtype=complex)

    if MSC == 'BPSK':
        p_21 = 1
        p_7 = 1
        p7 = 1
        p21 = -1
        for n in range(0,48,1):
            bits_modulated[n] = 2*(bits_inter[n]-(1/2))
    
    elif MSC == 'QPSK':
        p_21 = 1
        p_7 = 1
        p7 = 1
        p21 = -1
        m = 0
        for n in range(0,96,2):
            bits_modulated[m] = (2*(bits_inter[n]-(1/2)))+(1j*(2*(bits_inter[n+1]-(1/2))))
            m = m + 1
    
    elif MSC == '16-QAM':
        p_21 = 3
        p_7 = 3
        p7 = 3
        p21 = -3
        m = 0
        for n in range(0, 192, 4):
            if np.array_equal(bits_inter[n:(n+2)], [0, 0]):   # bits_inter[n+np.array([0,1])]==[0,0]:
                bits_modulated[m] = -3
            elif np.array_equal((bits_inter[n:(n+2)]), [0, 1]): 
                bits_modulated[m] = -1
            elif np.array_equal((bits_inter[n:(n+2)]), [1, 1]): 
                bits_modulated[m] = 1
            elif np.array_equal((bits_inter[n:(n+2)]), [1, 0]): 
                bits_modulated[m] = 3

            if np.array_equal((bits_inter[(n+2):(n+4)]), [0, 0]):
                bits_modulated[m] = bits_modulated[m]+(1j*-3)
            elif np.array_equal((bits_inter[(n+2):(n+4)]), [0, 1]):
                bits_modulated[m] = bits_modulated[m]+(1j*-1)
            elif np.array_equal((bits_inter[(n+2):(n+4)]), [1, 1]):
                bits_modulated[m] = bits_modulated[m]+(1j*1)
            elif np.array_equal((bits_inter[(n+2):(n+4)]), [1, 0]):
                bits_modulated[m] = bits_modulated[m]+(1j*3)
            
            m = m + 1

    elif MSC == '64-QAM':
        p_21 = 7
        p_7 = 7
        p7 = 7
        p21 = -7
        m = 0
        for  n in range( 0,288,6) :             
            if np.array_equal(bits_inter[n:(n+3)], [0, 0,0]): 
                bits_modulated[m] = -7
            elif np.array_equal(bits_inter[n:(n+3)], [0, 0,1]): 
                bits_modulated[m] = -5
            elif np.array_equal(bits_inter[n:(n+3)], [0, 1,1]): 
                bits_modulated[m] = -3
            elif np.array_equal(bits_inter[n:(n+3)], [0, 1,0]): 
                bits_modulated[m] = -1
            elif np.array_equal(bits_inter[n:(n+3)], [1, 1,0]): 
                bits_modulated[m] = 1
            elif np.array_equal(bits_inter[n:(n+3)], [1, 1,1]): 
                bits_modulated[m] = 3
            elif np.array_equal(bits_inter[n:(n+3)], [1, 0,1]): 
                bits_modulated[m] = 5
            elif np.array_equal(bits_inter[n:(n+3)], [1, 0,0]): 
                bits_modulated[m] = 7

            if np.array_equal(bits_inter[(n+3):(n+6)], [0, 0,0]): 
                bits_modulated[m] = bits_modulated[m]+(1j*-7)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [0, 0,1]): 
                bits_modulated[m] = bits_modulated[m]+(1j*-5)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [0, 1,1]): 
                bits_modulated[m] = bits_modulated[m]+(1j*-3)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [0, 1,0]): 
                bits_modulated[m] = bits_modulated[m]+(1j*-1)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [1, 1,0]): 
                bits_modulated[m] = bits_modulated[m]+(1j*1)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [1, 1,1]): 
                bits_modulated[m] = bits_modulated[m]+(1j*3)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [1, 0,1]): 
                bits_modulated[m] = bits_modulated[m]+(1j*5)
            elif np.array_equal(bits_inter[(n+3):(n+6)], [1, 0,0]): 
                bits_modulated[m] = bits_modulated[m]+(1j*7)
            m = m + 1

    iq_symb_fft_64[32-21] = pilot_polarity*p_21
    iq_symb_fft_64[32-7] = pilot_polarity*p_7
    iq_symb_fft_64[32+7] = pilot_polarity*p7
    iq_symb_fft_64[32+21] = pilot_polarity*p21

    iq_symb_fft_64[32+ np.arange(-26,-21)] = bits_modulated[np.arange(0,5)]
    iq_symb_fft_64[32+np.arange(-20,-7)] = bits_modulated[np.arange(5,18)]
    iq_symb_fft_64[32+np.arange(-6,0)] = bits_modulated[np.arange(18,24)]
    iq_symb_fft_64[32+np.arange(1,7)] = bits_modulated[np.arange(24,30)]
    iq_symb_fft_64[32+np.arange(8,21)] = bits_modulated[np.arange(30,43)]
    iq_symb_fft_64[32+np.arange(22,27)] = bits_modulated[np.arange(43,48)]

    return iq_symb_fft_64

