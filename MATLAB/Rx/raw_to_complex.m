%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read raw data in binary format to a complex vector
% data is stored as inphase followed by quadrature
% inputs:
% - file_name: name of the file
% - fraction: any range between 0 to 1, which will be multiplied by the
% size of the file
% output:
% - complex_data: Nx1 vector containing I + jQ
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [complex_data] = raw_to_complex(file_name, fraction)

file_id = fopen(file_name , 'r'); % open file
raw_data = fread(file_id, Inf, 'float32'); % read file with float 32 percision
fclose(file_id); % close file
inphase_data = raw_data(1:2:end); % extract inphase components
quadrature_data = raw_data(2:2:end); % extract quadrature components
data_length = floor(fraction*min(length(inphase_data),length(quadrature_data))); % find common length
complex_data = inphase_data(1:data_length) + 1j*quadrature_data(1:data_length); % construct complex signal
complex_data = complex_data/max(abs(complex_data)); % normalize complex signal with respect to the maximum magnitude
end
















