
import numpy as np
import cmath as cm

def de2bi(n,N):
    bseed= bin(n).replace("0b", "")
    fix = N-len(bseed)
    pad = np.zeros(fix)
    pad=pad.tolist()
    y=[]         
    for i in range(len(pad)):
        y.append(int(pad[i]))  
    for i in range(len(bseed)):
        y.append(int(bseed[i]))
        
    return y
      

def  scrambler(bits,seed):
    #predict initial state
    # initialize scrambler
    # scramble
    
    bit_count = len(bits)
    scrambled_bits = np.zeros(bit_count)
    N=7
    bseed = de2bi(seed,N)
    x1 = bseed[0]
    x2 = bseed[1]
    x3 = bseed[2]
    x4 = bseed[3]
    x5 = bseed[4]
    x6 = bseed[5]
    x7 = bseed[6]   
    
    for n in range(bit_count):
        x1t = x1
        x2t = x2
        x3t = x3
        x4t = x4
        x5t = x5
        x6t = x6
        x7t = x7
        var = int(x4t)^int(x7t)
        scrambled_bits[n] =int(var)^int(bits[n])
        x1 = var
        x2 = x1t
        x3 = x2t
        x4 = x3t
        x5 = x4t
        x6 = x5t
        x7 = x6t
    return scrambled_bits