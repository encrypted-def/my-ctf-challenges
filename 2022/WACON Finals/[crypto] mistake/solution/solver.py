from Crypto.Util.number import *

P = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff72ef
g = 5
a = 0xe86680d8ebd7cfec4d29118f1b470ce6f0dfdba9ef2b2d217fc4f9cbe21b974c
b = 0x34b368d265d16df26ea6bc6c04c24b3f7e8885cdac2f722de6141e6e4c17a110
c = 0x1cb0bc561d53c36847e0cb2b66484d8ece75eb937f84b6ac43e81a74332d14f5

bmp_header = bytes.fromhex('424DB69670000000000036000000280000008007000001050000010018000000000080967000C40E0000C40E00000000000000000000FFFFFFFFFFFFFFFFFFFF')

fr = open("flag.bmp.enc", "rb")
cipher = fr.read()

fw = open("flag_ecbattack.bmp", "wb")
fw.write(bmp_header)

SIZE = 32
for i in range(0, len(cipher), 32):
    if i <= 1: continue # ignore header part
    block = (bytes_to_long(cipher[i:i+32]) - a * i**2 - b * i - c) % P
    fw.write(long_to_bytes(block, 32))

fw.close()




# BMP_HEADER_LEN = 0x36