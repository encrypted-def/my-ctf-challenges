import os
import des
import random
import sys

print(sys.version_info)
print("========== Constants ===========")
print(des.IP)
print(des.CP_1)
print(des.CP_2)
print(des.P)
print(des.FP)
print("===============================\n")

key = os.urandom(8)
flag = "WACON2023{" + key.hex() + "}"
print(f"flag = {flag}")
key_bits = des.bytes_to_bits(key)
for i in range(64):
    tmp_key = des.bits_to_bytes(key_bits)
    cipher = des.DES(tmp_key, 5) # ROUND NUMBER = 5
    key_bits = key_bits[1:] + key_bits[:1]
    file_pt = open(f"data_easy/pt{i}", "wb")
    file_ct = open(f"data_easy/ct{i}", "wb")
    
    random.seed(os.urandom(32))
    for _ in range(65536):
        pt = ''.join(random.choices('0123456789-', k=8)).encode()
        ct = cipher.encrypt(pt)
        file_pt.write(pt)
        file_ct.write(ct)
    
    file_pt.close()
    file_ct.close()


'''
sys.version_info(major=3, minor=10, micro=4, releaselevel='final', serial=0)
========== Constants ===========
[3, 60, 61, 15, 41, 33, 13, 14, 53, 24, 36, 4, 8, 32, 22, 39, 43, 35, 12, 50, 30, 40, 20, 21, 0, 7, 34, 51, 57, 49, 52, 37, 6, 9, 48, 47, 19, 2, 16, 18, 26, 55, 62, 58, 31, 54, 11, 17, 10, 38, 56, 29, 1, 42, 28, 25, 5, 59, 27, 44, 46, 45, 23, 63]
[19, 37, 50, 47, 8, 4, 36, 30, 55, 6, 14, 35, 44, 0, 49, 41, 26, 12, 59, 53, 17, 54, 51, 57, 5, 22, 10, 2, 16, 52, 1, 62, 46, 60, 56, 33, 21, 29, 34, 48, 27, 38, 43, 18, 32, 9, 20, 61, 3, 13, 11, 15, 58, 45, 42, 28]
[19, 34, 14, 12, 3, 5, 42, 35, 17, 40, 27, 53, 29, 18, 7, 48, 0, 20, 22, 16, 28, 45, 39, 54, 1, 2, 38, 6, 31, 47, 44, 30, 52, 25, 43, 13, 49, 50, 24, 33, 15, 10, 26, 9, 21, 8, 23, 46]
[14, 13, 16, 26, 2, 19, 5, 22, 30, 27, 24, 0, 11, 9, 29, 3, 8, 15, 25, 12, 7, 23, 17, 21, 6, 28, 18, 4, 20, 10, 31, 1]
[52, 48, 3, 46, 5, 49, 15, 37, 54, 41, 28, 4, 61, 40, 26, 24, 59, 34, 19, 27, 47, 21, 18, 43, 29, 9, 36, 35, 51, 62, 6, 45, 32, 12, 22, 56, 11, 16, 31, 50, 7, 10, 39, 2, 55, 14, 42, 13, 60, 0, 63, 25, 44, 8, 57, 20, 53, 1, 17, 38, 23, 58, 30, 33]
================================
'''