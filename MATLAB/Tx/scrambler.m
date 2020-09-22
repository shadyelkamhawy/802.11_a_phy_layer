function [scrambled_bits] = scrambler(bits,seed)
    % predict initial state
    % initialize scrambler
    % scramble
    
    bit_count = length(bits(:));
    scrambled_bits = zeros(bit_count,1);
    
    bseed = de2bi(seed,7);
    x1 = bseed(1);
    x2 = bseed(2);
    x3 = bseed(3);
    x4 = bseed(4);
    x5 = bseed(5);
    x6 = bseed(6);
    x7 = bseed(7);
    
    for n = 1:bit_count
        x1t = x1;
        x2t = x2;
        x3t = x3;
        x4t = x4;
        x5t = x5;
        x6t = x6;
        x7t = x7;
        in = xor(x4t,x7t);
        scrambled_bits(n) = xor(in,bits(n));
        x1 = in;
        x2 = x1t;
        x3 = x2t;
        x4 = x3t;
        x5 = x4t;
        x6 = x5t;
        x7 = x6t;
    end
end