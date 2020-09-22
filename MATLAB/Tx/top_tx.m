
function s = top_tx(R,MSC,ppdu_length,FC,MAC1,MAC2,MAC3)
constants;
global ltf_fft;
global stf_fft;
global symb_len;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PREAMBLE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sts = ifft(fftshift(stf_fft)); % inverse FFT to get 64 samples in time domain
sts_norm = sts/sqrt(sts'*sts);
stf = [sts_norm;sts_norm;sts_norm(1:32)]; % repeat the short training sequence 2.5 times -> 64 64 32 = 160
lts = ifft(fftshift(ltf_fft)); % inverse FFT to get 64 samples in time domain
lts_norm = lts/sqrt(lts'*lts);
ltf = [lts_norm(33:64);lts_norm;lts_norm]; % repeat 2.5 times -> last 32 samples then long training sequence repeated twice
[sig,NCBPS,NDBPS] = sig_field(R,MSC,ppdu_length);
sig = sig/sqrt(sig'*sig);
preamble = [stf;ltf;sig];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PAYLAOD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% payload bits
[bits_final,Nsym] = payload_bits(FC,MAC1,MAC2,MAC3,NDBPS,ppdu_length);
% scramble
seed=93;
scrambled_bits = scrambler(bits_final,seed);
% encode
bits_encoded = conv_enc(scrambled_bits,R);
% samples for symbols
ppdu_samples = zeros(80*Nsym,1);
% pilot polarity for symbols
pilot_polarity = pilot_generator(Nsym+1);
for n =1:Nsym
    bits_inter = interleave_symbs(bits_encoded(((n-1)*NCBPS)+(1:NCBPS)),NCBPS);
    iq_symb_fft = modulate_symbs(bits_inter,pilot_polarity(n+1),MSC);
    iq_symb = ifft(fftshift(iq_symb_fft));
    iq_symb_norm = iq_symb/sqrt(iq_symb'*iq_symb);
    cyclic_prefix = iq_symb_norm(49:64);
    iq_symb_80 = [cyclic_prefix;iq_symb_norm];
    ppdu_samples(((n-1)*(cyc_prefix_len+symb_len))+(1:(cyc_prefix_len+symb_len))) = iq_symb_80;
end

s = [preamble;ppdu_samples];