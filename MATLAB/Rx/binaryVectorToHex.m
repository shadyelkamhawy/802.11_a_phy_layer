function hex = binaryVectorToHex(bits)
hex = [];
Nhex = length(bits)/4;
bitsT = bits';
for n = 1:Nhex
    if isequal(bitsT(((n-1)*4)+(1:4)),[0,0,0,0])
        hex = [hex,'0'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,0,0,1])
        hex = [hex,'1'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,0,1,0])
        hex = [hex,'2'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,0,1,1])
        hex = [hex,'3'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,1,0,0])
        hex = [hex,'4'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,1,0,1])
        hex = [hex,'5'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,1,1,0])
        hex = [hex,'6'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[0,1,1,1])
        hex = [hex,'7'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,0,0,0])
        hex = [hex,'8'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,0,0,1])
        hex = [hex,'9'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,0,1,0])
        hex = [hex,'A'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,0,1,1])
        hex = [hex,'B'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,1,0,0])
        hex = [hex,'C'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,1,0,1])
        hex = [hex,'D'];
    elseif isequal(bitsT(((n-1)*4)+(1:4)),[1,1,1,0])
        hex = [hex,'E'];
    else
        hex = [hex,'F'];
    end
end