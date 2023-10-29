from Crypto.Util.number import *
import random
import os
from copy import deepcopy
from tqdm import tqdm
from pwn import *


STATE_SIZE = 4 
N = 128
MOD = 2**N
NUM_ROUNDS = 256
TIME_OUT = 600
QUERY_NUM = 100

def query(plain, iv):
    r.recvuntil(b" > ")
    r.sendline(f"{plain[0]} {plain[1]} {plain[2]} {plain[3]}".encode())
    r.recvuntil(b" > ")
    r.sendline(str(iv).encode())
    r.recvuntil(b" = ")
    cipher = list(map(int, r.recvline().split()))
    return cipher

def query_ans(KEY):
    r.recvuntil(b" > ")
    r.sendline(f"{KEY[0]} {KEY[1]} {KEY[2]} {KEY[3]}".encode())
    r.interactive()

def encrypt(state, KEY):
    assert len(state) == len(KEY) == STATE_SIZE
    for i in range(NUM_ROUNDS):
        # Add key and round constants
        for j in range(STATE_SIZE):
            state[j] = pow(state[j] + KEY[j] + round_constants[i][j], (i+j) % 4 + 3, MOD)
        # Shift
        state[0], state[1], state[2], state[3] = state[1], state[2], state[3], state[0]

#r = process(["python3", "prob.py"])
r = remote("175.118.127.63", 3715)

plains = [[random.randrange(1,MOD,2),random.randrange(1,MOD,2),random.randrange(1,MOD,2),random.randrange(1,MOD,2)] for _ in range(100)]
ivs = [random.randrange(0,MOD) for _ in range(100)]
ciphers = [None] * 100

for i in range(100):
    ciphers[i] = query(plains[i], ivs[i])

round_constants = [[0]*STATE_SIZE for _ in range(NUM_ROUNDS)]

def set_round_constants(iv):
    for i in range(NUM_ROUNDS):
        for j in range(STATE_SIZE):
            m = b'wacon2023_' + long_to_bytes(iv) + bytes([i]) + bytes([j])        
            round_constants[i][j] = bytes_to_long(hashlib.sha256(m).digest()) % MOD

current_mod = 2
key_remainder_candidates = [[a,b,c,d] for a in [0,1] for b in [0,1] for c in [0,1] for d in [0,1]]

round_constants_eachiv = []
for iv in ivs:
    set_round_constants(iv)
    round_constants_eachiv.append(deepcopy(round_constants))

chk = 0
while True:
    next_candidates = []
    for candidates in key_remainder_candidates:
        for i in range(100):
            round_constants = round_constants_eachiv[i]
            #set_round_constants(ivs[i])
            state = plains[i][:]
            encrypt(state, candidates)
            if any(state[j] % current_mod != ciphers[i][j] % current_mod for j in range(4)):
                break

        else:
            if current_mod == MOD:
                query_ans(candidates)
                exit()
            else:
                next_candidates += [[candidates[0]+a,candidates[1]+b,candidates[2]+c,candidates[3]+d] for a in [0,current_mod] for b in [0,current_mod] for c in [0,current_mod] for d in [0,current_mod]]
    
    key_remainder_candidates = next_candidates
    current_mod *= 2
    chk+=1
    print(f"{chk}/{N}, {len(key_remainder_candidates)} candidates")

    if len(key_remainder_candidates) == 0:
        break