N = 256
ROUNDS = 128

matrices = [matrix(GF(2), N, N) for _ in range(ROUNDS)]
vectors = [vector(GF(2), N) for _ in range(ROUNDS)]

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

load_constants()

def encrypt(plain, key):
    cipher = plain[:]
    for r in range(ROUNDS):
        # S-BOX layer
        cipher[0] += cipher[1] * cipher[2]
        # Key addition
        cipher += key
        # Linear layer
        cipher = matrices[r] * cipher + vectors[r]
    return cipher