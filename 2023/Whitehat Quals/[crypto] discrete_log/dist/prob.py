from Crypto.Util.number import *
import os

def is_safe_prime(p):
    if not isPrime(p):
        return False
    
    if p.bit_length() > 1024:
        return False

    q = int(input("A large(> 999 bits) prime q such that q | p-1? (in hex) > "), 16)
    if q < 0 or q.bit_length() < 1000 or p % q != 1:
        return False
    
    return True
    
N = 1020
flag = open('flag', 'rb').read()
x = flag + os.urandom(N // 8 - len(flag))
x = bytes_to_long(x)

for _ in range(77):
    p = int(input("prime modulus p? (in hex) > "), 16)
    if not is_safe_prime(p):
        print("invalid p..")
        exit(-1)

    g = bytes_to_long(os.urandom(N // 8))
    print(f"g = {hex(g)[2:]}")

    y = pow(g, x, p)
    print(f"g^x = {hex(y)[2:]}")

print("bye..")