import requests
import hashlib, json
from pwn import *

def get_block_raw(hash):
    url = f'https://blockstream.info/testnet/api/block/{hash}/raw'
    resp = requests.get(url)
    return resp.content

def get_block_header(hash):
    url = f'https://blockstream.info/testnet/api/block/{hash}/header'
    resp = requests.get(url)
    return resp.text

def get_transaction_raw(txid):
    url = f'https://blockstream.info/testnet/api/tx/{txid}/hex'
    resp = requests.get(url)
    return bytes.fromhex(resp.text)

def get_transaction_info(txid):
    url = f'https://blockstream.info/testnet/api/tx/{txid}'
    resp = requests.get(url)
    return json.loads(resp.text)

def get_merkle_proof(txid):
    url = f'https://blockstream.info/testnet/api/tx/{txid}/merkle-proof'
    resp = requests.get(url)
    return json.loads(resp.text)

def sha256(x):
    return hashlib.sha256(x).digest()

def sha256_double(x):
    return sha256(sha256(x))

# Eliminate [marker], [flag], and [witness]
# https://bitcoin.stackexchange.com/questions/77699/whats-the-difference-between-txid-and-hash-getrawtransaction-bitcoind
def txid_processed_data(x, witness):
    dat = b''
    dat = x[:4] + x[6:]
    idx = dat.find(witness)
    dat = dat[:idx-2] + dat[-4:]
    return dat

def interact(r, dat, rev):
    r.recvuntil(b'data > ')
    r.sendline(dat)
    r.recvuntil(b'reverse?(y/n) > ')
    r.sendline(rev)
    r.recvuntil(b'seed = ')
    seed = r.recvline().strip().decode()
    return seed

def solve(txid):
    # 1. Transaction
    x = get_transaction_raw(txid)
    info_json = get_transaction_info(txid)
    witness = bytes.fromhex(info_json['vin'][0]['witness'][0])
    dat = txid_processed_data(x, witness)
    #assert(sha256_double(dat)[::-1] == bytes.fromhex(txid))
    seed = interact(r, dat.hex().encode(), b'n')
    seed = interact(r, seed.encode(), b'n')
    
    # 2. Merkle tree
    merkle_json = get_merkle_proof(txid)  
    merkle_list = merkle_json['merkle']
    merkle_pos = merkle_json['pos']
    for i in range(len(merkle_list)):
        if merkle_pos % 2 == 0:
            seed = seed + bytes.fromhex(merkle_list[i])[::-1].hex()
        else:
            seed = bytes.fromhex(merkle_list[i])[::-1].hex() + seed
        seed = interact(r, seed.encode(), b'n')
        seed = interact(r, seed.encode(), b'n')
        merkle_pos //= 2
    
    # 3. Block header
    block_header = get_block_header(info_json['status']['block_hash'])
    seed = interact(r, block_header, b'n')
    seed = interact(r, seed.encode(), b'y')
    print("seed is ", seed)
    r.interactive()


r = remote('localhost', 9001)
r.sendline(b'_0BaAaAaAaRk1nGd09{^o^}*') # phrase = _0BaAaAaAaRk1nGd09{^o^}*
r.recvuntil(b'seed = ')
seed = r.recvline().strip()
print("seed", seed)
# 1. Convert seed to Bech32 address
# 2. Receive a testnet coin to bech32 address using https://bitcoinfaucet.uo1.net/send.php (or anything else)
# 3. Find a txid which includes seed
# 4. Wait until transaction is included in any block
#txid = input().strip()
txid = '03ba86055ee9a2f17fae859f958b743bf8cc65b3cc62c0c4d00c3cf05b30f14e'
solve(txid)

'''
EXAMPLE
seed : d6cdeccac8d25fca16c0d6bf74de5583
transaction : 03ba86055ee9a2f17fae859f958b743bf8cc65b3cc62c0c4d00c3cf05b30f14e
'''