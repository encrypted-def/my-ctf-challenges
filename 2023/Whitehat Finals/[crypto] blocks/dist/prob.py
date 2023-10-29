from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
import os

ECB_MODE = 0
CBC_MODE = 1
CTR_MODE = 2
CFB_MODE = 3
OFB_MODE = 4

# choose random number from 0 to n-1
def secure_random_choice(n):
    while True:
        x = os.urandom(1)[0]
        if x // n == 0xff // n:
            continue
        return x % n

def challenge():
    mode = secure_random_choice(5)
    key = os.urandom(16)
    
    for _ in range(2):
        iv = bytes.fromhex(input("iv? > "))
        assert len(iv) == 16, f"Invalid iv size({len(iv)})"

        enc_option = input("encrypt? ('y' if encrypt/'n' if decrypt) > ") == 'y'    

        if mode == ECB_MODE:
            cipher = AES.new(key, AES.MODE_ECB)
        elif mode == CBC_MODE:
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        elif mode == CTR_MODE:
            ctr = Counter.new(128, initial_value=bytes_to_long(iv))
            cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        elif mode == CFB_MODE:
            cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
        else:
            cipher = AES.new(key, AES.MODE_OFB, iv=iv)


        if enc_option: # encrypt
            pt = bytes.fromhex(input("plaintext? > "))  
            assert len(pt) % 16 == 0, f"Invalid pt size({len(pt)})"
            ct = cipher.encrypt(pt)
            print(f"ct = {ct.hex()}")
        
        else: # decrypt
            ct = bytes.fromhex(input("ciphertext? > "))
            assert len(ct) % 16 == 0, f"Invalid ct size({len(ct)})"
            pt = cipher.decrypt(ct)
            print(f"pt = {pt.hex()}")        


    guess = int(input("mode? > "))
    if mode == guess:
        print("Good!")
        return True
    else:
        print("nono..", mode, guess)
        return False


for i in range(100):
    print(f"Stage {i+1}/100")
    if not challenge():
        exit(-1)

print("Good job!", open("flag").read())