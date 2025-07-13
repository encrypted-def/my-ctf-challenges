import Character

from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad
import hashlib
import random
import string
import os
from pwn import *

random.seed(int(42))

EAT_COMMAND = int(1)
PWN_COMMAND = int(2)
SLEEP_COMMAND = int(3)
DATE_COMMAND = int(4)
SAVE_COMMAND = int(5)

GF.<a> = GF(2^128, modulus=x^128 + x^7 + x^2 + x + 1)
#P.<x> = PolynomialRing(F)

def int_to_GF(n):
    return GF([(n >> i) & 1 for i in range(127, -1, -1)])

def GF_to_int(elem):
    n = elem.to_integer()
    ans = 0
    for i in range(128):
        ans <<= 1
        ans |= ((n >> i) & 1)
    return ans

def bytes_to_GF(b):
    assert len(b) == 16
    return int_to_GF(int.from_bytes(b, 'big'))

def GF_to_bytes(elem):
    n = GF_to_int(elem)
    return int(n).to_bytes(16, 'big')

def GHASH(H, a, c):
    assert len(a) % 16 == 0, len(c) % 16 == 0
    block_int = int(((8*len(a)) << 64) + 8 * len(c))

    ret = int_to_GF(0)
    for i in range(0, len(a), 16):
        block = a[i:i+16]
        block_gf = bytes_to_GF(block)
        ret = (ret + block_gf) * H

    for i in range(0, len(c), 16):
        block = c[i:i+16]
        block_gf = bytes_to_GF(block)
        ret = (ret + block_gf) * H

    block_gf = int_to_GF(block_int)
    ret = (ret + block_gf) * H

    return ret

def get_tag(key, nonce, ct, aad = b''):
    assert len(nonce) == 12
    y0 = nonce + bytes.fromhex('00000001')
    cipher = AES.new(key, AES.MODE_ECB)
    H = bytes_to_GF(cipher.encrypt(b'\x00'*16))
    tag_gf = GHASH(H, aad, ct) + bytes_to_GF(cipher.encrypt(y0))
    tag = GF_to_bytes(tag_gf)
    return tag

def get_tag_test():
    key = b'\x01'*16
    nonce = b'\x00'*12

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    pt = b'\x00'*16
    ct, tag = cipher.encrypt_and_digest(pt)
    tag2 = get_tag(key, nonce, ct, b'')
    assert tag == tag2

