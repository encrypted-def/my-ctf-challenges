import random

def get_invertible_matrix(n):
    while True:
        mat = matrix(GF(2), n, n)
        for i in range(n):
            for j in range(n):
                mat[i,j] = random.randint(0,1)
        if mat.is_invertible():
            return mat

def get_random_vector(n):
    vec = vector(GF(2), n)
    for i in range(n):
        vec[i] = random.randint(0,1)
    return vec

N = 256
ROUNDS = 128
random.seed("BTS Bongjunho Sonheungmin Cogechan Let's go!!")
matrices = [get_invertible_matrix(N) for _ in range(ROUNDS)]
vectors = [get_random_vector(N) for _ in range(ROUNDS)]

f = open("constants.txt", "w")

for r in range(ROUNDS):
    for i in range(N):
        for j in range(N):
            f.write(str(matrices[r][i][j]))
        f.write("\n")

    for i in range(N):
        f.write(str(vectors[r][i]))
    f.write("\n")

f.close()