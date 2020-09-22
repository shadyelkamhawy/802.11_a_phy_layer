function [descrambled_bits] = descrambler(bits)
    % predict initial state
    % initialize scrambler
    % scramble
    
    bit_count = length(bits(:));
    descrambled_bits = zeros(bit_count,1);
    
    x1 = xor(bits(1+6),bits(1+2));
    x2 = xor(bits(1+5),bits(1+1));
    x3 = xor(bits(1+4),bits(1+0));
    x4 = xor(xor(bits(1+3),bits(1+6)),bits(1+2));
    x5 = xor(xor(bits(1+2),bits(1+5)),bits(1+1));
    x6 = xor(xor(bits(1+1),bits(1+4)),bits(1+0));
    x7 = xor(bits(1+0),xor(xor(bits(1+3),bits(1+6)),bits(1+2)));
    
    for n = 1:bit_count
        x1t = x1;
        x2t = x2;
        x3t = x3;
        x4t = x4;
        x5t = x5;
        x6t = x6;
        x7t = x7;
        in = xor(x4t,x7t);
        descrambled_bits(n) = xor(in,bits(n));
        x1 = in;
        x2 = x1t;
        x3 = x2t;
        x4 = x3t;
        x5 = x4t;
        x6 = x5t;
        x7 = x6t;
    end
end