from Crypto.Util.number import *
import random
import os
from copy import deepcopy
from tqdm import tqdm
from pwn import *

def xor(a : bytes, b : bytes):
    return bytes([u ^ v for u,v in zip(a,b)])

def query(q, inverse):
    if inverse == True:
        inverse = 'y'
    if inverse == False:
        inverse = 'n'
    r.recvuntil(b" > ")
    r.sendline(q.hex().encode())
    r.recvuntil(b" > ")
    r.sendline(inverse.encode())
    return bytes.fromhex(r.recvline().strip().decode())

#r = process(["python3", "./deploy/prob.py"])
r = remote("175.118.127.63", 2821)

def chal1():
    ### Challenge 1, 1 query
    r.recvuntil(b" > ")
    r.sendline(b"1")
    for _ in tqdm(range(40)):
        result = query(bytes(16), False)
        r.recvuntil(b" > ")            
        if result[:8] == bytes(8):
            r.sendline(b'0')
        else:
            r.sendline(b'1')


def chal2():
    ### Challenge 2, 2 queries
    r.recvuntil(b" > ")
    r.sendline(b"2")
    for _ in tqdm(range(40)):
        M1 = bytes(16)
        M2 = bytes([1]+[0]*15)
        result1 = query(M1, False)
        result2 = query(M2, False)
        r.recvuntil(b" > ")            
        if xor(result1[:8], result2[:8]) == bytes([1] + [0]*7):
            r.sendline(b'0')
        else:
            r.sendline(b'1')

def chal3():
    ### Challenge 3, 3 queries
    # Generic Attacks on Feistel Schemes
    r.recvuntil(b" > ")
    r.sendline(b"3")
    for _ in tqdm(range(40)):
        x1 = bytes(16)
        y1 = query(x1, False)
        s1, t1 = y1[:8], y1[8:]

        x2 = bytes([1] + [0]*15)
        y2 = query(x2, False)
        s2, t2 = y2[:8], y2[8:]

        y3 = s2 + xor(t2, bytes([1] + [0]*7))
        x3 = query(y3, True)
        l3, r3 = x3[:8], x3[8:]
        
        r.recvuntil(b" > ")            
        if xor(s2, s1) == r3:
            r.sendline(b'0')
        else:
            r.sendline(b'1')

def chal4():
    ### Challenge 4, 4 queries
    r.recvuntil(b" > ")
    r.sendline(b"4")
    BLOCK0 = bytes(8)
    BLOCK1 = bytes([0]*7+[1])
    for _ in tqdm(range(40)):
        x1 = BLOCK0 + BLOCK0
        y1 = query(x1, False)

        x2 = BLOCK1 + BLOCK1
        y2 = query(x2, False)

        z1 = query(xor(y1, BLOCK1) + BLOCK1, True)
        z2 = query(xor(y2, BLOCK1) + BLOCK0, True)

        r.recvuntil(b" > ")            
        if xor(z1, z2) == BLOCK1:
            r.sendline(b'0')
        else:
            r.sendline(b'1')

def chal5():
    ### Challenge 5, 256 queries
    r.recvuntil(b" > ")
    r.sendline(b"256")
    for _ in tqdm(range(40)):
        s = 0
        for i in range(256):
            y = query(bytes([i]), False)
            s ^= y[0]
        
        r.recvuntil(b" > ")            
        if s == 0:
            r.sendline(b'0')
        else:
            r.sendline(b'1')

chal1()
chal2()

print(r.recvuntil(b"#")) # Get flag_baby

chal3()

print(r.recvuntil(b"#")) # Get flag_easy

chal4()
chal5() # Having 15% of failure prob

r.interactive() # Get flag_hard