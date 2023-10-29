import random
import des
import string

random.seed(1)


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

def get_linear_bias(idx, x_mask, y_mask):
  cnt = -32
  for x in range(64):
    if (hw(x & x_mask) + hw(sbox(x, idx) & y_mask)) % 2 == 0:
      cnt += 1
  return abs(cnt)



def sbox(x, idx):
  row = ((x >> 4) & 2) | (x & 1)
  col = (x >> 1) & 0xf
  return S_BOX[idx][row][col]

def get_linear_info():
  fixed_bits = [IP[i] for i in range(0,64,8)]+[IP[i] for i in range(1,64,8)]+[IP[i] for i in range(2,64,8)]+[IP[i] for i in range(2,64,8)]
  fixed_bits_left = []
  fixed_bits_right = []
  for x in fixed_bits:
    if x < 32:
      fixed_bits_left.append(x)
    else:
      fixed_bits_right.append(x - 32)
  
  bias_table = [[[0]*16 for _ in range(64)] for _ in range(8)]

  for sbox_idx in range(8):
    for x_mask in range(64):
      for y_mask in range(16):
        bias_table[sbox_idx][x_mask][y_mask] = get_linear_bias(sbox_idx, x_mask, y_mask)
  
  info = [-1]

  for sbox_idx in range(6,7): # 8
    for first_input_mask in range(39,40): # 64
      first_input_mask_bits = bin(first_input_mask)[2:].zfill(6)
      sbox_input_bit_idx = E[6*sbox_idx : 6*sbox_idx + 6]
      chk = True
      for i in range(6):
        if first_input_mask_bits[i] == '1' and sbox_input_bit_idx[i] not in fixed_bits_right:
          chk = False
      if not chk:
        continue
      
      # For convinience, only 1 bit is active
      for first_output_active_bit_idx in [3]: # [0,1,2,3]
        first_output_mask = 1 << (3 - first_output_active_bit_idx)
        bias1 = bias_table[sbox_idx][first_input_mask][first_output_mask]

        idx_after_perm = P[4 * sbox_idx + first_output_active_bit_idx]
        if idx_after_perm % 4 not in [1,2]: # s-box 2개에 걸치면 골치아프니 그냥 고려하지 않음
          continue
        if idx_after_perm not in fixed_bits_left:
          continue

        second_sbox_idx = idx_after_perm // 4
        second_input_mask = 16 >> (idx_after_perm % 4) # 1 -> 0b1000, 2 -> 0b100

        for second_output_mask in range(16):
          bias2 = bias_table[second_sbox_idx][second_input_mask][second_output_mask]
          if bias1*bias2 > info[0]:
            info = [bias1*bias2, sbox_idx, first_input_mask, first_output_mask, second_sbox_idx, second_input_mask, second_output_mask] 

  print(info)

get_linear_info()
exit()

# [bias1*bias2, sbox_idx, first_input_mask, first_output_mask, second_sbox_idx, second_output_mask] 
# [144, 6, 39, 1, 4, 8, 11]

# sbox_idx = 6
# first_input_mask = 39,
# first_output_mask = 1,
# second_sbox_idx = 4,
# second_input_mask = 8
# second_output_mask = 11

round_keys_perm_idx = []

def key_bit_perm_check():
  k = list(range(64))
  k = [k[x] for x in CP_1]
  g, d = k[:28], k[28:]
  for i in range(5):
    g = g[SHIFT[i]:] + g[:SHIFT[i]]
    d = d[SHIFT[i]:] + d[:SHIFT[i]]
    tmp = g + d
    round_keys_perm_idx.append([tmp[x] for x in CP_2])

#key_bit_perm_check()

#### Right에서 (S4, 001000)에 대응되는 17번째 비트
#### Left에서 (S4, 1011)에 대응되는 16, 18, 19번째 비트, P를 거친 후에는 각각 18, 4, 14번째 비트
#### 이들이 FP를 거친 후의 결과를 XOR하면 됨

def linear_test_round4():
  # 0.006591796875
  key = b'12345678'
  cipher = des.DES(key, 1)

  z = [0,0]

  for a in range(10000000):
    pt = ''.join(random.choices(string.ascii_lowercase, k=8)).encode()
    ct = cipher.encrypt(pt)
    ct_bits = des.bytes_to_bits(ct)

    ct_fp_before_idx = [27]
    #ct_fp_before_idx = [P[16], P[18], P[19], 17+32]
    #ct_fp_before_idx = [18, 4, 14, 17+32]
    ct_idx = [FP[x] for x in ct_fp_before_idx]

    z[sum(ct_bits[x] for x in ct_idx) % 2] += 1
    #z[random.randint(0,1)]+=1
    if a % 10000 == 1:
      print(z, (z[0]-z[1])/a)

    

linear_test_round4()



'''
E = [    31, 0,  1,  2,  3,  4,
    3,  4,  5,  6,  7,  8,
    7,  8,  9,  10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0,]
'''