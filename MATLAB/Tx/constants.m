% short training sequence length
global sts_len;
sts_len = 16;
% short training sequence cycles 
global sts_cyc;
sts_cyc = 10;
% total short training field length
global stf_len;
stf_len = sts_len*sts_cyc;
% long training sequence length
global lts_len;
lts_len = 64;
% long training sequence cycles
global lts_cyc;
lts_cyc = 2.5;
% total long training field length
global ltf_len;
ltf_len = lts_len*lts_cyc;
% cyclic prefix length
global cyc_prefix_len;
cyc_prefix_len = 16;
% symbol length
global symb_len;
symb_len = 64;
% signal field length
global sig_len;
sig_len = cyc_prefix_len + symb_len;
% minimum packet length
global pkt_min_len;
pkt_min_len = stf_len;

% deinterleaving indexing
global k48;
global k96;
global k192;
global k288;
load('deinterleave_index.mat');

%interleaving indexing
global w48;
global w96;
global w192;
global w288;
load('interleave_index.mat');

% STF FFT 
global stf_fft;
stf_fft = (1+1i)*[0;0;0;0;0;0;...
    0;0;1;0;0;0;-1;0;0;0;1;0;0;0;-1;0;0;0;-1;0;0;0;1;0;0;0;...
    0;...
    0;0;0;-1;0;0;0;-1;0;0;0;1;0;0;0;1;0;0;0;1;0;0;0;1;0;0;...
    0;0;0;0;0];

% LTF FFT
global ltf_fft;
ltf_fft = [...
    0;0;0;0;0;0;...
    1;1;-1;-1;1;1;-1;1;-1;1;1;1;1;1;1;-1;-1;1;1;-1;1;-1;1;1;1;1;...
    0;...
    1;-1;-1;1;1;-1;1;-1;1;-1;-1;-1;-1;-1;1;1;-1;-1;1;-1;1;-1;1;1;1;1;...
    0;0;0;0;0;...
    ];
    
global G1; % First polynomial of the convolutional encoder
global G2; % Second polynomial of the convolutional encoder
G1 = [1,0,1,1,0,1,1]; 
G2 = [1,1,1,1,0,0,1];