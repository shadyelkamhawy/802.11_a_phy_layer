import math as m
import numpy as np
from RX import de2bi
from RX import bi2de


def viterbi_decoder(coded_in, G1, G2, R):
    M = len(coded_in)
    puncpat12 = [1, 1]
    puncpat34 = [1, 1, 1, 0, 0, 1]
    puncpat23 = [1, 1, 1, 0]
    # coded_in = np.array(coded_in, dtype=int)
    # coded_in = coded_in.astype(int)
    coded_in_array = np.zeros(len(coded_in))
    for n in range(0, len(coded_in)):
        coded_in_array[n] = coded_in[n]
    coded_in_array = coded_in_array.astype(int)

    if R == "1/2":
        if len(puncpat12) > M:
            puncpat_ext = puncpat12[0:M]
        else:
            Q = m.floor(M/len(puncpat12))
            puncpat_ext_temp = np.tile(puncpat12, (1, Q))
            if Q*len(puncpat12) < M:
                puncpat_ext = [puncpat_ext_temp, puncpat12[0: (M - (Q * len(puncpat12)))]]

    elif R == "3/4":
        if len(puncpat34) > M:
            puncpat_ext_temp = puncpat34[0:M]
        else:
            Q = m.floor(M/len(puncpat34))
            puncpat_ext_temp = np.tile(puncpat34, (1, Q))
            if Q*len(puncpat34) < M:
                puncpat_ext = [puncpat_ext_temp, puncpat34[0: (M - (Q * len(puncpat34)))]]
    else:
        if len(puncpat23) > M:
            puncpat_ext_temp = puncpat23[0:M]
        else:
            Q = m.floor(M/len(puncpat23))
            puncpat_ext_temp = np.tile(puncpat23, (1, Q))
            if Q*len(puncpat23) < M:
                puncpat_ext = [puncpat_ext_temp, puncpat23[0: (M - (Q * len(puncpat23)))]]


    puncpat_ext = np.zeros(len(puncpat_ext_temp[0,:]))
    for n in range(0, len(puncpat_ext_temp[0, :])):
        temp = puncpat_ext_temp[0, n]
        puncpat_ext[n] = puncpat_ext_temp[0, n]
    puncpat_ext = puncpat_ext.astype(int)

    N = int(M/2)  # Length of decoded bits for code rate = 1/2

    g1_temp = np.argwhere(G1)
    g2_temp = np.argwhere(G2)
    g1 = np.zeros(len(g1_temp))
    g2 = np.zeros(len(g2_temp))

    for n in range(0, len(g1_temp)):
        g1[n] = g1_temp[n]

    for n in range(0, len(g2_temp)):
        g2[n] = g2_temp[n]

    g1 = g1.astype(int)
    g2 = g2.astype(int)

    k = len(G1)
    n_states = 2**(k-1)

    #########################################
    # STATE TRANSITION TABLE
    #########################################
    N0 = np.zeros(n_states, dtype=int)  # next state corresponding to a 0 input for the current state(row index)
    N1 = np.zeros(n_states, dtype=int)  # next state corresponding to a 1 input for the current state(row index)
    P = np.zeros((n_states, 2), dtype=int)  # previous states for the current state(row index)
    AB0 = np.zeros((n_states, 2), dtype=int) #  coded output corresponding to a 0 input for the current state(row index)
    AB1 = np.zeros((n_states, 2), dtype=int) #  coded output corresponding to a 1 input for the current state(row index)

    # Next States:
    for n in range(0, n_states):
        current_state = de2bi.de2bi(n, k-1)
        trans_val = current_state[0:k-2]
        trans_val_0 = [0] + trans_val
        trans_val_1 = [1] + trans_val
        N0[n] = bi2de.bi2de(trans_val_0)  # 0 transition
        N1[n] = bi2de.bi2de(trans_val_1)  # 1 transition
    # Previous States:
    for n in range(0, n_states):
        # find current state in N0 -> which index corresponds to this entry,
        # take the index and store in P0(n)
        x1 = np.argwhere(N0 == n)
        x2 = np.argwhere(N1 == n)

        if len(x1) == 2:
            x = [x1[0],x1[1]]
        elif len(x1) == 1:
            x = [x1[0],x2[0]]
        else:
            x = [x2[0],x2[1]]

        P[n, 0] = x[0]
        P[n, 1] = x[1]

    for n in range(0, n_states):
        current_vector = de2bi.de2bi(n, k - 1)
        current_vector0 = [0] + current_vector
        A0 = [current_vector0[x] for x in g1]
        A0 = sum(A0)
        A0 = np.mod(A0, 2)

        B0 = [current_vector0[x] for x in g2]
        B0 = sum(B0)
        B0 = np.mod(B0, 2)
        AB0[n, :] = [A0, B0]

        current_vector1 = [1] + current_vector
        A1 = [current_vector1[x] for x in g1]
        A1 = sum(A1)
        A1 = np.mod(A1, 2)

        B1 = [current_vector1[x] for x in g2]
        B1 = sum(B1)
        B1 = np.mod(B1, 2)
        AB1[n, :] = [A1, B1]

    ######################################
    # CALCULATE EMISSION HAMMING DISTANCE:
    ######################################
    Ha = np.zeros((n_states, N+1))
    H0 = np.zeros((n_states, N+1))
    H1 = np.zeros((n_states, N+1))

    H0[0:len(H0)+1, 0] = m.inf
    H1[0:len(H1)+1, 0] = m.inf

    ab0 = AB0[0, :]
    ab1 = AB1[0, :]

    c_in = coded_in_array[0:1+1]
    H0[0, 0] = np.sum(c_in[:] ^ ab0[:])
    H1[0, 0] = np.sum(c_in[:] ^ ab1[:])

    for n in range(1, N):
        for k in range(0, n_states):
            ab0 = AB0[k, :]
            ab1 = AB1[k, :]
            c_in = coded_in_array[((2*n) + 0):((2*n) + 2)]
            hw = puncpat_ext[(2*n):((2*n) + 2)]
            H0[k, n] = np.sum(hw[:] * (c_in[:] ^ ab0[:]))
            H1[k, n] = np.sum(hw[:] * (c_in[:] ^ ab1[:]))

    ##############################################
    # CALCULATE BEST BRANCHES (problem is in here)
    ##############################################
    b = np.zeros((n_states, N+1))
    for n in range(1, N+1):
        for k in range(0, n_states):
            ps1 = P[k, 0]
            ps2 = P[k, 1]

            if N0[ps1] == k:
                h1 = Ha[ps1, n-1] + H0[ps1, n-1]
            else:
                h1 = Ha[ps1, n-1] + H1[ps1, n-1]

            if N0[ps2] == k:
                h2 = Ha[ps2, n-1] + H0[ps2, n-1]
            else:
                h2 = Ha[ps2, n-1] + H1[ps2, n-1]

            if h1 > h2:
                b[k, n] = ps2
                Ha[k, n] = h2
            else:
                b[k, n] = ps1
                Ha[k, n] = h1

    best_path_value = min(Ha[:, N])
    end_best_path_temp = np.argwhere(Ha[:, N] == best_path_value)
    end_best_path = np.zeros(len(end_best_path_temp))
    for n in range(0, len(end_best_path)):
        end_best_path[n] = end_best_path_temp[n, 0]

    #################################
    # TRACEBACK BEST PATHS:
    #################################
    t_T = len(end_best_path)
    best_path = np.zeros((t_T, N+1))
    best_path[:, N] = end_best_path
    for t in range(0, t_T):
        for n in range(N-1, 0, -1):
            k = int(best_path[t, n+1])
            best_path[t, n] = b[k, n+1]

    # PERFECT TO HERE:
    ##############################
    # DECODED BEST PATHS:
    ##############################
    decoded = np.zeros((t_T, N+1))
    for t in range(0, t_T):
        for n in range(0, N-1-1):
            current_state = best_path[t, n]
            current_state = current_state.astype(int)
            next_state = best_path[t, n + 1]
            next_state = next_state.astype(int)
            if next_state == N0[current_state]:
                decoded[t, n] = 0
            else:
                decoded[t, n] = 1

    decoded_bits = decoded[:, 0:len(decoded[0, :])+1]

    # ##################################
    # # ENCODED BEST PATHS
    # ##################################
    # encoded = np.zeros((t_T, M))  # The issue is here in this loop
    # for t in range(1, t_T+1):
    #     if t < t_T+1:
    #         x = conv_enc(decoded_bits[t-1, :], R)
    #         x = depuncture_bits(x, R)
    #         encoded[t - 1, :] = np.array(x)
    #
    # ###################################
    # # BEST ENCODED FIT
    # ###################################
    # x = coded_in_array[1:len(coded_in_array)+1]
    # x = x.astype(int)
    # encoded = encoded.astype(int)
    # e = sum((x ^ encoded[0, :]), 0)  # This line may be wrong
    # decoded_out = decoded_bits[0, e-1:len(decoded_bits[0, :])+1]
    return decoded_bits
