function [bits_punct] = puncture_bits(bits_inter,R)

N = length(bits_inter);
if R == "1/2"
    bits_punct = bits_inter;
elseif R=="3/4"
    bits_punct = [];
    n = 1;
    while 1
        if (n+1) <= N
            bits_punct = [bits_punct;bits_inter(n:(n+1))];
        else
            break;
        end
        
        if (n+2) <= N
            bits_punct = [bits_punct;bits_inter(n+2)];
        else
            break;
        end
        
        if (n+5) <= N
            bits_punct = [bits_punct;bits_inter(n+5)];
        else
            break;
        end
        n = n + 6;
    end
else
    bits_punct = [];
    n = 1;
    while 1
        if (n+1) <= N
            bits_punct = [bits_punct;bits_inter(n:(n+1))];
        else
            break;
        end
        
        if (n+2) <= N
            bits_punct = [bits_punct;bits_inter(n+2)];
        else
            break;
        end
        n = n + 4;
    end
end