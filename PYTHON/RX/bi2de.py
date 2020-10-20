def bi2de(binary):
    x = 0
    for n in range(0, len(binary)):
        x = (binary[n]*(2**n)) + x
    return x


