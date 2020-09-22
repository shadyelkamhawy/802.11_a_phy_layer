function [valid] = check_sig_field(rate,res,length,parity,tail)

if res ~= 0 % check reserved bit is set to zero
    valid = 0;
elseif tail ~= zeros(1,6) % check tail is 6 zeros
    valid = 0;
elseif rem(sum([rate,length,parity]),2) ~= 0 % even parity check
    valid = 0;
else
    if sum(rate == [1 1 0 1]) == 4
        valid = 1;
    elseif sum(rate == [1 1 1 1]) == 4
        valid = 1;
    elseif sum(rate == [0 1 0 1]) == 4
        valid = 1;
    elseif sum(rate == [0 1 1 1]) == 4
        valid = 1;
    elseif sum(rate == [1 0 0 1]) == 4
        valid = 1;
    elseif sum(rate == [1 0 1 1]) == 4
        valid = 1;
    elseif sum(rate == [0 0 0 1]) == 4
        valid = 1;
    elseif sum(rate == [0 0 1 1]) == 4
        valid = 1;
    else
        valid = 0;
    end
end