
def hex2bi(hex_str):
    bin_int=[]
    for n in range(len(hex_str)):
        bin_str = format(int(hex_str[n], 16), "04b")
        for i in range(len(bin_str)):
            if bin_str[i]=='1':
                bin_int.append(1)
            else:
                bin_int.append(0)    
    return bin_int