function pilot_polarity = pilot_generator(Nsym)



in = zeros(Nsym,1);
out = scrambler(in,127);
pilot_polarity = 2*((-out)+(1/2));
end
