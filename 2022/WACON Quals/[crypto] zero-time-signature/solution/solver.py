import hashlib
import os

from pwn import *

def forward(msg, step):
    for _ in range(step):
        msg = hashlib.sha256(msg).digest()
    return msg

MESSAGE_LEN = 18
SPELL = 'gimme a flag plz^^'
FLAG = 'flag{afsdfadfads}'

r = remote('localhost', 9001)

pub = []
for i in range(MESSAGE_LEN+1):
    x = r.recvline().split(b'=')[1].strip()
    pub.append(bytes.fromhex(x.decode()))

r.recvuntil('>')
msg = chr(256)*(MESSAGE_LEN-1) + chr(512)
r.sendline(msg)

sig1 = []
for i in range(MESSAGE_LEN+1):
    x = r.recvline().split(b'=')[1].strip()
    sig1.append(bytes.fromhex(x.decode()))

sig2 = []
tot = sum(ord(c) for c in SPELL)
for i, c in enumerate(SPELL):
    if i != len(SPELL) - 1:
        sig2.append(forward(sig1[i], 256 - ord(c)))
    else:
        sig2.append(forward(sig1[i], 255 - ord(c)))
sig2.append(forward(sig1[MESSAGE_LEN], tot - 255))

for i in range(MESSAGE_LEN+1):
    r.recvuntil('>')
    r.sendline(sig2[i].hex())

r.interactive()