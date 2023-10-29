# [crypto] NZK-SIARK

## Tag

AES, ZK-SNARK

## Difficulty

Medium

## Scenario

The challenge asks us to find the KEY which satisfies `AES_K(P) = C`. `P, C` are randomly chosen. Unlike normal AES, the verifier(=server) does not directly compute the inverse. Inverse is given by prover(=user) and the verifier only verifies by checking `x * (x * xinv - GF(1)) == GF(0)`.