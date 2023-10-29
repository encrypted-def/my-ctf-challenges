# [crypto] Tiny Encryption

## Tag

LowMC variants, Difference enumeration attack, eprint 2018/859(Cryptanalysis of Low-Data Instances of Full LowMCv2)

## Difficulty

Hard

## Scenario

Cryptosystem is a LowMC variants. S-box is very simple(`cipher[0] += cipher[1] * cipher[2]`), but the round number is 128. Attack setting is Chosen plaintext attack setting but only 4 plaintext-ciphertext pairs are given.

Flag is given even a single key bit leak is succeed.