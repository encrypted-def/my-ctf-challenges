# [crypto] BYOS

## Solution

First of all, `key3` is simply ignored when the difference between two ciphers $C1 \oplus C2$ is considered. When the permutation is chosen to be MSB 12 bits and LSB 12 bits are not mixed, then remaining keys can also be divided into MSB/LSB. This allows to bruteforce only `24 bits` for MSB/LSB, respectively.