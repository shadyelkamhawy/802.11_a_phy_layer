% read signal from bin file
clear;

%file_name = "./bins/receive16QAM12.bin";
file_name = "test1.bin";

fraction = 1;
complex_data = raw_to_complex(file_name,fraction);
complex_data = [zeros(1000,1);complex_data;zeros(1000,1)];

[PKT_START,...PKT_END,...
    MSC,R,...
    PPDU_LENGTH,...
    PKT_TYPE,...
    MAC1,MAC2,MAC3] = top_rx(complex_data);

disp("MACS: " + MAC1 + " " + MAC2 + " " + MAC3)