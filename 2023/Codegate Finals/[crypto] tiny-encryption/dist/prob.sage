#!/usr/bin/sage
import os

load('tiny-encryption.sage')

MAGIC_NUMBER = 256
N = 256

def bytes_to_vector(b):
    vec = vector(GF(2), N)
    assert len(b) == N // 8
    for i in range(len(b)):
        tmp = b[i]
        for j in range(8):
            vec[8*i+7-j] = tmp & 1
            tmp >>= 1    
    return vec

def vector_to_bytes(vec):
    assert len(vec) == N
    b = bytearray(N // 8)
    for i in range(len(b)):
        for j in range(8):
            b[i] = (b[i] << 1) | int(vec[8*i + j])
    return b

success = 0
while success < MAGIC_NUMBER:
    print(f"!!! {success}/{MAGIC_NUMBER} !!!")
    key_b = os.urandom(N // 8)
    key = bytes_to_vector(key_b)
    for i in range(4):
        plain_b = bytes.fromhex(input("plaintext > "))
        assert len(plain_b) == N // 8, "Invalid plaintext length"
        plain = bytes_to_vector(plain_b)
        cipher = encrypt(plain, key)
        cipher_b = vector_to_bytes(cipher)
        print(f"ciphertext > {cipher_b.hex()}")

    while True:
        idx = int(input("Guess any bits. Key index? > "))
        if not 0 <= idx < N:
            break
        guess = input(f"key[{idx}]? > ")
        if int(guess) == key[idx]:
            print("Correct!")
            success += 1
        else:
            exit(-1)

print("Good job!")
print(open("flag.txt").read())