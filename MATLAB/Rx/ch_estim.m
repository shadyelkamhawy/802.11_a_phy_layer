%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CHANNEL ESTIMATION
% Perform channel estimation using the subcarriers of the LTF
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Hinv] = ch_estim(ltf)

global ltf_fft;
global lts_len;

% v = [-26:-1,1:26]; % locations of the valid subcarriers
% Hinv = ones(lts_len,1);


% subcarriers of L1
ltf_fft1 = fftshift(fft(ltf((lts_len/2)+(1:lts_len))));
% subcarriers of L2
ltf_fft2 = fftshift(fft(ltf((lts_len/2)+lts_len+(1:lts_len))));
% average of L1 and L2
ltf_fft_avg = (ltf_fft1+ltf_fft2)/2;
% estimation
% Hinv(v+33) = ltf_fft((lts_len/2)+1+v)./(ltf_fft_avg((lts_len/2)+1+v));
Hinv = ltf_fft./ltf_fft_avg;
