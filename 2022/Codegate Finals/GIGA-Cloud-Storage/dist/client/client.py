#!/usr/bin/python3
from Crypto.Util.number import *
import os
import socket
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
from Crypto.Cipher import AES

CREDENTIALS = {
    "codegate": "*******************"
}

def aes_enc(pt, key):
    pt_pad = pad(pt, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pt_pad)

def aes_dec(ct, key):
    cipher = AES.new(key, AES.MODE_ECB)
    pt_pad = cipher.decrypt(ct)
    return unpad(pt_pad, 16)

def packet_recv_plain(sock):
    data = b''
    while True:
        c = sock.recv(1)
        if c == b'\n':
            break
        data += c
    return data

def packet_send_plain(sock, data):
    if type(data) != bytes or b'\n' in data:
        print("[-] Invalid packet")
        exit(-1)
    sock.sendall(data + b'\n')

def packet_recv_aes_enc(sock, session_key):
    data = b''
    while True:
        c = sock.recv(1)
        if c == b'\n':
            break
        data += c
    data = data.decode()
    data = bytes.fromhex(data)
    return aes_dec(data, session_key)

def packet_send_aes_enc(sock, data, session_key):
    if type(data) != bytes or b'\n' in data:
        print("[-] Invalid packet")
        exit(-1)
    data_enc = aes_enc(data, session_key).hex().encode()
    sock.sendall(data_enc + b'\n')

# Garner's formula
def rsa_crt_dec(p, q, d, u, c):
    mp = pow(c, d % (p-1), p)
    mq = pow(c, d % (q-1), q)
    m = ((mp - mq) * u % p) * q + mq
    return m

# Derive file encryption key from RSA prvate key
def file_encryption_key(p, q, d, u):
    rsa_priv_key = long_to_bytes(p) + long_to_bytes(q) + long_to_bytes(d) + long_to_bytes(u)
    return sha256(rsa_priv_key).digest()

def login(sock):
    client_id = input("id (Only lowercase) > ")
    if not client_id.islower():
        print("[-] Invalid ID")
        exit(-1)
    if client_id in CREDENTIALS:
        client_pw = CREDENTIALS[client_id]
    else:
        client_pw = input("pw > ")
    
    sock.send(client_id.encode())

def generate_rsa_private_key():
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        e = 65537
        phi = (p-1) * (q-1)
        if phi % e == 0: continue
        if p == q: continue
        d = inverse(e, phi)
        u = inverse(q, p)
        return p, q, d, u

