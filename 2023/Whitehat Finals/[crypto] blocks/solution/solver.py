from pwn import *
from Crypto.Util import strxor

ECB_MODE = 0
CBC_MODE = 1
CTR_MODE = 2
CFB_MODE = 3
OFB_MODE = 4

#context.log_level = 'debug'
#r = process(["python3", "./prob.py"])
r = remote("3.34.50.93", 4816)

BLOCK0 = bytes(16)
BLOCK1 = bytes(15) + bytes([1])

for i in range(100):
  print(f"Stage {i+1}/100")
  mode = -1
  iv1 = BLOCK0
  pt1 = BLOCK0 + BLOCK0 + BLOCK0 + BLOCK0
  r.recvuntil(b" > ") # iv
  r.sendline(iv1.hex())
  r.recvuntil(b" > ") # enc_option
  r.sendline(b'y')
  r.recvuntil(b" > ") # pt
  r.sendline(pt1.hex())
  r.recvuntil(b" = ") # ct
  ct1 = bytes.fromhex(r.recvline().decode())
  
  iv2 = BLOCK1
  ct2 = ct1[:16] + BLOCK0 + BLOCK0
  r.recvuntil(b" > ") # iv
  r.sendline(iv2.hex())
  r.recvuntil(b" > ") # enc_option
  r.sendline(b'n')
  r.recvuntil(b" > ") # ct
  r.sendline(ct2.hex())
  r.recvuntil(b" = ") # pt
  pt2 = bytes.fromhex(r.recvline().decode())

  if ct1[0:16] == ct1[16:32]:
    mode = ECB_MODE

  elif ct1[48:64] == pt2[32:48]:
    mode = CTR_MODE

  elif pt2[0:16] == BLOCK1:
    mode = CBC_MODE

  elif pt2[16:32] == ct1[16:32]:
    mode = CFB_MODE
  
  else:
    mode = OFB_MODE

  r.recvuntil(b" > ") # mode
  r.sendline(str(mode).encode())

print(r.interactive())