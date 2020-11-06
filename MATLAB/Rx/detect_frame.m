%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% returns a Nx2 matrix containing the index of the start of the packets in 
% the first column and the end of the packet in the second column. The
% input is a baseband complex signal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
function [loc, offset] = detect_frame(stf)
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FIND POTENTIAL PACKET START
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform autocorrelation to find a potential packet
% first 16 samples of STF
x1 = stf(2:sts_len);
% last 16 samples of STF
%x2 = stf(sts_len + (2:sts_len));
x2 = stf(9*sts_len + (2:sts_len));

% correlate to check if they match
c = cross_corr(x1,x2);
offset = 0;
if c > 0.90 % 90% correlation
    min_c = c;
    loc = 1;
    for i = 1:10
        x1 = stf((2:sts_len)+i);
        % last 16 samples of STF
        x2 = stf(i+(9*sts_len) + (2:sts_len));
        c = cross_corr(x1,x2);
        if c > min_c
            min_c = c;
            offset = i;
        end
    end
end