import random
import des
import string
import os
from tqdm import tqdm
import itertools

random.seed("The Game of DES2")

IP = random.sample(range(64), 64) # Initial permut matrix
CP_1 = random.sample(range(64), 56) # Initial permut made on the key
CP_2 = random.sample(range(56), 48) # Permut applied on shifted key to get round key
P = random.sample(range(32), 32) # Permut made after each SBox substitution for each round
FP = random.sample(range(64), 64) # Final permut for datas after the 16 rounds

#Expand matrix to get a 48bits matrix of datas to apply the xor with round key
E = [    31, 0,  1,  2,  3,  4,
    3,  4,  5,  6,  7,  8,
    7,  8,  9,  10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0,]

#SBOX
S_BOX = [         
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
], 

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]

SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def hw(x):
  return bin(x).count('1')

def sbox(x, idx):
  row = ((x >> 4) & 2) | (x & 1)
  col = (x >> 1) & 0xf
  return S_BOX[idx][row][col]

round_keys_perm_idx = []


#### Right에서 (S4, 001000)에 대응되는 17번째 비트
#### Left에서 (S4, 1011)에 대응되는 16, 18, 19번째 비트, P를 거친 후에는 각각 18, 4, 14번째 비트
#### 이들이 FP를 거친 후의 결과를 XOR하면 됨

# Revert S3 to determine R4[17], returns R4[17] only
def revert_1R(guessed_key, ct_bits):
  DEBUG = False
  exp_input_idxs = [23,52,31,3,20,1]
  if DEBUG:
    for i in range(6):
      assert FP.index(32 + E[3*6+i]) == exp_input_idxs[i]
      
  S3_in = des.xor(guessed_key, [ct_bits[i] for i in exp_input_idxs])
  x = 0
  for v in S3_in:
    x = 2*x + v
  
  y = sbox(x, 3)
  return y & 1

def lc_round5():
  # 0.006591796875
  key = os.urandom(8)
  key_bits = des.bytes_to_bits(key)
  cipher = des.DES(key, 5)

  key_ans = [key_bits[round_keys_perm_idx[4][i]] for i in range(18,24)]
  print("key ans ", key_ans)

  cts = []
  for i in tqdm(range(100000)):
    pt = ''.join(random.choices('0123456789-', k=8)).encode()
    ct = cipher.encrypt(pt)
    cts.append(ct)

  
  for guessed_key in itertools.product([0,1], repeat=6):
    z = [0,0]
    for i in range(100000):
      ct = cts[i]
      ct_bits = des.bytes_to_bits(ct)
      ct_fp_before_idx = [2 + 32, 26 + 32, 5 + 32, 17]
      ct_idx = [FP.index(x) for x in ct_fp_before_idx]
      tot = sum(ct_bits[x] for x in ct_idx) + revert_1R(guessed_key, ct_bits)
      z[tot%2] += 1
    
    print(guessed_key, abs(z[0]-z[1]))

# DEBUG PURPOSE
RIGHT_KEY = bytes.fromhex('4aa0c4233e0069f4')
RIGHT_KEY_BITS = des.bytes_to_bits(RIGHT_KEY)

keybits_cnt = [[0]*2 for _ in range(64)]

ct_fp_before_idx = [2 + 32, 26 + 32, 5 + 32, 17]
ct_idx = [FP.index(x) for x in ct_fp_before_idx]

for i in range(64):
  get_key_idx = [(x+i)%64 for x in [50,5,21,45,61,56]] # key bits corresponding to Sbox3

  file_ct = open(f"data_hard/ct{i}", "rb")
  cts = []
  for _ in range(65536):
    ct = file_ct.read(8)
    ct_bits = des.bytes_to_bits(ct)
    cts.append(ct_bits)
  file_ct.close()

  mx = 0
  right_key = []
  for guessed_key in itertools.product([0,1], repeat=6):
    bias = 0
    for j in range(65536):
      tot = sum(cts[j][x] for x in ct_idx) + revert_1R(guessed_key, cts[j])
      if tot % 2 == 0:
        bias -= 1
      else:
        bias += 1
    if abs(bias) > mx:
      right_key = list(guessed_key)
      mx = abs(bias)
  
  print("!!!!!",i)
  for j in range(6):
    print(RIGHT_KEY_BITS[get_key_idx[j]], right_key[j])
    keybits_cnt[get_key_idx[j]][right_key[j]] += 1


recovered_key_bits = []
for i in range(64):
  if keybits_cnt[i][0] > keybits_cnt[i][1]:
    recovered_key_bits.append(0)
  else:
    recovered_key_bits.append(1)

recovered_key = des.bits_to_bytes(recovered_key_bits)
print("WACON2023{" + recovered_key.hex() + "}")


# flag = WACON2023{bb2ef4b3979b2f51} (easy)
# flag = WACON2023{4aa0c4233e0069f4} (hard)