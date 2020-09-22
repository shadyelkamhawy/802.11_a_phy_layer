function [bits_depunct] = depuncture_bits(bits_deinter,R)

N = length(bits_deinter);
if R == "1/2"
    bits_depunct = bits_deinter;
elseif R=="3/4"
    bits_depunct = [];
    n = 1;
    while 1
        if (n+1) <= N
            bits_depunct = [bits_depunct;bits_deinter(n:(n+1))];
        else
            break;
        end
        
        if (n+2) <= N
            bits_depunct = [bits_depunct;bits_deinter(n+2);0];
        else
            break;
        end
        
        if (n+3) <= N
            bits_depunct = [bits_depunct;0;bits_deinter(n+3)];
        else
            break;
        end
        n = n + 4;
    end
else
    bits_depunct = [];
    n = 1;
    while 1
        if (n+1) <= N
            bits_depunct = [bits_depunct;bits_deinter(n:(n+1))];
        else
            break;
        end
        
        if (n+2) <= N
            bits_depunct = [bits_depunct;bits_deinter(n+2);0];
        else
            break;
        end
        n = n + 3;
    end
end