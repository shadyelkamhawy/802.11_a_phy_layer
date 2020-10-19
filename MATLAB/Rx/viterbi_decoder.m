%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% VITERBI DECODER
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function decoded_out = viterbi_decoder(coded_in,G1,G2,R)%,G1,G2)
% popular polynomials
% k = 7
% G1 = [1,0,1,1,0,1,1];
% G2 = [1,1,1,1,0,0,1];
% k = 3
% G1= [1,1,1];
% G2 = [1,0,1];
M = length(coded_in); % length of depunctured input bits
puncpat12 = [1,1]; % 1/2
puncpat34 = [1,1,1,0,0,1]; % 3/4
puncpat23 = [1,1,1,0]; % 2/3
if R == "1/2"
    
    if length(puncpat12) > M
        puncpat_ext = puncpat12(1:M);
    else
        Q = floor(M/length(puncpat12));
        puncpat_ext = repmat(puncpat12,1,Q);
        if Q*length(puncpat12) < M
            puncpat_ext = [puncpat_ext,puncpat12(1:(M-(Q*length(puncpat12))))];
        end
    end
elseif R == "3/4"
    if length(puncpat34) > M
        puncpat_ext = puncpat34(1:M);
    else
        Q = floor(M/length(puncpat34));
        puncpat_ext = repmat(puncpat34,1,Q);
        if Q*length(puncpat34) < M
            puncpat_ext = [puncpat_ext,puncpat34(1:(M-(Q*length(puncpat34))))];
        end
    end
else
    if length(puncpat23) > M
        puncpat_ext = puncpat23(1:M);
    else
        Q = floor(M/length(puncpat23));
        puncpat_ext = repmat(puncpat23,1,Q);
        if Q*length(puncpat23) < M
            puncpat_ext = [puncpat_ext,puncpat23(1:(M-(Q*length(puncpat23))))];
        end
    end
end


N = M/2; % length of decoded bits for code rate = 1/2
g1 = find(G1);
g2= find(G2);

k = length(G1); % number of shift registers + 1
n_states = 2^(k-1); % number of possible states
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% STATE TRANSITION TABLE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
N0 = zeros(n_states,1); % next state corresponding to a 0 input for the current state(row index)
N1 = zeros(n_states,1); % next state corresponding to a 1 input for the current state(row index)
P = zeros(n_states,2); % previous states for the current state(row index)
AB0 = zeros(n_states,2); % coded output corresponding to a 0 input for the current state(row index)
AB1 = zeros(n_states,2); % coded output corresponding to a 1 input for the current state(row index)
% next states
for n = 1:n_states
    current_state = (de2bi(n-1,k-1));
    N0(n) = bi2de(([0,current_state(1:(k-2))])); % 0 transition
    N1(n) = bi2de(([1,current_state(1:(k-2))])); % 1 transition
end
% previous states
for n = 1:n_states
    % find current state in N0 -> which index corresponds to this entry,
    % take the index and store in P0(n)
    x = [find(N0 == (n-1))-1,find(N1 == (n-1))-1];
    P(n,1) = x(1);
    P(n,2) = x(2);
end
% coded outputs
for n = 1:n_states
    % output due to 0 input
    current_vector = (de2bi(n-1,k-1));
    current_vector0 = [0,current_vector(1:(k-1))];
    A0 = mod(sum(current_vector0(g1)),2);
    B0 = mod(sum(current_vector0(g2)),2);
    AB0(n,:) = [A0,B0];
    % output due to 1 input
    current_vector1 = [1,current_vector(1:(k-1))];
    A1 = mod(sum(current_vector1(g1)),2);
    B1 = mod(sum(current_vector1(g2)),2);
    AB1(n,:) = [A1,B1];
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CALCULATE EMISSION HAMMING DISTANCE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% hamming distance matrix for branch 1 from each state at each point in
% time
Ha = zeros(n_states,N+1);
H0 = zeros(n_states,N+1);
H1 = zeros(n_states,N+1);
% all hamming distance at the first distance from any state other than the
% first state is invalid, INFINITY
H0(2:end,1) = Inf;
H1(2:end,1) = Inf;
% calculate the feed forward hamming matrix
ab0 = AB0(1,:);
ab1 = AB1(1,:);
c_in = coded_in((2*(1-1))+(1:2));
H0(1,1) = sum(xor(c_in(:),ab0(:)));
H1(1,1) = sum(xor(c_in(:),ab1(:)));

% H0(1,1) = sum(xor(coded_in(1:2),transpose(AB0(1,:))));
% H1(1,1) = sum(xor(coded_in(1:2),transpose(AB1(1,:))));
for n = 2:N
    for m =1:n_states
        ab0 = AB0(m,:);
        ab1 = AB1(m,:);
        c_in = coded_in((2*(n-1))+(1:2));
        hw = puncpat_ext((2*(n-1))+(1:2));
        H0(m,n) = sum(hw(:).*xor(c_in(:),ab0(:)));
        H1(m,n) = sum(hw(:).*xor(c_in(:),ab1(:)));
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CALCULATE BEST BRANCHES
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% matrix for previous survivor states starting from second node
b = zeros(n_states,N+1);
for n = 2:(N+1)
    for m =1:n_states
        ps1 = P(m,1);
        if N0(ps1+1) == (m-1)
            h1 = Ha(ps1+1,n-1) + H0(ps1+1,n-1);
        else
            h1 = Ha(ps1+1,n-1) + H1(ps1+1,n-1);
        end
        
        ps2 = P(m,2);
        if N0(ps2+1) == (m-1)
            h2 = Ha(ps2+1,n-1) + H0(ps2+1,n-1);
        else
            h2 = Ha(ps2+1,n-1) + H1(ps2+1,n-1);
        end
        
        if (h1 > h2) % branch with minimum hamming distance
            b(m,n) = ps2;
            Ha(m,n) = h2;
        else
            b(m,n) = ps1;
            Ha(m,n) = h1;
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MINIMUM TOTAL HAMMING DISTANCE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end_best_path = (find(Ha(:,N+1)==min(Ha(:,N+1)))-1); % find the path with the minimum total hamming distance
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TRACEBACK BEST PATHS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
T = length(end_best_path);
best_path = zeros(T,N+1);
best_path(:,N+1) = end_best_path;
for t = 1:T
    for n =N:-1:1
        m = best_path(t,n+1);
        best_path(t,n) = b(m+1,n+1);
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DECODED BEST PATHS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
decoded = zeros(T,N);
for t = 1:T
    for n = 1:N
        current_state = best_path(t,n);
        next_state = best_path(t,n+1);
        if next_state == N0(current_state+1)
            decoded(t,n) = 0;
        else
            decoded(t,n) = 1;
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ENCODED BEST PATHS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
encoded = zeros(T,M);
for t = 1:T
    x = conv_enc(decoded(t,:),R);
    encoded(t,:) = depuncture_bits(x,R);
    
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BEST ENCODED FIT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
x = transpose(coded_in(:));
e = sum(xor(x,encoded),2);
decoded_out = decoded(min(find(e==min(e))),:);