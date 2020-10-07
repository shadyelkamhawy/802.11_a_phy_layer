import numpy as np
import constants as c

def convdenc(codedin,R):
    xin = np.array(codedin)
    Nx = xin.size
    A = xin[0:Nx:2]
    B = xin[1:Nx:2]

    T1 = 0
    T2 = 0
    T3 = 0
    T4 = 0
    T5 = 0
    T6 = 0
    N = len(A)
    decodedout = np.zeros(N,dtype=int)
    for n in range(0,N):
        # temporary storage of shift register states
        T1t = T1
        T2t = T2
        T3t = T3
        T4t = T4
        T5t = T5

        if ((n+1)%3) != 0 or R=='1/2' or R == '2/3':
            # data prediction from A
            Acomp = (int(T2)^int(T3))^(int(T5)^int(T6))
           # print('hello')
            #print(n)
           # print('hello')
            An = A[n]
            if Acomp == 0:
               # print(An)
                decodedout[n] = An
            else:
                decodedout[n] = np.abs(An-1)
        else:
            # data prediction from B
            Bcomp = (int(T1)^int(T2))^(int(T3)^int(T6))
            Bn = B[n]
            if Bcomp == 0:
                decodedout[n] = Bn
            else:
                decodedout[n] = np.abs(Bn-1)

        # update shift registers
        T1 = decodedout[n]
        T2 = T1t
        T3 = T2t
        T4 = T3t
        T5 = T4t
        T6 = T5t

    return decodedout
