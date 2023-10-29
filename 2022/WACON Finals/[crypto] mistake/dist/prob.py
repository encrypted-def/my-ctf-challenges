from Crypto.Util.number import *


P = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff72ef
g = 5
a = 0xe86680d8ebd7cfec4d29118f1b470ce6f0dfdba9ef2b2d217fc4f9cbe21b974c
b = 0x34b368d265d16df26ea6bc6c04c24b3f7e8885cdac2f722de6141e6e4c17a110
c = 0x1cb0bc561d53c36847e0cb2b66484d8ece75eb937f84b6ac43e81a74332d14f5

def encrypt(x, index):
    assert(x < P-1)
    return (pow(g, x, P) + a * index ** 2 + b * index + c) % P

fr = open("flag.bmp", "rb")
plain = fr.read()
fw = open("flag.bmp.enc", "wb")

SIZE = 32
for i in range(0, len(plain), 32):
    block = bytes_to_long(plain[i:i+32])
    fw.write(long_to_bytes(encrypt(block, i), 32))

fw.close()




# BMP_HEADER_LEN = 0x36