def init_connection():
    ip = input("ip > ")
    port = int(input("port > "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except:
        print("[-] Connection error")
        exit(-1)
    
    print("[+] Connection established")
    return sock

def login(sock):
    client_id = input("id > ")
    if client_id in CREDENTIALS:
        client_pw = CREDENTIALS[client_id]
    else:
        client_pw = input("pw > ")
    
    sock.sendall((client_id + '\n').encode())
    resp = packet_recv_plain(sock).decode()
    print("(From server)", resp)
    # Already registered
    if resp == f"Hi {client_id}! Glad to see you again":
        pw_hash = sha256(client_pw.encode()).digest()
        p = int(aes_dec(bytes.fromhex(packet_recv_plain(sock).decode()), pw_hash))
        q = int(aes_dec(bytes.fromhex(packet_recv_plain(sock).decode()), pw_hash))
        d = int(aes_dec(bytes.fromhex(packet_recv_plain(sock).decode()), pw_hash))
        u = int(aes_dec(bytes.fromhex(packet_recv_plain(sock).decode()), pw_hash))
    
    # Not registered
    elif resp == f"Hi {client_id}! To create an account, please send your RSA private key encrypted with your pw":
        pw_hash = sha256(client_pw.encode()).digest()
        p, q, d, u = generate_rsa_private_key()
        enc_p = aes_enc(str(p).encode(), pw_hash).hex().encode()
        enc_q = aes_enc(str(q).encode(), pw_hash).hex().encode()
        enc_d = aes_enc(str(d).encode(), pw_hash).hex().encode()
        enc_u = aes_enc(str(u).encode(), pw_hash).hex().encode()
        packet_send_plain(sock, enc_p)
        packet_send_plain(sock, enc_q)
        packet_send_plain(sock, enc_d)
        packet_send_plain(sock, enc_u)
        packet_send_plain(sock, str(n).encode())
        resp = packet_recv_plain(sock).decode()
        print("(From server)", resp)

    # Error has been occured
    else:
        exit(-1)

    return p,q,d,u

def recv_session_key(sock, p, q, d, u):
    rsa_enc_session_key = int(packet_recv_plain(sock).decode(), 16)
    rsa_plain = long_to_bytes(rsa_crt_dec(p, q, d, u, rsa_enc_session_key))
    session_key = rsa_plain[1:33]
    print("[+] Session key received")
    return session_key

def save_file(sock, session_key, file_enc_key):
    packet_send_aes_enc(sock, "save_file".encode(), session_key)
    name = input("filename(Only lowercase) > ")
    if not name.islower():
        print("[-] Invalid filename")
        packet_send_aes_enc(sock, "BACK".encode(), session_key)
        return False

    packet_send_aes_enc(sock, name.encode(), session_key)
    resp = packet_recv_aes_enc(sock, session_key).decode()
    if resp != "OK":
        print("(From server)", resp)
        return False
    
    data = bytes.fromhex(input("data(in hex) > "))
    if len(data) > 1000:
        print("[-] File too large")
        packet_send_aes_enc(sock, "BACK".encode(), session_key)
        return False

    data_enc = aes_enc(data, file_enc_key)
    packet_send_aes_enc(sock, data_enc.hex().encode(), session_key)
    resp = packet_recv_aes_enc(sock, session_key).decode()
    if resp != "OK":
        print("(From server)", resp)
        return False

    print(f"[+] File {name} successfully saved")
    return True

def load_file(sock, session_key, file_enc_key):
    packet_send_aes_enc(sock, "load_file".encode(), session_key)
    name = input("filename(Only lowercase) > ")
    if not name.islower():
        print("[-] Invalid filename")
        packet_send_aes_enc(sock, "BACK".encode(), session_key)
        return False

    packet_send_aes_enc(sock, name.encode(), session_key)
    resp = packet_recv_aes_enc(sock, session_key).decode()
    if resp != "OK":
        print("(From server)", resp)
        return False
    
    data_enc_hex = packet_recv_aes_enc(sock, session_key).decode()
    data_enc = bytes.fromhex(data_enc_hex)

    '''    
    Sorry, I won't let you know a plain file content. But I will give you a encrypted
    one. You can easily decrypt this without my help because file_enc_key is derived
    from your own rsa private key. isn't it????
    '''

    # data = aes_dec(data_enc, file_enc_key)
    # print(f"[+] {name}(in hex) : {data.hex()}")
  
    print(f"[+] {name}.enc(in hex) : {data_enc.hex()}")
    return True

def menu(sock, session_key, file_enc_key):
    menu = '''1. Save a file
2. Load a file
3. Logout'''

    while True:
        print(menu)
        c = input("> ")
        if c == '1':
            save_file(sock, session_key, file_enc_key)
        elif c == '2':
            load_file(sock, session_key, file_enc_key)
        elif c == '3':
            packet_send_aes_enc(sock, "logout".encode(), session_key)
            print("[+] Bye...")
            break
        else:
            continue

def go():
    ### INIT
    sock = init_connection()
    p,q,d,u = login(sock)    
    session_key = recv_session_key(sock, p, q, d, u)
    file_enc_key = file_encryption_key(p, q, d, u)
    ### MAIN ROUTINE
    menu(sock, session_key, file_enc_key)
    sock.close()

go()
