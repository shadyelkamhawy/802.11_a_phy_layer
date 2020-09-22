%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SIGNAL FIELD DECODER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [rate,res,length,parity,tail] = sig_field_decoder(sig,Hinv)
% symbol length
global symb_len;
symb_len = 64;
% deinterleaving vector for signal field
global k48;
% Polynomials for the Viterbi decoder
global G1;
global G2;

rate = zeros(1,4);
res = zeros(1,1);
length = zeros(1,12);
parity = zeros(1,1);
tail = zeros(1,6);

v = [-26:-22,-20:-8,-6:-1,1:6,8:20,22:26]; % locations of data subcarriers

sig_field_fft = fftshift(fft(sig)).*Hinv; % apply channel estimation
sig_48 = real(sig_field_fft(v+1+(symb_len/2))); % extract data subcarriers
sig_48_bits = sig_48 > 0; % BPSK demodulation
sig_48_bits_deinter = sig_48_bits(k48);

% use viterbi decoder with code rate 1/2
decodedout = viterbi_decoder(sig_48_bits_deinter,G1,G2,'1/2');
rate = decodedout(1+(0:3));
res = decodedout(1+4);
length = decodedout(1+5+(0:11));
parity = decodedout(1+5+11+1);
tail = decodedout(1+5+11+1+1+(0:5));

end
