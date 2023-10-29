#!/usr/bin/python3
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
from pwn import *

context.log_level = 'ERROR'

def aes_enc(pt, key):
    pt_pad = pad(pt, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pt_pad)

def aes_dec(ct, key):
    cipher = AES.new(key, AES.MODE_ECB)
    pt_pad = cipher.decrypt(ct)
    return unpad(pt_pad, 16)

# Derive file encryption key from RSA prvate key
def file_encryption_key(p, q, d, u):
    rsa_priv_key = long_to_bytes(p) + long_to_bytes(q) + long_to_bytes(d) + long_to_bytes(u)
    return sha256(rsa_priv_key).digest()

MY_IP = 'host.docker.internal' # If you run this on your own server, then replace this to your server ip
MY_PORT = 8787

CLIENT_IP = '3.39.27.228'
CLIENT_PORT = 9001

SERVER_IP = '3.39.27.228'
SERVER_PORT = 9002

# Check whether client can connect to here
def connection_test():
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('0.0.0.0', MY_PORT))
        server_sock.listen()

        r_client = remote(CLIENT_IP, CLIENT_PORT)
        r_client.recvuntil(b"ip > ")
        r_client.sendline(MY_IP.encode())
        r_client.recvuntil(b"port > ")
        r_client.sendline(str(MY_PORT).encode())

        client_sock, _ = server_sock.accept()
        client_sock.close()
        r_client.close()
        server_sock.close()

    except:
        print(f"[-] Client cannot connect to {MY_IP}:{MY_PORT}. Firewall issue?")
        exit(-1)
    
    print("[+] Connection test passed")

