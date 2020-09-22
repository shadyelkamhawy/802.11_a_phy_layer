%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Coarse Carrier Frequency Offset Correction
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [df] = coarse_cfo_correct(stf)
    global sts_len;
    global stf_len;
    
    len = (stf_len-sts_len);
    v = 1:len;
    
    % calculate frequency offset
    df = (1/sts_len)*angle(sum(stf(v).*conj(stf(sts_len+v))));
end