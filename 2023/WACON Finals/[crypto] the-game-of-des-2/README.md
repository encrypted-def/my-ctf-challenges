# [crypto] The Game of DES2

## Tag

DES, Linear cryptanalysis, Ciphertext only attack

## Difficulty

Hard

## Scenario

The goal is to break a reduced-round DES. Plaintext is biased. IP, CP, P, and FP are changed to prevent that obtaining flag without understanding LC so that using the trail provided in the Matsui's paper.

- Baby : round number = 2, known plaintext attack
- Easy : round number = 5, known plaintext attack
- Hard : round number = 5, Ciphertext only attack