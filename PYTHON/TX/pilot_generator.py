import numpy as np
from TX import scrambler

def pilot_generator(Nsym):
    var = np.zeros(Nsym)
    out = scrambler.scrambler(var, 127)
    pilot_polarity = 2*((-out)+(1/2))  
    return pilot_polarity

