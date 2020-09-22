function [bits_deinter] = deinterleave_symb(bits_demod,MSC)
global k48;
global k96;
global k192;
global k288;
if MSC == "BPSK"  
    bits_deinter = bits_demod(k48);
elseif MSC == "QPSK"
    bits_deinter = bits_demod(k96);
elseif MSC == "16-QAM"
    bits_deinter = bits_demod(k192);
else
    bits_deinter = bits_demod(k288);
end
end