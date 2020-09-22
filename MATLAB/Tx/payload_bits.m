function [bits_final,Nsym] = payload_bits(FC,MAC1,MAC2,MAC3,NDBPS,ppdu_length)
service_field = zeros(16,1);
preMAC = transpose(hexToBinaryVector(FC,8*4));
MAC1b = transpose(hexToBinaryVector(MAC1,12*4));
MAC2b = transpose(hexToBinaryVector(MAC2,12*4));
MAC3b = transpose(hexToBinaryVector(MAC3,12*4));
ppdu = zeros((8*ppdu_length),1);
ppdu_tail=zeros(6,1);

Nsym = ceil((16+(8*4)+(3*4*12)+16+(8*ppdu_length)+6)/NDBPS);
Ndata = Nsym*NDBPS;
Npad = Ndata - (16+(8*4)+(3*4*12)+16+(8*ppdu_length)+6);

bits_final=[service_field;preMAC;MAC1b;MAC2b;MAC3b;zeros(16,1);ppdu;ppdu_tail;zeros(Npad,1)];
