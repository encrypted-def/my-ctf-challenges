from pwn import *

r = remote('localhost', 9001)

r.sendline(b'42')

# DES weak key
for i in range(21):
    r.sendline(b'1fe01ee10ef10ff0')
    r.sendline(b'e01fe11ef10ef00f')

r.recvuntil(b"enc : ")
print(r.recv().decode())