# [crypto] mistake

## Solution

As `a,b,c` are public values, `a * index ** 2 + b * index + c` is known. After substracting this part, the ciphertext is same when the plaintext is same. This allows to mount a well-known ECB attack.