function [type,MAC1,MAC2,MAC3] = packet_info(ppdu)
m = 12*4;
m1 = 16+32+(1:m);
m2 = max(m1)+(1:m);
m3 = max(m2)+(1:m);
MAC1 = binaryVectorToHex(ppdu(m1));
MAC2 = binaryVectorToHex(ppdu(m2));
MAC3 = binaryVectorToHex(ppdu(m3));

if isequal(transpose(ppdu(16 + 2 + (1:6))), [0,0,1,0,0,0])
    type = 'Beacon';
elseif isequal(transpose(ppdu(16 + 2 + (1:6))), [1,0,0,0,0,0])
    type = 'Data';
else
    type = 'N/A';
end

end