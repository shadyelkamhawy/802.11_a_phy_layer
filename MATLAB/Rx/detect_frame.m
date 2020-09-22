%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% returns a Nx2 matrix containing the index of the start of the packets in 
% the first column and the end of the packet in the second column. The
% input is a baseband complex signal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
function [loc] = detect_frame(stf)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CONSTANTS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% short training sequence length
global sts_len;
% total short training field length
global stf_len;
% symbol length
global symb_len; 
% FFT of the STF
global stf_fft;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INITIALIZATIONS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
loc = 0;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FIND POTENTIAL PACKET START
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform autocorrelation to find a potential packet
% first 16 samples of STF
x1 = stf(2:sts_len);
% last 16 samples of STF
x2 = stf(stf_len-sts_len+(2:sts_len));
% correlate to check if they match
c = cross_corr(x1,x2);
if c > 0.90 % 90% correlation
    x = fftshift(fft(stf(1:symb_len))); % first 64 samples of STF
    c = cross_corr(x,stf_fft); % cross correlation with ideal STF FFT
    if c > 0.7 % above 70% correlation
        loc = 1; % found packet
    end
end