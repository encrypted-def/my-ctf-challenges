#!/usr/bin/python3
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def aes_enc(pt : bytes, key : bytes):
    pt_pad = pad(pt, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pt_pad)

def aes_dec(ct : bytes, key : bytes):
    cipher = AES.new(key, AES.MODE_ECB)
    pt_pad = cipher.decrypt(ct)
    return unpad(pt_pad, 16)

def input_enc(session_key : bytes) -> str:
    dat_enc = bytes.fromhex(input())
    return aes_dec(dat_enc, session_key).decode()

def print_enc(session_key : bytes, data : bytes):
    data_enc = aes_enc(data.encode(), session_key)
    print(data_enc.hex())

def key_parser(client_id : str):
    try:
        f = open(f"{client_id}/key.txt")
        enc_p = f.readline()[:-1]
        enc_q = f.readline()[:-1]
        enc_d = f.readline()[:-1]
        enc_u = f.readline()[:-1]
        n = int(f.readline())        
        f.close()
    except:
        print("[-] Error has been occured during key parsing. Please try later.")
        exit(-1)

    return enc_p, enc_q, enc_d, enc_u, n


def login():
    client_id = input()
    if not client_id.islower():
        print("[-] Only lowercase alphabet is allowed in ID")
        exit(-1)

    if os.path.exists(client_id): # Already registered
        enc_p, enc_q, enc_d, enc_u, n = key_parser(client_id)
        print(f"Hi {client_id}! Glad to see you again")
        print(enc_p)
        print(enc_q)
        print(enc_d)
        print(enc_u)   

    else: # Not registered account
        print(f"Hi {client_id}! To create an account, please send your RSA private key encrypted with your pw")
        enc_p = input()
        enc_q = input()
        enc_d = input()
        enc_u = input()
        n = int(input())
        try:
            os.makedirs(client_id)
            os.makedirs(f"{client_id}/src")
            f = open(f"{client_id}/key.txt", 'w')
            f.write(enc_p + '\n')
            f.write(enc_q + '\n')
            f.write(enc_d + '\n')
            f.write(enc_u + '\n')
            f.write(str(n) + '\n')
            f.close()
        except:
            print("Error has been occured during key storing. Please try later.")
            exit(-1)        
        print("Key is successfully saved")
    
    return client_id, n, 65537
            
def gen_and_send_session_key(n, e):
    session_key = os.urandom(32)
    while True:
        prefix_padding = os.urandom(1)
        if prefix_padding != b'\x00':
            break
    postfix_padding = os.urandom(256 - 32 - 1 - 1)
    rsa_plain = bytes_to_long(prefix_padding + session_key + postfix_padding)
    rsa_enc_session_key = long_to_bytes(pow(rsa_plain, e, n))
    print(rsa_enc_session_key.hex())
    return session_key

def save_file(session_key : bytes, client_id : str):
    name = input_enc(session_key)
    if name == "BACK":
        return False
    if not name.islower():
        print_enc(session_key, "Invalid filename")
        return False
    print_enc(session_key, "OK")
    try:
        data_hex = input_enc(session_key)
        if data_hex == "BACK":
            return False
        data = bytes.fromhex(data_hex)
        if len(data) > 1000:
            print_enc(session_key, "File too large")
            return False
    except:
        print_enc(session_key, "Wrong hex data")
        return False
    
    try:
        filepath = f"{client_id}/src/{name}.enc"
        if os.path.exists(filepath):
            print_enc(session_key, "File already exists")
            return False
        f = open(filepath, "wb")
        f.write(data)
        f.close()
    
    except:
        print_enc(session_key, "Failed to save a file")
        return False

    print_enc(session_key, "OK")
    return True
    

def load_file(session_key : bytes, client_id : str):
    name = input_enc(session_key)
    if name == "BACK":
        return False
    if not name.islower():
        print_enc(session_key, "Invalid filename")
        return False
    
    try:
        filepath = f"{client_id}/src/{name}.enc"
        data_enc = open(filepath, "rb").read()
    except:
        print_enc(session_key, "File does not exist")
        return False

    print_enc(session_key, "OK")
    print_enc(session_key, data_enc.hex())
    return True

def menu(session_key : bytes, client_id : str):
    while True:
        c = input_enc(session_key)
        if c == 'save_file':
            save_file(session_key, client_id)
        elif c == 'load_file':
            load_file(session_key, client_id)
        elif c == 'logout':
            exit(-1)
        else:
            print("Wrong choice.")
            exit(-1)


def go():
    client_id, n, e = login()
    session_key = gen_and_send_session_key(n, e)
    menu(session_key, client_id)

go()