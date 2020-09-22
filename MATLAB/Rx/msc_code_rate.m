function [MSC,R,numDBPS] = msc_code_rate(rate)
    if sum(rate(1:2) == [1 1]) == 2
        MSC = 'BPSK';
        if sum(rate(3:4) == [0 1]) == 2
            R = '1/2';
            numDBPS = 24;
        else
            R = '3/4';
            numDBPS = 36;
        end
    elseif sum(rate(1:2) == [0 1]) == 2
        MSC = 'QPSK';
        if sum(rate(3:4) == [0 1]) == 2
            R = '1/2';
            numDBPS = 48;
        else
            R = '3/4';
            numDBPS = 72;
        end
    elseif sum(rate(1:2) == [1 0]) == 2
        MSC = '16-QAM';
        if sum(rate(3:4) == [0 1]) == 2
            R = '1/2';
            numDBPS = 96;
        else
            R = '3/4';
            numDBPS = 144;
        end
    else
        MSC = '64-QAM';
        if sum(rate(3:4) == [0 1]) == 2
            R = '2/3';
            numDBPS = 192;
        else
            R = '3/4';
            numDBPS = 216;
        end
    end
end
