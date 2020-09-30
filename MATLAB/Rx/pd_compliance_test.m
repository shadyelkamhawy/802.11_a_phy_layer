% read signal from bin file
clear;
DUT_MAC = '';
file_name = "./bins/receive16QAM12.bin";
fraction = 1;
complex_data = raw_to_complex(file_name,fraction);
complex_data = [zeros(1000,1);complex_data;zeros(1000,1)];
T1 = 36*20;
[...
    PKT_START,PKT_END,...
    MSC,R,...
    PPDU_LENGTH,...
    PKT_TYPE,...
    MAC1,MAC2,MAC3,...
    TIME_STAMP...
    ] = top_rx(complex_data);

pkt_count = length(PKT_START);
test = 0;
fail = 0;
pass = 0;
fail_data = [];
for n = 1:(pkt_count-2)
    if isequal(PKT_TYPE(n),'BEACON') && isequal(MAC1(n),'BEAC09BAC09') && isequal(MAC2(n),'BEAC08BEAC08') % start of test
        T2 = T1+400+(20*TIME_STAMP(n)*8/6)+(20*16); % silent duration after beacon end in samples
        if PKT_START(n+1) - PKT_END(n) <= T1 % found small preamble
            if isequal(MAC2(n+2),DUT_MAC)
                % valid test
                test = test + 1;
                if PKT_START(n+2) < (PKT_END(n) + T2)
                    % fail
                    fail = fail + 1;
                    fail_data = [fail_data;n+2,T2,1,PKT_START(n+2)-PKT_END(n)]
                else
                    % pass
                    pass = pass + 1;
                end
            end
        else
            if isequal(MAC2(n+1),DUT_MAC)
                % valid test
                test = test + 1;
                if PKT_START(n+1) < (PKT_END(n) + T2)
                    % fail
                    fail = fail + 1;
                    fail_data = [fail_data;n+2,T2,0,PKT_START(n+1)-PKT_END(n)]
                else
                    % pass
                    pass = pass + 1;
                end
            end
        end
    end
end