# recover min(p, q)
def recover_priv_key():
    print("[+] Begin recover_priv_key")
    enc_p = '5901d4d62364a649837b4638748fd17beb3942388cce66f7595ea589820b7ca86fa1c33d92435f6820c06e09752b4bcf1f0a3936d173d482fb414cabe446ed00fbcc7de15b79670e8cf0ee478be647b6bf637e4a69eac25b2d8567fd400b01b3bbf9ec3a6cee1718d43cb8c5d16b0ebd35e3cffc2bc58662338e56f3a7a9478d958d8abac38a84d801e11cd209510782b5e9f5bcc277b5e7518c38571c923771c2a22c1dc11abf5a82d32c1c4e3ae84300a11fd09a978304cf65c6e31c8286685020c63c1ed465a1f0e2423bafff2cf1b951266cacfd99580693c0cdd80d8224a41e56bfc9ae430fc219a6a4d8570d487de2dc67ec5610734181e72bc5cf8691f04ffb9997d259d757e4779966d1fd0c911c50928345a5c8fedfd81f56c07340051d97c41c6529a5593b854af0f10f832c158b049a53325d13e68b6d34b297be'
    enc_q = '312f77b75d0dcf6dd54c4f12f6a220b12a617c73a7b6ba061ddb5733927ed603502cfbfa3607880d558a3cbde74b04a94c24b9940bf80b7f9464336108c71729aa5e412d4a434f8c9903d063c834efc25bfc65d3879dacb4ae42c53586124fe5f6771f674e984f3a999eda035e9176c5a20f2c8860ee470090680f668564eed7d724d31182238aed00a377c11144c537296b995f65ffd4256910f0e711f059fdbe69524913a10d6be930cf2c19c1afe53bd5adcf0aa09dac2d1103af61afa413986a90c1e1e2f739e8dcc6a2ed886259569dee4ad5babfd1b8f67ede5b75d2bca287d49cbaab7c77bc1afedfd8f230a9d63d23f37eadbbd8a984cb59e43945149b11ff06f578a36d7bb18a667dc976f3f4e1e8ba20d38501031bfaeb84a40f45187f1c28a5ba0382251962f67101892a3c15a864a79a4b446367cd2418ada4ec'
    enc_d = 'd48e1cc30261b74d88f70825635765f57905a6fe14ac012a15bd3da5e977773883acaa2e29e9a1abb2d53f3d577fe4a575050e4928f17ea6ab8f6430a33b17139e3854d2fc9837a8a39775bff06fcf4d006dea99d91bd05e41443151e3a26dd287f66977fbde51e290802c7e17fb5dd927cf2bd38f49309d9d7549758851ed238661531d83dd0c05f5fedb7dece60d268cfa64db86d76410d6e98ae4c702ee10c5ff364e635024de9471c40b5c4b396e20b664a181fad45cdcf07c44537a6f17a026574c79b68fadb5caecfc6f35b23963bf05aadcdc2df54bba46cfec810a6581fba5f8c8474c4d7c2559ff1a959cefc09bf0acffebc586fb929fcd4625c75d8c3f8801b4f555adf9d756ea487315f7607e2178d6879d65bd194853be63fe17c6307923ab5cf70989095eccb1c0c1be98f02f0f33d45d1618041dc51fae01a55e6adedfc77100a883666eb3c5063545d5f870e2b41a075dcdde08e1b143d660d1d100647e4e8bb2906fdf188bab040412b0745ad732e62c9aa60e09bb4a73c21b6e2b8a77c805c759ce77cb235d3b841c06a155acd0c0ccc5318fa752c249dd767d44195c021153fd4372049889e970cfaa57117a5174f60395e6c54b35323cac58d6a8858b4610c07c937c721fd70d57f9a0f3d43931234881ea047afffa740bae7af956badea71c5b0f06cac29536993cf2fa99b9fd03a9b3ff5546e08ed6e13c9df9df407564b49375952e377ec1a71dbc6d55d13d02af793f2a445cbf21f4468dd013a0e4fda9b53b0c54bd22efb5a9b49c58b2873dd2f636b348622e70864c572d3adb5e5b9a5746e76e2ddd9a2dcba5d08a7b0b771cf3c1f134ea18aecca80238498960dbc1a806a162db5b99'
    enc_u = '7a00dbda0a01db597eee1759f4565870da4757c42e0b4cef0a3cabe759e6ef24dcab8a3313c5e2c95ec7f38010b763b831f4d9b7f9539b8c7447f0f81f11caf00f75813d87cd803137d088b0f1ee8179f532a58cdb427cd0ad903babaf3312b954d9694d306e62f5ae6af08348ed9560c1bbecd84799fb942e4b0486f6af7a6649e9d50a1f7ef460ea5f5d087f3565ff09336336496729f786b6a654d99ad4a7f925dc268cd5c1b35c3c6cf57089e2afb53532832c7b66a17b2287e67c53518ba90a99d1a8495369cf3530109709d5419a5046b733dcb4e6006f8cbc964d17ab6121f94b6a1a46b28e17077f24adf417c21a5f2d50f741773befe15d3c9c37906c92798618879c0c9c5fe346e0a67f73fc6640c1c32c2d3ac1512fc781c95e259fcd79496523a07e73d5171f37251a3fbb80a12ee7a18cdce8d6381a7cf59d18'
    n = 12659214462730739290777710676401716129364537461971321037157877540193780746910540896819650182970880505880808257029478576966922788012182813161567264480789412487933555048594859387373262444873139956649127172509365160527593844518913325580532608517683946927197373934501869789520791006507064633048240282420120292353010385218838558491852148859208850993839899492722657498287727598894181537635087547896216039380309309759245366183056244723928135316860412330991393425352005295678522825817645977696006156843729550866483053456177362041805254686689400982564781219502910693511366956648759975359689060253588108513703355540146694238377

    st = 1
    en = 1<<1024
    e = 65537

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('0.0.0.0', MY_PORT))
    server_sock.listen()

    while st < en:
        gap = en - st
        if gap.bit_length() % 50 == 0:
            print(f"{int( (1024 - gap.bit_length()) /1024 * 100)}%..")
        r_client = remote(CLIENT_IP, CLIENT_PORT)
        r_client.recvuntil(b"ip > ")
        r_client.sendline(MY_IP.encode())
        r_client.recvuntil(b"port > ")
        r_client.sendline(str(MY_PORT).encode())

        client_sock, _ = server_sock.accept()
        r_client.recvuntil(b"id > ")
        r_client.sendline(b'codegate')
        
        client_id = client_sock.recv(1024)
        assert client_id == b'codegate\n'

        client_sock.sendall(f"Hi codegate! Glad to see you again\n".encode())

        client_sock.sendall(enc_p.encode() + b'\n')
        client_sock.sendall(enc_q.encode() + b'\n')
        client_sock.sendall(enc_d.encode() + b'\n')
        client_sock.sendall(enc_q.encode() + b'\n') # corrupted u
        
        mid = (st+en)//2
        session_key = long_to_bytes(mid)[1:33]
        enc_session_key = long_to_bytes(pow(mid, e, n))

        client_sock.sendall(enc_session_key.hex().encode() + b'\n')
        
        r_client.sendline(b'3') # choose logout

        try:
            expected_enc_hex = aes_enc(b"logout", session_key).hex()
            dat_enc_hex = client_sock.recv(1024).decode()[:-1]
            #print(expected_enc_hex)
            #print(dat_enc_hex)
            if expected_enc_hex == dat_enc_hex:
                st = mid + 1
            else:
                en = mid
        except:
            pass

        r_client.close()
        client_sock.close()

    server_sock.close()
    p = st
    assert(n % p == 0)

    print("[+] RSA private key successfully recovered")
    # p = 90963561636973648079748872710233174372627229619862552156868868624382464054942417475700780603355113343585008425358474307873808408406479575611336981505769196262469538075309296635799368598090065862245712809107399779324506152673381675069862205414043721577448302842238856356790422786981850473394241451010170968199
    #print(f"{p = }")
    q = n // p
    phi = (p-1)*(q-1)
    d = inverse(e, phi)
    return p, q, d

def recover_flag(p, q, d):
    ct = bytes.fromhex('05317E8E878CF267B924C9AEBCA52BFA9169813439997054DB6A5522E488A0B34594104098AE60ED147A465D12D797AF')
    # There are two possibilities of u
    u = inverse(q, p)
    file_enc_key1 = file_encryption_key(p, q, d, u)
    try:
        print(aes_dec(ct, file_enc_key1))
    except:
        pass
    
    p, q = q, p
    u = inverse(q, p)
    file_enc_key1 = file_encryption_key(p, q, d, u)
    try:
        print(aes_dec(ct, file_enc_key1))
    except:
        pass

connection_test()
p, q, d = recover_priv_key()
recover_flag(p, q, d)
