# https://github.com/RobinDavid/pydes with medium(?) modifications

import random

random.seed("The Game of DES2")

IP = random.sample(range(64), 64) # Initial permut matrix
CP_1 = random.sample(range(64), 56) # Initial permut made on the key
CP_2 = random.sample(range(56), 48) # Permut applied on shifted key to get round key
P = random.sample(range(32), 32) # Permut made after each SBox substitution for each round
FP = random.sample(range(64), 64) # Final permut for datas after the 16 rounds

##########################################################
##########################################################
########## E, S_BOX, SHIFT ARE NOT CHANGED!!!!! ##########
##########################################################
##########################################################

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

#Matrix that determine the shift for each round of keys
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def bytes_to_bits(bytes_arr):
    ret = []
    for b in bytes_arr:
        for i in range(7,-1,-1):
            ret.append((b >> i) & 1)
    return ret

def bits_to_bytes(bits_arr): #Recreate the string from the bit array
    assert len(bits_arr) % 8 == 0, "invalid bits_arr length"
    size = len(bits_arr) // 8
    ret = []
    for i in range(size):
        tmp = 0
        for j in range(8):
            tmp = 2 * tmp + bits_arr[8*i + j]
        ret.append(tmp)
    return bytes(ret)

def xor(t1, t2):#Apply a xor and return the resulting list
    return [x^y for x,y in zip(t1,t2)]

class DES():
    def __init__(self, key, round_num):
        self.round_keys = []
        self.round_num = round_num
        self._keyschedule(key)

    def _keyschedule(self, key):
        key = bytes_to_bits(key)
        key = [key[x] for x in CP_1]
        g, d = key[:28], key[28:]
        for i in range(self.round_num):
            g = g[SHIFT[i]:] + g[:SHIFT[i]]
            d = d[SHIFT[i]:] + d[:SHIFT[i]]            
            tmp = g + d
            self.round_keys.append([tmp[x] for x in CP_2])

    def _substitute(self, R_expand):#Substitute bytes using SBOX
        subblocks = [R_expand[k:k+6] for k in range(0, 48, 6)]
        ret = []
        for i in range(8): #For all the sublists
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]), 2)#Get the row with the first and last bit
            column = int(''.join([str(x) for x in block[1:][:-1]]),2) #Column is the 2,3,4,5th bits
            val = S_BOX[i][row][column] #Take the value in the SBOX appropriated for the round (i)
            for j in range(3,-1,-1):
                ret.append((val >> j) & 1)            
        return ret
    
    def encrypt(self, pt):        
            pt = bytes_to_bits(pt)
            pt = [pt[x] for x in IP]                
            L, R = pt[:32], pt[32:]
            tmp = None
            for i in range(self.round_num):
                R_expand = [R[x] for x in E]
                tmp = xor(self.round_keys[i], R_expand)
                tmp = self._substitute(tmp)
                tmp = [tmp[x] for x in P]
                L, R = R, xor(L, tmp)

            tmp = R + L
            C = [tmp[x] for x in FP]
            return bits_to_bytes(C)
