function c = cross_corr(x1,x2)
% returns the cross correlation coefficient between two signals x1 and x2
P1 = ctranspose(x1)*x1; % power of the first signal
P2 = ctranspose(x2)*x2; % power of the second signal
c = abs(ctranspose(x1)*x2)/sqrt(P1*P2); % cross correlation coefficient
end