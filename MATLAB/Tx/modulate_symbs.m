function iq_symb_fft_64 = modulate_symbs(bits_inter,pilot_polarity,MSC);



iq_symb_fft_64 = zeros(64,1);


bits_modulated = zeros(48,1);

% MODULATION

if isequal(MSC,'BPSK')
    p_21 = 1;
    p_7 = 1;
    p7 = 1;
    p21 = -1;
    for n = 1:1:48
        bits_modulated(n) = 2*(bits_inter(n)-(1/2));
    end
elseif isequal(MSC,'QPSK')
    p_21 = 1;
    p_7 = 1;
    p7 = 1;
    p21 = -1;
    m = 1;
    for n = 1:2:96
        bits_modulated(m) = (2*(bits_inter(n)-(1/2)))+(1i*(2*(bits_inter(n+1)-(1/2))));
        m = m + 1;
    end
elseif isequal(MSC,'16-QAM')
    p_21 = 3;
    p_7 = 3;
    p7 = 3;
    p21 = -3;
    m = 1;
    for n = 1:4:192
        if isequal(bits_inter(n+(0:1)),[0;0])
            bits_modulated(m) = -3;
        elseif isequal(bits_inter(n+(0:1)),[0;1])
            bits_modulated(m) = -1;
        elseif isequal(bits_inter(n+(0:1)),[1;1])
            bits_modulated(m) = 1;
        elseif isequal(bits_inter(n+(0:1)),[1;0])
            bits_modulated(m) = 3;
        end
        
        if isequal(bits_inter(n+(2:3)),[0;0])
            bits_modulated(m) = bits_modulated(m)+(1i*-3);
        elseif isequal(bits_inter(n+(2:3)),[0;1])
            bits_modulated(m) = bits_modulated(m)+(1i*-1);
        elseif isequal(bits_inter(n+(2:3)),[1;1])
            bits_modulated(m) = bits_modulated(m)+(1i*1);
        elseif isequal(bits_inter(n+(2:3)),[1;0])
            bits_modulated(m) = bits_modulated(m)+(1i*3);
        end
        m = m + 1;
    end
elseif isequal(MSC,'64-QAM')
    p_21 = 7;
    p_7 = 7;
    p7 = 7;
    p21 = -7;
    m = 1;
    for n = 1:6:288
        if isequal(bits_inter(n+(0:2)),[0;0;0])
            bits_modulated(m) = -7;
        elseif isequal(bits_inter(n+(0:2)),[0;0;1])
            bits_modulated(m) = -5;
        elseif isequal(bits_inter(n+(0:2)),[0;1;1])
            bits_modulated(m) = -3;
        elseif isequal(bits_inter(n+(0:2)),[0;1;0])
            bits_modulated(m) = -1;
        elseif isequal(bits_inter(n+(0:2)),[1;1;0])
            bits_modulated(m) = 1;
        elseif isequal(bits_inter(n+(0:2)),[1;1;1])
            bits_modulated(m) = 3;
        elseif isequal(bits_inter(n+(0:2)),[1;0;1])
            bits_modulated(m) = 5;
        elseif isequal(bits_inter(n+(0:2)),[1;0;0])
            bits_modulated(m) = 7;
        end
        
        if isequal(bits_inter(n+(3:5)),[0;0;0])
            bits_modulated(m) = bits_modulated(m)+(1i*-7);
        elseif isequal(bits_inter(n+(3:5)),[0;0;1])
            bits_modulated(m) = bits_modulated(m)+(1i*-5);
        elseif isequal(bits_inter(n+(3:5)),[0;1;1])
            bits_modulated(m) = bits_modulated(m)+(1i*-3);
        elseif isequal(bits_inter(n+(3:5)),[0;1;0])
            bits_modulated(m) = bits_modulated(m)+(1i*-1);
        elseif isequal(bits_inter(n+(3:5)),[1;1;0])
            bits_modulated(m) = bits_modulated(m)+(1i*1);
        elseif isequal(bits_inter(n+(3:5)),[1;1;1])
            bits_modulated(m) = bits_modulated(m)+(1i*3);
        elseif isequal(bits_inter(n+(3:5)),[1;0;1])
            bits_modulated(m) = bits_modulated(m)+(1i*5);
        elseif isequal(bits_inter(n+(3:5)),[1;0;0])
            bits_modulated(m) = bits_modulated(m)+(1i*7);
        end
        m = m + 1;
    end
end



iq_symb_fft_64(33+-21) = pilot_polarity*p_21;
iq_symb_fft_64(33+-7) = pilot_polarity*p_7;
iq_symb_fft_64(33+7) = pilot_polarity*p7;
iq_symb_fft_64(33+21) = pilot_polarity*p21;



iq_symb_fft_64(33+(-26:-22)) = bits_modulated(1:5);
iq_symb_fft_64(33+(-20:-8)) = bits_modulated(6:18);
iq_symb_fft_64(33+(-6:-1)) = bits_modulated(19:24);
iq_symb_fft_64(33+(1:6)) = bits_modulated(25:30);
iq_symb_fft_64(33+(8:20)) = bits_modulated(31:43);
iq_symb_fft_64(33+(22:26)) = bits_modulated(44:48);