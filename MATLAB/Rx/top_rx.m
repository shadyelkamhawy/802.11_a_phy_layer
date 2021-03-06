
function [...
    PKT_START,PKT_END,...
    MSC,R,...
    PPDU_LENGTH,...
    PKT_TYPE,...
    MAC1,MAC2,MAC3,...
    TIME_STAMP...
    ] = top_rx(complex_data)
constants;
global stf_len;
global ltf_len;
global cyc_prefix_len;
global symb_len;
global sig_len;
global G1;
global G2;
data_length = length(complex_data);
PKT_START = [];
PKT_END = [];
MSC = [];
R = [];
PPDU_LENGTH = [];
PKT_TYPE = [];
MAC1 = [];
MAC2 = [];
MAC3 = [];
TIME_STAMP = [];
n = 1;
while n <= data_length
    if (n-1+stf_len+10) <= data_length
        stf = complex_data(n-1+(1:(10+stf_len)));
        [loc, offset] = detect_frame(stf);
        n = n + offset;
        if loc
            df = coarse_cfo_correct(stf);
            if (n-1+stf_len+ ltf_len) <= data_length
                v = (n-1+stf_len+(1:ltf_len));
                ltf = exp(1j*df*v(:)).*complex_data(v);
                Hinv = ch_estim(ltf);
                if (n-1+stf_len+ltf_len+cyc_prefix_len+ symb_len) <= data_length
                    v = (n-1+stf_len+ltf_len+cyc_prefix_len+(1:symb_len));
                    sig = exp(1j*df*v(:)).*complex_data(v);
                    [rate,res,LENGTH,parity,tail] = sig_field_decoder(sig,Hinv);
                    valid = check_sig_field(rate,res,LENGTH,parity,tail);
                    if valid
                        [msc,r,numDBPS] = msc_code_rate(rate);
                        ppdu_length = bi2de(LENGTH);
                        pkt_samples_len = stf_len + ltf_len + cyc_prefix_len+ symb_len + (ppdu_length*8*numDBPS*80);
                        noise_power = (norm(complex_data(n-64 + (0:63))))^2;
                        for m = (min((data_length-symb_len),n+pkt_samples_len)):(data_length-symb_len)
                            x_power = (norm(complex_data(m + (0:63))))^2;
                            if x_power <= 1.1*noise_power
                                pkt_end = m;
                                break;
                            end
                        end
                        
                        PPDU_LENGTH = [PPDU_LENGTH;ppdu_length];
                        R = [R;r];
                        PKT_START = [PKT_START;n];
                        PKT_END = [PKT_END;pkt_end];
                        % PKT_END = [PKT_END;pkt_end];
                        
                        mac1 = "000000000000";
                        mac2 = "000000000000";
                        mac3 = "000000000000";
                        pkt_type = "N/A";
                        
                        mmax = ceil(232/numDBPS);
                        if (n-1 + stf_len+ltf_len + sig_len + cyc_prefix_len + ((mmax-1)*(cyc_prefix_len+symb_len)) + symb_len) <= data_length
                            bits_deinter = [];
                            for m = 1:mmax
                                v = n-1 + stf_len+ltf_len + sig_len + cyc_prefix_len + ((m-1)*(cyc_prefix_len+symb_len)) + (1:symb_len);
                                symb = exp(1j*df*v(:)).*complex_data(v);
                                bits_demod = demodulate_symb(symb,msc,Hinv);
                                bits_deinter = [bits_deinter;deinterleave_symb(bits_demod,msc)];
                            end
                            bits_depunct = depuncture_bits(bits_deinter,R);
                            ppdu_scrambled = viterbi_decoder(bits_depunct,G1,G2,r);
                            ppdu = descrambler(ppdu_scrambled);
                            [pkt_type,mac1,mac2,mac3,time_stamp] = packet_info(ppdu);
                        end
                        PKT_TYPE = [PKT_TYPE;pkt_type];
                        MAC1 = [MAC1;mac1];
                        MAC2 = [MAC2;mac2];
                        MAC3 = [MAC3;mac3];
                        TIME_STAMP = [TIME_STAMP,time_stamp];
                    end
                end
            end
            n = n + stf_len + ltf_len + sig_len;
        end
    end
    n = n + 1;
end
end