function [bits_demod] = demodulate_symb(symb,MSC,Hinv)
bits_demod = [];
v = [-26:-22,-20:-8,-6:-1,1:6,8:20,22:26];
symb_fft = fftshift(fft(symb)).*Hinv;
symb_fft_48 = symb_fft(v+33);


if MSC == "BPSK"
    bits_demod = real(symb_fft_48)>0;
elseif MSC == "QPSK"
    for n = 1:48
        re = real(symb_fft_48(n));
        im = imag(symb_fft_48(n));
        if re > 0
            bits_demod = [bits_demod;1];
        else
            bits_demod = [bits_demod;0];
        end
        if im > 0
            bits_demod = [bits_demod;1];
        else
            bits_demod = [bits_demod;0];
        end
        
    end
elseif MSC == "16-QAM"
    p_21 = abs(real(symb_fft(33+-21)));
    p_7 = abs(real(symb_fft(33+-7)));
    p7 = abs(real(symb_fft(33+7)));
    p21 = abs(real(symb_fft(33+21)));
    pth = mean([p_21,p_7,p7,p21])/2;
    for n = 1:48
        re = real(symb_fft_48(n));
        im = imag(symb_fft_48(n));
        if re > 0
            if re > pth
                bits_demod = [bits_demod;1;0];
            else
                bits_demod = [bits_demod;1;1];
            end
        else
            if re < -pth
                bits_demod = [bits_demod;0;0];
            else
                bits_demod = [bits_demod;0;1];
            end
        end
        if im > 0
            if im > pth
                bits_demod = [bits_demod;1;0];
            else
                bits_demod = [bits_demod;1;1];
            end
        else
            if im < -pth
                bits_demod = [bits_demod;0;0];
            else
                bits_demod = [bits_demod;0;1];
            end
        end
    end
else
    p_21 = abs(real(symb_fft(33+-21)));
    p_7 = abs(real(symb_fft(33+-7)));
    p7 = abs(real(symb_fft(33+7)));
    p21 = abs(real(symb_fft(33+21)));
    pmax = mean([p_21,p_7,p7,p21]);
    pth1 = (2/7)*pmax;
    pth2 = (4/7)*pmax;
    pth3 = (6/7)*pmax;
    for n = 1:48
        re = real(symb_fft_48(n));
        im = imag(symb_fft_48(n));
        if re > 0
            if re > pth1
                if re > pth2
                    if re > pth3
                        bits_demod = [bits_demod;1;0;0];
                    else
                        bits_demod = [bits_demod;1;0;1];
                    end
                else
                    bits_demod = [bits_demod;1;1;1];
                end
            else
                bits_demod = [bits_demod;1;1;0];
            end
        else
            if re < -pth1
                if re < -pth2
                    if re <- pth3
                        bits_demod = [bits_demod;0;0;0];
                    else
                        bits_demod = [bits_demod;0;0;1];
                    end
                else
                    bits_demod = [bits_demod;0;1;1];
                end
            else
                bits_demod = [bits_demod;0;1;0];
            end
        end
        
        
        if im > 0
            if im > pth1
                if im > pth2
                    if im > pth3
                        bits_demod = [bits_demod;1;0;0];
                    else
                        bits_demod = [bits_demod;1;0;1];
                    end
                else
                    bits_demod = [bits_demod;1;1;1];
                end
            else
                bits_demod = [bits_demod;1;1;0];
            end
        else
            if im < -pth1
                if im < -pth2
                    if im <- pth3
                        bits_demod = [bits_demod;0;0;0];
                    else
                        bits_demod = [bits_demod;0;0;1];
                    end
                else
                    bits_demod = [bits_demod;0;1;1];
                end
            else
                bits_demod = [bits_demod;0;1;0];
            end
        end
    end
end



end