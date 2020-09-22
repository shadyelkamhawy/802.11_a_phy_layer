function [sig,NCBPS,NDBPS] = sig_field(R,MSC,ppdu_length)
RATE = zeros(1,4);
if isequal(MSC,'BPSK')
    RATE(1:2) = [1;1];
    NDBPS = 24;
    NCBPS = 48;
elseif isequal(MSC,'QPSK')
    RATE(1:2) = [0;1];
    NDBPS = 48;
    NCBPS = 96;
elseif isequal(MSC,'16-QAM')
    RATE(1:2) = [1;0];
    NDBPS = 96;
    NCBPS = 192;
elseif isequal(MSC,'64-QAM')
    RATE(1:2) = [0;0];
    NDBPS = 192;
    NCBPS = 288;
end

if isequal(R,'1/2') 
    NDBPS = NDBPS*2*(1/2);
    RATE(3:4) = [0;1];
elseif isequal(R,'3/4')
    NDBPS = NDBPS*2*(3/4);
    RATE(3:4) = [1;1];
elseif isequal(R,'2/3')
    NDBPS = NDBPS*2*(2/3);
    RATE(3:4) = [0;1];
end
    
RES = 0; % reserved bit
LENGTH = de2bi(min(ppdu_length,(2^12)-1),12); % length bits in binary
PARITY = mod(sum([RATE,LENGTH]),2); % even parity
TAIL = zeros(1,6); % tail of 6 zeros
sig_bits = [RATE,RES,LENGTH,PARITY,TAIL]; % concatenate all 24 bits together

sig_bits_encoded = conv_enc(sig_bits,'1/2');
sig_bits_interleave = interleave_symbs(sig_bits_encoded,48);

sig_bits_modulated = 2*(sig_bits_interleave-(1/2)); % BPSK modulation

p_21 = 1; p_7 = 1; p7 = 1; p21 = -1;
sig_fft = zeros(64,1);

sig_fft(33+(-26:-22)) = sig_bits_modulated(1:5);
sig_fft(33+-21) = p_21;
sig_fft(33+(-20:-8)) = sig_bits_modulated(6:18);
sig_fft(33+-7) = p_7;
sig_fft(33+(-6:-1)) = sig_bits_modulated(19:24);
sig_fft(33+(1:6)) = sig_bits_modulated(25:30);
sig_fft(33+7) = p7;
sig_fft(33+(8:20)) = sig_bits_modulated(31:43);
sig_fft(33+21) = p21;
sig_fft(33+(22:26)) = sig_bits_modulated(44:48);

sig_symb = ifft(fftshift(sig_fft));
sig = [...
    sig_symb(49:64);... % cyclic prefix
    sig_symb;... % data
    ];

