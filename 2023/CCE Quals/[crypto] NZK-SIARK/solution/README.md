# [crypto] NZK-SIARK

## Solution

The goal of this problem is to manipulate results when the computation of the S-box during AES is delegated to a prover.

The verification for the inverse xinv of x is `x * (x * xinv - GF(1)) == GF(0)', but the problem is that `x = 0, xinv = arbitrary` passes the verification.

Therefore, an attacker can simply leave `KEY = PLAINTEXT`, keygen normally, and then match the outputs of the S-boxes so that the inputs of the S-box layer are all zero each time. The output of the last S-box can be matched so that its output is `CIPHERTEXT`.