def forge():
    pw1 = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, k=20))
    pw1_hash = hashlib.sha256(pw1.encode()).digest()
    key1 = pw1_hash[:16]
    cipher1_ecb = AES.new(key1, AES.MODE_ECB)
    #cipher1_gcm = AES.new(key1, AES.MODE_GCM, nonce=nonce)
    pw2 = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, k=20))
    pw2_hash = hashlib.sha256(pw2.encode()).digest()
    key2 = pw2_hash[:16]
    cipher2_ecb = AES.new(key2, AES.MODE_ECB)
    #cipher2_gcm = AES.new(key2, AES.MODE_GCM, nonce=nonce)

    pt1 = b'\xfe\x00' # nickname len = 0xfe
    pt1 += b'a' * 0xfe # arbitrary long nickname
    pt1 += int(0).to_bytes(4, 'little') # day
    pt1 += int(100).to_bytes(4, 'little') # stamina
    pt1 += int(0).to_bytes(4, 'little') # intelligence
    pt1 += int(0).to_bytes(4, 'little') # friendship
    pt1 += bytes([16]*16) # padding
    
    pt1 = bytearray(pt1)

    print("Step 1. Determine ID(to fix nonce)")
    cnt = 0
    while True:
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)

        #ID = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, k=20))
        ID = 'FIcnzaUNeKHEbCrdvfQl'
        id_hash = hashlib.sha256(ID.encode()).digest()
        nonce = id_hash[:12]

        first_block_plain = nonce + bytes.fromhex('00000002')
        pt1_first_block = cipher1_ecb.encrypt(first_block_plain)
        pt2_first_block = cipher2_ecb.encrypt(first_block_plain)
        first_block_xor = strxor(pt1_first_block, pt2_first_block)

        last_block_plain = nonce + int(len(pt1)//16 + 1).to_bytes(4, 'big')
        pt1_last_block = cipher1_ecb.encrypt(last_block_plain)
        pt2_last_block = cipher2_ecb.encrypt(last_block_plain)
        last_block_xor = strxor(pt1_last_block, pt2_last_block)
        
        # nickname len is 0x0e and last padding is 0x01
        if (first_block_xor[1] ^^ pt1[1]) != 0:
            continue
        
        if (last_block_xor[-1] ^^ pt1[-1]) != 1:
            continue

        if (first_block_xor[0] ^^ pt1[0]) != 14:
            continue
        
        print(f"{ID = }")
        break

    print("Step 2. control intelligence and friendship in pt2")
    # nickname field in pt2 : 0-15B( = 1 block)
    # day : 16-19B
    # stamina = 20-23B 
    # intelligence = 24-27B, must be 0xffffffff
    # friendship = 28-31B, must be 0x21000000
    second_block_plain = nonce + bytes.fromhex('00000003')
    pt1_second_block = cipher1_ecb.encrypt(second_block_plain)
    pt2_second_block = cipher2_ecb.encrypt(second_block_plain)
    second_block_xor = strxor(pt1_second_block, pt2_second_block)
    # second_block_xor[8:12] ^^ pt1[24:28] = 0x7fffffff
    # -> pt1[24:28] = second_block_xor[8:12] ^^ 0xffffffff
    
    pt1[24] = second_block_xor[8] ^^ 0xff
    pt1[25] = second_block_xor[9] ^^ 0xff
    pt1[26] = second_block_xor[10] ^^ 0xff
    pt1[27] = second_block_xor[11] ^^ 0xff
    pt1[28] = second_block_xor[12] ^^ 0x21
    pt1[29] = second_block_xor[13] ^^ 0x00
    pt1[30] = second_block_xor[14] ^^ 0x00
    pt1[31] = second_block_xor[15] ^^ 0x00

    
    print("Step 3. make a tag as same")
    cipher1_gcm = AES.new(key1, AES.MODE_GCM, nonce=nonce)
    ct1 = cipher1_gcm.decrypt(pt1)

    # Making a tag as same by modifying 3rd blocks
    tag1 = bytes_to_GF(get_tag(key1, nonce, ct1))
    tag2 = bytes_to_GF(get_tag(key2, nonce, ct1))

    block_size = len(ct1) // 16
    H1 = bytes_to_GF(cipher1_ecb.encrypt(b'\x00'*16))
    H2 = bytes_to_GF(cipher2_ecb.encrypt(b'\x00'*16))

    block3_GF = (tag2 - tag1) * (H1 ^ (block_size-1) - H2 ^(block_size-1))^(-1)
    assert H1^(block_size - 1) * block3_GF + tag1 == H2^(block_size - 1) * block3_GF + tag2
    block3 = GF_to_bytes(block3_GF)

    pt1[32:48] = strxor(pt1[32:48], block3)

    print("Step 4. Verify everything.")
    cipher1_gcm = AES.new(key1, AES.MODE_GCM, nonce=nonce)
    #cipher2_gcm = AES.new(key2, AES.MODE_GCM, nonce=nonce)
    ct1 = cipher1_gcm.decrypt(pt1)
    tag1 = get_tag(key1, nonce, ct1)
    tag1_GF = bytes_to_GF(tag1)
    tag2 = get_tag(key2, nonce, ct1)
    assert tag1 == tag2, "tag is not matched"

    cipher1_gcm = AES.new(key1, AES.MODE_GCM, nonce=nonce)
    pt1 = cipher1_gcm.decrypt_and_verify(ct1, tag1)
    cipher2_gcm = AES.new(key2, AES.MODE_GCM, nonce=nonce)
    pt2 = cipher2_gcm.decrypt_and_verify(ct1, tag2)

    assert pt2[0] == 0x0e
    assert pt2[1] == 0
    assert pt2[-1] == 1
    assert pt2[24] == 0xff
    assert pt2[25] == 0xff
    assert pt2[26] == 0xff
    assert pt2[27] == 0xff
    assert pt2[28] == 0x21

    print("all passed!")
    
    return ID, pw1, pw2, ct1, pt1, pt2, tag1

def encrypt_data(ID, PW, character):
    id_hash = hashlib.sha256(ID.encode()).digest()
    pw_hash = hashlib.sha256(PW.encode()).digest()
    nonce = id_hash[:12]
    file_name = id_hash[16:24].hex()
    key = pw_hash[:16]
    cipher = AES.new(key, AES.MODE_GCM, nonce)

    file_data = b''
    file_data += len(character.nickname).to_bytes(2, 'little')
    file_data += character.nickname.encode()
    file_data += int(character.day).to_bytes(4, 'little')
    file_data += int(character.stamina).to_bytes(4, 'little')
    file_data += int(character.intelligence).to_bytes(4, 'little')
    file_data += int(character.friendship).to_bytes(4, 'little')

    file_data = pad(file_data, 16)
    file_data_enc, tag = cipher.encrypt_and_digest(file_data)
    return file_data_enc, tag


print("(A). Finding godgets...")
ID, pw1, pw2, ct1, pt1, pt2, tag1 = forge()


print("\n(B). Initialize server's save file")
r = remote("localhost", int(9001))
# Initialize server's save file first
pw3 = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, k=20)) + os.urandom(10).hex() # meaningless
r.send(len(ID).to_bytes(2, 'little') + ID.encode())
r.send(len(pw3).to_bytes(2, 'little') + pw3.encode())
status = r.recv(1)
assert status == b'\x02', status # LOAD_FAIL
nickname = 'asdfadsf' # whatever..
r.send(len(nickname).to_bytes(2, 'little') + nickname.encode())
r.send(SAVE_COMMAND.to_bytes(1, 'little'))

