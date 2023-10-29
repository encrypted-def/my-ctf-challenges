from pwn import *

import random

#context.log_level = 'debug'

#r = process(["sage", "./prob.sage"])
r = remote("localhost", int(2905))

N = 256
ROUNDS = 128

matrices = [matrix(GF(2), N, N) for _ in range(ROUNDS)]
vectors = [vector(GF(2), N) for _ in range(ROUNDS)]

def bytes_to_vector(b):
    vec = vector(GF(2), N)
    assert len(b) == N // 8
    for i in range(len(b)):
        tmp = b[i]
        for j in range(8):
            vec[8*i+7-j] = tmp & 1
            tmp >>= 1
    return vec

def vector_to_bytes(vec):
    assert len(vec) == N
    b = bytearray(N // 8)
    for i in range(len(b)):
        for j in range(8):
            b[i] = (b[i] << 1) | int(vec[8*i + j])
    return b

def encrypt_oracle(plain):
    plain_b = vector_to_bytes(plain)
    r.recvuntil(b" > ")
    r.sendline(plain_b.hex().encode())
    r.recvuntil(b" > ")
    cipher_b = bytes.fromhex(r.recv(64).decode())
    return bytes_to_vector(cipher_b)

def answer_oracle(ans_list):
    for i in range(len(ans_list)):
        r.recvuntil(b" > ")
        r.sendline(str(ans_list[i][0]).encode()) # index
        if ans_list[i][0] != -1:
            r.recvuntil(b" > ")
            r.sendline(str(ans_list[i][1]).encode()) # value

def load_constants():
    f = open("constants.txt", "r")
    for r in range(ROUNDS):
        for i in range(N):
            row = f.readline()
            for j in range(N):
                matrices[r][i,j] = int(row[j])

        row = f.readline()
        for i in range(N):            
            vectors[r][i] = int(row[i])

# 1-127R의 x1, x2에는 입력 차분이 0이고 128R의 x1, x2에는 입력 차분이 delta_x1, delta_x2이게 하는 입력 차분
def get_input_diff(delta_x1, delta_x2):
    init_mat = matrix(GF(2), N, N)
    for i in range(N):
        init_mat[i,i] = 1
    
    constraint_mat = matrix(GF(2), N, N)
    for r in range(ROUNDS):
        for i in range(N):
            constraint_mat[2*r+0,i] = init_mat[1,i]
            constraint_mat[2*r+1,i] = init_mat[2,i]
        init_mat = matrices[r] * init_mat

    target = vector(GF(2), N)
    target[N-2] = delta_x1
    target[N-1] = delta_x2

    return constraint_mat.inverse() * target

def get_random_vector(n):
    vec = vector(GF(2), n)
    for i in range(n):
        vec[i] = random.randint(0,1)
    return vec
    
load_constants()

diff10 = get_input_diff(1,0)
diff01 = get_input_diff(0,1)
diff11 = get_input_diff(1,1)

success = 0

while success < 256:
    print(f"{success}/256")

    random_plain = get_random_vector(N)

    cipher0 = encrypt_oracle(random_plain)
    cipher1 = encrypt_oracle(random_plain + diff10)
    cipher2 = encrypt_oracle(random_plain + diff01)
    cipher3 = encrypt_oracle(random_plain + diff11)

    # remove last linear layer
    cipher0 = matrices[-1].inverse() * (cipher0 + vectors[-1])
    cipher1 = matrices[-1].inverse() * (cipher1 + vectors[-1])
    cipher2 = matrices[-1].inverse() * (cipher2 + vectors[-1])
    cipher3 = matrices[-1].inverse() * (cipher3 + vectors[-1])

    # x1 : plain을 암호화했을 때 마지막 라운드의 입력 중 1번째 비트
    # x2 : plain을 암호화했을 때 마지막 라운드의 입력 중 2번째 비트
    # delta_x0 = delta_x1
    # (k1,k2) 가능한 후보 4가지를 확인
    cand = []
    for (k1,k2) in ((0,0),(0,1),(1,0),(1,1)):
        x1 = cipher0[1] + k1
        x2 = cipher0[2] + k2

        chk = True
        for i, (delta_x1, delta_x2) in enumerate(((1,0),(0,1),(1,1))):
            if i == 0:
                cipher_prime = cipher1
            elif i == 1:
                cipher_prime = cipher2
            else:
                cipher_prime = cipher3

            delta_x0 = delta_x1
            x1_prime = x1 + delta_x1
            x2_prime = x2 + delta_x2
            v = cipher0[0] + cipher_prime[0] + (delta_x0 + x1_prime * x2_prime)
            if cipher0[0] + cipher_prime[0] + (delta_x0 + x1_prime * x2_prime) != 0:
                chk = False
                break

        if chk:
            cand.append([k1,k2])

    if len(cand) != 1:
        ans = [(-1,-1)]
    else:
        ans = [(1, cand[0][0]), (2, cand[0][1]), (-1, -1)]
        success += 2
    answer_oracle(ans)

r.interactive()