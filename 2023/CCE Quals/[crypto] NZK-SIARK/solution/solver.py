from pwn import *
from tqdm import tqdm
from constants import Rcon, Sbox
from GF import GF

Inv = [0]*256
for i in range(1, 256):
    for j in range(1,256):
        if GF(i) * GF(j) == GF(1):
            Inv[i] = j
            break

def forge_sbox(target):
    for v in range(256):
        xinv = GF(v)
        z = xinv + xinv.lrotate(1) + xinv.lrotate(2) + xinv.lrotate(3) + xinv.lrotate(4) + GF(99)
        if z == target:
            return v
    assert(0)

def sbox_query(out = -1):
    r.recvuntil(b"inv(")
    x = int(r.recv(2).decode(), 16)
    r.recvuntil(b" > ")
    if out == -1:
        r.sendline(hex(Inv[x])[2:].encode())
    else:
        r.sendline(hex(out)[2:].encode())


def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] = state[i][j] + round_key[i][j]

def shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]

def inv_shift_rows(state):
    shift_rows(state)
    shift_rows(state)
    shift_rows(state)    

def mix_columns(state):
    mat = [[GF(2), GF(3), GF(1), GF(1)],
           [GF(1), GF(2), GF(3), GF(1)],
           [GF(1), GF(1), GF(2), GF(3)],
           [GF(3), GF(1), GF(1), GF(2)]]
    tmp = [GF(0) for _ in range(4)]
    for j in range(4):
        for i in range(4):
            tmp[i] = mat[i][0] * state[0][j] + mat[i][1] * state[1][j] + mat[i][2] * state[2][j] + mat[i][3] * state[3][j]
        for i in range(4):
            state[i][j] = tmp[i]

def inv_mix_columns(state):
    mat = [[GF(14), GF(11), GF(13), GF(9)],
           [GF(9), GF(14), GF(11), GF(13)],
           [GF(13), GF(9), GF(14), GF(11)],
           [GF(11), GF(13), GF(9), GF(14)]]
    tmp = [GF(0) for _ in range(4)]
    for j in range(4):
        for i in range(4):
            tmp[i] = mat[i][0] * state[0][j] + mat[i][1] * state[1][j] + mat[i][2] * state[2][j] + mat[i][3] * state[3][j]
        for i in range(4):
            state[i][j] = tmp[i]



def get_sbox(x):
    return GF(Sbox[x.val])

def key_schedule(round_keys, KEY):
    for i in range(4):
        for j in range(4):
            round_keys[i][j].val = KEY[i + 4*j]

    for i in range(4, 4*ROUNDS+4):
        if i % 4 == 0:
            round_keys[0][i] = round_keys[0][i-4] \
                            + get_sbox(round_keys[1][i-1]) \
                            + GF(Rcon[i // 4])

            for j in range(1, 4):
                round_keys[j][i] = round_keys[j][i-4] \
                                + get_sbox(round_keys[(j+1)%4][i-1])
        
        else:
            for j in range(4):
                round_keys[j][i] = round_keys[j][i-4] + round_keys[j][i-1]


r = process(["python3", "./prob.py"])

r.recvuntil(b"(")
plain = bytes.fromhex(r.recvuntil(b")").decode()[:-1])
r.recvuntil(b"= ")
cipher = bytes.fromhex(r.recvline().decode().strip())

r.recvuntil(b" > ")
key = plain

r.sendline(key.hex().encode())

ROUNDS = 10
round_keys = [[GF(0) for i in range(4 * (ROUNDS + 1))] for j in range(4)]

key_schedule(round_keys, key)


# KEY SCHEDULE

r.recvline() # ### Key schedule ###

for _ in range(ROUNDS * 4):
    sbox_query()

# ENCRYPTION
r.recvline() 

'''
SubBytes
[I1]
ShiftRows
[I2]
MixColumns
[I3]
AddRoundKey
[I4 = [00 00 00 ... 00]]
'''

# [[round_keys[z][j] for j in range(4*i+4, 4*i+8)] for z in range(4)]

for i in range(9):
    state = [[round_keys[z][j] for j in range(4*i+4, 4*i+8)] for z in range(4)] # I3
    inv_mix_columns(state) # I2
    inv_shift_rows(state) # I1

    for a in range(4):
        for b in range(4):
            sbox_query(forge_sbox(state[a][b]))

    print(f"ROUND {i+1} DONE")


'''
SubBytes
[I1]
ShiftRows
[I2]
AddRoundKey
[I3 = CIPHERTEXT]
'''
for i in range(4):
    for j in range(4):
        state[i][j].val = cipher[i + 4*j]

add_round_key(state, [[round_keys[z][j] for j in range(4*ROUNDS, 4*ROUNDS+4)] for z in range(4)]) # I2
inv_shift_rows(state) # I1

for a in range(4):
    for b in range(4):
        sbox_query(forge_sbox(state[a][b]))

print(r.recv())