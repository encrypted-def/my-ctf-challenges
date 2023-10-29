from Crypto.Util.number import *
import math
import os
import hashlib
import signal

STATE_SIZE = 4 
N = 128
MOD = 2**N
NUM_ROUNDS = 256
TIME_OUT = 600
QUERY_NUM = 100

round_constants = [[0]*STATE_SIZE for _ in range(NUM_ROUNDS)]

def set_round_constants(iv):
    for i in range(NUM_ROUNDS):
        for j in range(STATE_SIZE):
            m = b'wacon2023_' + long_to_bytes(iv) + bytes([i]) + bytes([j])        
            round_constants[i][j] = bytes_to_long(hashlib.sha256(m).digest()) % MOD

def encrypt(state, KEY):
    assert len(state) == len(KEY) == STATE_SIZE
    for i in range(NUM_ROUNDS):
        # Add key and round constants
        for j in range(STATE_SIZE):
            state[j] = pow(state[j] + KEY[j] + round_constants[i][j], (i+j) % 4 + 3, MOD)
        # Shift
        state[0], state[1], state[2], state[3] = state[1], state[2], state[3], state[0]

def challenge():
    KEY = [bytes_to_long(os.urandom(N // 8)) for _ in range(STATE_SIZE)]
    for _ in range(QUERY_NUM):
        plain = list(map(int, input("plain?(ex: 1 1 1 1) > ").split()))
        iv = int(input("iv? > "))
        if len(plain) != STATE_SIZE or min(plain) < 0 or max(plain) >= MOD:
            print("wrong plaintext")
            continue
        if iv < 0 or iv >= MOD:
            print("wrong iv")
            continue
        set_round_constants(iv)
        state = plain[:]
        encrypt(state, KEY)
        print(f"cipher = {state[0]} {state[1]} {state[2]} {state[3]}")

    key_guess = list(map(int, input("key?(ex: 1 1 1 1) > ").split()))
    if KEY != key_guess:
        print("Wrong...")
        exit(-1)
    else:
        print("Good!")

signal.alarm(TIME_OUT)

challenge()

print("Good job!", open("flag.txt", 'r').read())