c = Character.Character()
c.nickname = nickname
c.stamina = 100
file_data_enc, tag = encrypt_data(ID, pw3, c)

r.send(len(file_data_enc).to_bytes(2, 'little') + file_data_enc)
r.send(tag)

status = r.recv(1)
assert status == b'\x0B', status # SAVE_SUCCESS
r.close()

print("\n(C). Add malicious save file into server")
r = remote("localhost", int(9001))
r.send(len(ID).to_bytes(2, 'little') + ID.encode())
r.send(len(pw1).to_bytes(2, 'little') + pw1.encode())
status = r.recv(1)
assert status == b'\x02', status # LOAD_FAIL
nickname = pt1[2:256]
r.send(len(nickname).to_bytes(2, 'little') + nickname)
r.send(SAVE_COMMAND.to_bytes(1, 'little'))

r.send(len(ct1).to_bytes(2, 'little') + ct1)
r.send(tag1)

status = r.recv(1)
assert status == b'\x0B', status # SAVE_SUCCESS
r.close()

print("\n(D). Load malicious save file into server, with second key")
r = remote("localhost", int(9001))
r.send(len(ID).to_bytes(2, 'little') + ID.encode())
r.send(len(pw2).to_bytes(2, 'little') + pw2.encode())
status = r.recv(1)
assert status == b'\x01', status # LOAD_SUCCESS

nickname_len = int.from_bytes(r.recv(2), 'little')
nickname = r.recv(nickname_len).decode()
day = int.from_bytes(r.recv(4), 'little')
stamina = int.from_bytes(r.recv(4), 'little')
intelligence = int.from_bytes(r.recv(4), 'little')
friendship = int.from_bytes(r.recv(4), 'little')

print("\n(E). friendship +1, then get flag")
r.send(PWN_COMMAND.to_bytes(1, 'little'))
rnd = int.from_bytes(r.recv(1), 'little')

r.send(DATE_COMMAND.to_bytes(1, 'little'))
rnd = int.from_bytes(r.recv(1), 'little')
assert rnd != 0, rnd

flag_len = int.from_bytes(r.recv(2), 'little')
flag = r.recv(flag_len).decode()
print(flag)