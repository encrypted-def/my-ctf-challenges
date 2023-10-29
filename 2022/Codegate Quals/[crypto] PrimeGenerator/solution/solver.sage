#!/usr/bin/sage
from Crypto.Util.number import *
from pwn import *
from sage.all import *
import math

r = remote("localhost", 9001)

BITS = 512
UPPER_BITS = 296
LOWER_BITS = BITS - UPPER_BITS

primes = [ 3, 5, 7, 11, 13, 17, 19, 23, 29,
31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
607, 613, 617, 619, 631, 641, 643, 647, 653, 659]

remainders = [set([x for x in range(p)]) for p in primes]

def prod(L):
    val = 1
    for x in L:
        val *= x
    return val

def get_lower():
    r.recvuntil(b"> ")
    r.sendline(b"1")
    r.recvuntil(b"> ")
    r.sendline(b"10")
    return [int(r.recvline()) for _ in range(10)]

def get_nc():
    r.recvuntil(b"> ")
    r.sendline(b"2")
    r.recvuntil(b"n : ")
    n = int(r.recvline())
    r.recvuntil(b"c : ")
    c = int(r.recvline())
    return n, c

def rsa_high_bits_known(n, c, upper):
    F.<x> = PolynomialRing(Zmod(n), implementation='NTL'); 
    pol = x - upper
    beta = 0.48  # we should have q >= N^beta
    XX = 2 ** LOWER_BITS
    epsilon = beta / 7
    rt = pol.small_roots(XX, beta, epsilon)  
    q = int(gcd(rt[0] - upper, n))
    p = int(n) // int(q)
    assert(p*q == n and p > 1 and q > 1)
    phi = (p-1)*(q-1)
    e = 0x10001
    d = int(pow(e, -1, phi))
    plain = int(pow(c, d, n))
    print(long_to_bytes(plain))

#### STEP 1. Recover UPPER using crt ####
print("[+] STEP 1. Recover UPPER using crt")
crt_a = [0]
crt_m = [2**LOWER_BITS]

cnt = 0
while prod(crt_m) < 2**BITS:
    cnt += 1
    if cnt % 10 == 0:
        print(f"Gather {cnt*10} primes.. progress : {int(100 * (math.log2(prod(crt_m))-LOWER_BITS) / UPPER_BITS)}%")
    lowers = get_lower()
    for lower in lowers:
        for i in range(len(primes)):
            rem = lower % primes[i]
            if rem in remainders[i]:
                remainders[i].remove(rem)
                if len(remainders[i]) == 1:
                    crt_a.append(primes[i] - remainders[i].pop())
                    crt_m.append(primes[i])

upper = crt(crt_a, crt_m)
print(f"[+]UPPER = {upper.hex()}")

#### STEP 2. Recover FLAG using RSA Factoring with high bits known attack ###
print("[+] STEP 2. Recover FLAG using RSA Factoring with high bits known attack")
n, c = get_nc()
rsa_high_bits_known(n, c, upper)
