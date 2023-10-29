from pwn import *

r = remote('localhost', 9001)

r.sendline(b'4886674138783273204')
r.recvuntil(b"0\n")
print(r.recv())
