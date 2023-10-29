from sage.all import *
from pwn import *
import math
import os
import hashlib
import signal
import random
from tqdm import tqdm


MOD = 17
HALF_MOD = (MOD+1)//2
m = 20

querynum = 0

QUERY_LIST = []

def print_list(L, prefix = ''):
    print(prefix, end='')
    for x in L:
        print(x, end = ' ')
    print()

def list_to_str(L):
    s = ''
    for x in L:
        s += str(x) + ' '
    return s

def differences(L1, L2):
    ret = 0
    for i in range(m):
        if L1[i] == L2[i]:
            ret += L1[i] * 2 ** i
    return ret

def list_to_int(L):
    assert len(L) == m, "Invalid list format"
    assert all(0 <= x < MOD for x in L), "Invalid list format"
    ret = 0
    for i in range(m):
        ret += L[i] * MOD ** i
    return ret

def int_to_list(x):
    assert 0 <= x < MOD ** m, "Invalid int format"
    L = [0] * m
    for i in range(m):
        L[i] = x % MOD
        x //= MOD
    return L

def query(Inputs):
    global querynum
    global QUERY_LIST
    querynum += len(Inputs)
    tmp = ''
    for I in Inputs:
        tmp += str(list_to_int(I)) + ' '
    r.sendlineafter(b" > ", tmp.encode())
    r.recvuntil(b" = ")
    ret = list(map(int,r.recvline().decode().split()))
    for i in range(len(Inputs)):
        QUERY_LIST.append((Inputs[i], ret[i]))
    return ret

#r = process(["python3", "./prob.py"])
r = remote('13.124.51.204', 6238)
r.recvuntil(b' = ')
TARGET = int_to_list(int(r.recvline().decode()))

#### STEP 1. Recover SboxLayer1
print("STEP 1. Recover SboxLayer1")
t = [-1] * m # S-box[i] = (x-t)^2
for i in tqdm(range(m)): # S-box index
    data = [None] * MOD
    for j in range(MOD):
        L1 = [0]*m
        L2 = [1]*m
        L1[i] = j
        L2[i] = j
        data[j] = (query([L1, L2]))

    for j in range(MOD):
        if data.count(data[j]) == 1:
            t[i] = j
            break

    if t[i] == -1:
        print("Something went wrong, cannot recover S-box. Try again.")
        exit()
    
    for j in range(8):
        idx1 = (t[i] + j) % MOD
        idx2 = (t[i] - j) % MOD
        if data[idx1] != data[idx2]:
            print("Something wrong, pair not matched. Try again.")
            exit()
    
#### STEP 2. Recover Linear Layer
print("STEP 2. Recover Linear Layer")
A = [[-1]*m for i in range(m)]
for i in range(m):
    A[i][0] = 1

for i in tqdm(range(m)):
    for j in range(1, m):
        # Want to find A[i][j]
        while A[i][j] == -1:
            L = [random.randrange(MOD) for _ in range(m)]

            Inputs = []
            for a in range(HALF_MOD):
                L[0] = (t[0] + a) % MOD
                for b in range(HALF_MOD):
                    L[j] = (t[j] + b) % MOD
                    Inputs.append(L[:])

            Outputs = query(Inputs)
            isMatched = [False] * (HALF_MOD ** 2)
            for z in range(HALF_MOD ** 2):
                if Outputs[z] & (1 << i):
                    isMatched[z] = True
            
            candidates = list(range(1,MOD))
            for a in range(HALF_MOD ** 2):
                for b in range(a+1, HALF_MOD ** 2):
                    s1 = pow(a // HALF_MOD, 2, MOD)
                    s2 = pow(a % HALF_MOD, 2, MOD)
                    s1prime = pow(b // HALF_MOD, 2, MOD)
                    s2prime = pow(b % HALF_MOD, 2, MOD)
                    
                    if s2 == s2prime:
                        continue

                    if isMatched[a] == isMatched[b]:
                        continue

                    v = (s1prime - s1) * pow(s2 - s2prime, -1, MOD) % MOD
                    
                    if v in candidates:
                        candidates.remove(v)

            if len(candidates) == 1:
                A[i][j] = candidates[0]
            
#### STEP 3. Find input
print("STEP 3. Find input")

mat = matrix(GF(MOD), A)
if mat.rank() != m:
    print("Linear layer is not invertible. Try again.")
    exit()

mat_inv = mat.inverse()
Inter2 = [[] for _ in range(m)]

for q in QUERY_LIST:
    Input = q[0]
    Inter = [pow(Input[i] - t[i], 2, MOD) for i in range(m)]
    result = q[1]
    for i in range(m):
        if (result & (1 << i)) == 0:
            continue
        
        res = sum(Inter[j] * A[i][j] for j in range(m)) % MOD
        if res not in Inter2[i]:
            Inter2[i].append(res)

for i in range(m):
    if len(Inter2[i]) == 1:
        Inter2[i].append(Inter2[i][0])
    assert len(Inter2[i]) == 2, "Unknown error. Try again."

possible_Inter1 = [pow(i, 2, MOD) for i in range(HALF_MOD)]

for brute in tqdm(range(1 << m)):
    tmp = vector(GF(MOD), m)
    for i in range(m):
        if brute & (1<<i):
            tmp[i] = Inter2[i][0]
        else:
            tmp[i] = Inter2[i][1]

    Inter1 = mat_inv * tmp
    if any(x not in possible_Inter1 for x in Inter1):
        continue

    L = [-1] * m
    for i in range(m):
        for j in range(MOD):
            if pow(j-t[i],2,MOD) == Inter1[i]:
                L[i] = j
    
    query([L])
    print("\n\nTOTAL QUERY NUMBER:", querynum)
    print(r.recv())
    exit()
