function [bits_inter] = interleave_symbs(bits,NCBPS)
global w48;
global w96;
global w192;
global w288;
if NCBPS == 48
    bits_inter = bits(w48);
elseif NCBPS == 96
    bits_inter = bits(w96);
elseif NCBPS == 192
    bits_inter = bits(w192);
elseif NCBPS == 288
    bits_inter = bits(w288);
end
end