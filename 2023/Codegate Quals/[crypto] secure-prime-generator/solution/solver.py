from Crypto.Util.number import *
from hashlib import sha256
from pwn import *
from itertools import product
import random

BITS = 512

def get_malicious_N():
    base = 2*3*5*7*11*13 * 60 # 1801800
    i = 0
    N = 1
    phi = 1
    while i*i <= base:
        i += 1
        if base % i != 0:
            continue
        if isPrime(i+1):
            N *= i+1
            phi *= i
        if isPrime(base//i + 1):
            N *= (base//i + 1)
            phi *= (base//i)
    return N, phi

def get_additive_shares(x, n, mod):
    shares = [0] * n
    shares[n-1] = x
    for i in range(n-1):
        shares[i] = random.randrange(mod)
        shares[n-1] = (shares[n-1] - shares[i]) % mod
    assert sum(shares) % mod == x
    return shares

def POW():
    print("[DEBUG] POW...")
    b_postfix = r.recvline().decode().split(' = ')[1][6:].strip()
    h = r.recvline().decode().split(' = ')[1].strip()
    for brute in product('0123456789abcdef', repeat=6):
        b_prefix = ''.join(brute)
        b_ = b_prefix + b_postfix
        if sha256(bytes.fromhex(b_)).hexdigest() == h:
            r.sendlineafter(b' > ', b_prefix.encode())
            return True

    assert 0, "Something went wrong.."

def generate_shared_modulus():
    SMALL_PRIMES = [2, 3, 5, 7, 11, 13]
    # Constraints: N + 1 - p1 - q1 = 0 mod prime
    # Candidates of p1. p1 = N+1 mod prime
    for prime in SMALL_PRIMES:
        remainder_candidates = [(malicious_N+1) % prime] + [-i for i in range(1, (prime+1)//2)]        
        r.sendlineafter(b' > ', ' '.join(str(c) for c in remainder_candidates).encode())

    # Candidates of q1. q1 = 0 mod prime
    for prime in SMALL_PRIMES:
        remainder_candidates = [0] + [-i for i in range(1, (prime+1)//2)]       
        r.sendlineafter(b' > ', ' '.join(str(c) for c in remainder_candidates).encode())

    p1_enc = int(r.recvline().decode().split(' = ')[1])
    q1_enc = int(r.recvline().decode().split(' = ')[1])

    
    X = [-p1_enc * q1_enc, pow(malicious_N, SERVER_E, SERVER_N)] + [0] * 10

    r.sendlineafter(b' > ', ' '.join(str(x) for x in X).encode())
    
    N = int(r.recvline().decode().split(' = ')[1])
    assert N == malicious_N

# STEP 2 - N_validity_check
def N_validity_check_client():
    for _ in range(20):
        b = int(r.recvline().decode().split(' = ')[1])
        # assume that 1801800 | p1+q1 (with 1/60 probability)
        client_digest = sha256(long_to_bytes(pow(b, 1801800, malicious_N))).hexdigest()
        r.sendlineafter(b' > ', client_digest.encode())
        msg = r.recvline().decode()
        if msg != "good!\n":
            print(msg)
            return -1
    
    flag_enc = int(r.recvline().decode().split(' = ')[1])
    return flag_enc

# malicious_N = 959786094359720393880755527014764297679284755008821449461738878016667441640737889548200382905165934296940972577769636941286395812979837734191509330192492184139324025254327298004205565526064865419849248314429472118817582677251789213073647457952361312265239139158754424189980214703262530643640838565624080643710
malicious_N, malicious_phi = get_malicious_N()
assert malicious_N.bit_length() >= 1024

print("### About 60 trials are required ###")
cnt = 1
while True:
    #r = process(["python3", "./prob.py"])
    r = remote('43.200.47.102', 9001)
    print(f"{cnt}-th trial")
    POW()
    SERVER_N = int(r.recvline().decode().split(' = ')[1])
    SERVER_E = int(r.recvline().decode().split(' = ')[1])
    cnt += 1
    generate_shared_modulus()
    flag_enc = N_validity_check_client()
    if flag_enc == -1:
        r.close()
        continue
    break

d = pow(0x10001, -1, malicious_phi)
flag = pow(flag_enc, d, malicious_N)

print(long_to_bytes(flag))
