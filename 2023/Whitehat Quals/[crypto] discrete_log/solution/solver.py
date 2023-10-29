from Crypto.Util.number import *
from pwn import *
from sage.all import *
import random
from tqdm import tqdm


def preprocess():
  q_lists = []
  while len(q_lists) < 3000:
    p = random.randint(2**1000, 2**1001)
    if isPrime(p):
      q_lists.append(p)
      print(len(q_lists))

  return q_lists

def get_unsafe_p(r):
  print("!!", r)
  q = (2**1024 - 1) // r
  if q % 2 == 0:
    q -= 1
  
  z = 0
  while q.bit_length() >= 1000:
    z += 1
    if z % 100 == 0:
      print(z)
    if not isPrime(q):
      q -= 2
      continue
    print("here?")
    p = q * r * 2 + 1
    if not isPrime(p):
      q -= 2
      continue
    
    return p, q

  return -1, -1

def query(p, q):
  c.sendlineafter(b'>', hex(p)[2:].encode())
  c.sendlineafter(b'>', hex(q)[2:].encode())
  c.recvuntil(b' = ')
  g = int(c.recvline(), 16)
  c.recvuntil(b' = ')
  y = int(c.recvline(), 16)
  return g, y
  
c = process(['python3', 'prob.py'])

small_primes = prime_range(1,10**6)
small_primes = small_primes[::-1]
#q_lists = preprocess()

crt_a = []
crt_m = []

def preprocess():
  small_primes = prime_range(1,10**6)
  small_primes = small_primes[::-1]
  go = 0
  while go < 70:
    q = getPrime(1000)
    for r in small_primes:
      p = 2 * r * q + 1
      if isPrime(int(p)):
        break

    else:
      continue

    small_primes.remove(r)
    g, y = query(p, q)
    base = pow(g, 2*q, p)
    if base == 1:
      continue

    L = [p,q,r]
    f = open("preprocess.txt", "a")
    f.write(str(L) + '\n')
    f.close()
    go += 1

# preprocess()

L = []
for line in open("preprocess.txt").readlines():
  z = eval(line)  
  L.append(z)

idx = 0
while prod(crt_m) < 2 ** 1020:
  p,q,r = L[idx]
  idx += 1
  g, y = query(p, q)
  base = pow(g, 2*q, p)
  if base == 1:
    continue

  target = pow(y, 2*q, p)

  mul = 1
  for i in tqdm(range(r)):
    if mul == target:
      crt_a.append(i)
      crt_m.append(r)
      break
    mul = mul * base % p

  print(int(prod(crt_m)).bit_length(), "/ 1020")


ans = crt(crt_a, crt_m)
print(long_to_bytes(ans))

c.close()