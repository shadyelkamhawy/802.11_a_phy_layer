
import numpy as np
import cmath as cm


def conv_enc(bits, code_rate):
    
    N = len(bits)
    A = np.zeros(N)
    B = np.zeros(N)
    T1 = 0
    T2 = 0
    T3 = 0
    T4 = 0
    T5 = 0
    T6 = 0
    c = []
    for n  in range(N):
    # temporary storage of shift register states
        T1t = T1
        T2t = T2
        T3t = T3
        T4t = T4
        T5t = T5
        A[n] = int(bits[n])^ ((int(T2)^int(T3)) ^ (int(T5)^int(T6)))
        B[n]= int(bits[n])^ ((int(T1)^int(T2)) ^ (int(T3)^int(T6)))  # update shift registers
        T1 = bits[n];
        T2 = T1t
        T3 = T2t
        T4 = T3t
        T5 = T4t
        T6 = T5t


    if code_rate == '1/2':
        for n  in range(0,N):
            c.append(A[n])
            c.append(B[n])
           # c=[c,A[n],B[n]]
    elif code_rate=='2/3':
        for  n in range(0,N):
            if (n+1)%2 == 1:
                c.append(A[n])
                c.append(B[n])
            else:
               c.append( A[n])
        
    else:
        c.append( A[0])
        c.append(B[0])
        for n in range(1, N, 3):
            c.append( A[n])
            if (n+2) <= N:
                c.append( B[n+1])
                if (n+3) <= N:
                  c.append(A[n+2])
                  c.append(B[n+2])
    return  c
    

    
    
    
    
    
    
    
  


