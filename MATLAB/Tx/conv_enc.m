function [c] = conv_enc(bits,R)

N = length(bits);
A = zeros(N,1);
B = zeros(N,1);

T1 = 0;
T2 = 0;
T3 = 0;
T4 = 0;
T5 = 0;
T6 = 0;


c = zeros(2*N,1);
for n = 1:N
    % temporary storage of shift register states
    T1t = T1;
    T2t = T2;
    T3t = T3;
    T4t = T4;
    T5t = T5;
    A(n) = xor(bits(n),xor(xor(T2,T3),xor(T5,T6)));
    B(n) = xor(bits(n),xor(xor(T1,T2),xor(T3,T6)));
    
    % update shift registers
    T1 = bits(n);
    T2 = T1t;
    T3 = T2t;
    T4 = T3t;
    T5 = T4t;
    T6 = T5t;
    m = 1+(2*(n-1));
    c(m) = A(n);
    c(m+1) = B(n);
end

c = puncture_bits(c,R);
    