from Crypto.Util.number import *
import os
from hashlib import sha256
from tqdm import tqdm

def cascade_hash(msg, cnt, digest_len):
    assert digest_len <= 32
    msg = msg * 10
    for _ in range(cnt):
        msg = sha256(msg).digest()
    return msg[:digest_len]

def seed_to_permutation(seed):
    permutation = ''
    msg = seed + b"_shuffle"
    while len(permutation) < 16:
        msg = cascade_hash(msg, 777, 32)
        msg_hex = msg.hex()
        for c in msg_hex:
            if c not in permutation:
                permutation += c

    return permutation


def permutation_secret_sharing_gen(secret):
    seed_len = 5
    master_seed = os.urandom(seed_len)
    seed_tree = [None] * (2*N - 1)
    seed_tree[0] = master_seed
    for i in range(N-1):
        h = cascade_hash(seed_tree[i], 123, 2 * seed_len)
        seed_tree[2*i+1], seed_tree[2*i+2] = h[:seed_len], h[seed_len:]
    
    secret_list = list(secret.decode()) # ex) ['0','1','2','3',...]
    for i in range(N):
        # i-th party has a permutation derived from seed_tree[i+N-1]
        permutation = seed_to_permutation(seed_tree[i + N - 1])
        secret_list = [hex(permutation.find(x))[2:] for x in secret_list]

    permutated_secret = ''.join(secret_list)
    hidden_party = os.urandom(1)[0] & 7
    proof_idxs = merkle_proof_indexes[hidden_party]

    return seed_tree[proof_idxs[0]] + \
           seed_tree[proof_idxs[1]] + \
           seed_tree[proof_idxs[2]] + \
           bytes([hidden_party]) + \
           bytes.fromhex(permutated_secret)

N = 8 # Number of parties

merkle_proof_indexes = {
    0 : [2,4,8],
    1 : [2,4,7],
    2 : [2,3,10],
    3 : [2,3,9],
    4 : [1,6,12],
    5 : [1,6,11],
    6 : [1,5,14],
    7 : [1,5,13]
}

fr = open("pss_data", "rb")
merkle_proofs = []
hidden_parties = []
permutated_secrets = []

sibling = {}

for i in range(2 ** 17):
    dat = fr.read(24)
    merkle_proofs.append([dat[0:5], dat[5:10], dat[10:15]])
    hidden_parties.append(dat[15])
    permutated_secrets.append(dat[16:24])
    sibling[(merkle_proofs[-1][2], (hidden_parties[-1]+1)%2)] = i

seed_len = 5
# About 2 ** 24 trials?
for i in tqdm(range(2**24)):
    #parent_seed = long_to_bytes(i, 5)
    parent_seed = bytes.fromhex('0000fc1eed')
    h = cascade_hash(parent_seed, 123, 2 * seed_len)
    h_left, h_right = h[:5], h[5:]

    if (h_left, 0) in sibling:
        idx = sibling[(h_left,0)]
        print(hex(i), "LEFT", idx)
    
    elif (h_right, 1) in sibling:
        idx = sibling[(h_right,1)]
        print(hex(i), "RIGHT", idx)

    else:
        continue
    
    hidden_party = hidden_parties[idx]
    seed_tree = [None] * (2*N - 1)
    seed_tree[(merkle_proof_indexes[hidden_party][2] - 1) // 2] = parent_seed
    seed_tree[merkle_proof_indexes[hidden_party][0]] = merkle_proofs[idx][0]
    seed_tree[merkle_proof_indexes[hidden_party][1]] = merkle_proofs[idx][1]
    for i in range(N-1):
        if not seed_tree[i]:
            continue
        h = cascade_hash(seed_tree[i], 123, 2 * seed_len)
        seed_tree[2*i+1], seed_tree[2*i+2] = h[:seed_len], h[seed_len:]

    for i in range(N):
        assert seed_tree[i + N - 1]

    permutated_secret = permutated_secrets[idx].hex()
    secret_list = list(permutated_secret) # ex) ['0','1','2','3',...]
    for i in range(N-1,-1,-1):
        # i-th party has a permutation derived from seed_tree[i+N-1]
        permutation = seed_to_permutation(seed_tree[i + N - 1])
        secret_list = [permutation[int(x,16)] for x in secret_list]

    secret_cand = ''.join(secret_list).encode()
    print("candidates", secret_cand)
    flag_cand = b"WACON2023{" + secret_cand + b'}'
    if cascade_hash(flag_cand, 0xbeeeef, 32).hex() == 'f7a5108a576391671fe3231040777e9ac455d1bb8b84a16b09be1b2bac68345c':
        print(flag_cand)
        print(parent_seed.hex())
        exit()

# parent_seed 0000fc1eed
# flag WACon2023{2d4b7a9c085316ef}