import time, copy, random
from pwn import *

candidates = [[[True]*9 for _ in range(9)] for __ in range(9)]

# possible move list for the current board
def movelist():
    L = []
    for i in range(9):
        for j in range(9):
            for num in range(1,10):
                if candidates[i][j][num-1]:
                    L.append((i,j,num))
    return L

def update_move(x, y, num):
    if x== -1:
        return None
    for i in range(9):
        candidates[x][y][i] = False
        candidates[x][i][num-1] = False
        candidates[i][y][num-1] = False
        
    r = x//3
    c = y//3
    for i in range(3*r, 3*r+3):
        for j in range(3*c, 3*c+3):
            candidates[i][j][num-1] = False

def is_move_collision(move1, move2):
    x,y,num = move1
    nx,ny,nnum = move2
    if nx == x and ny == y:
        return True
    if nnum == num and (nx==x or ny==y or (nx//3==x//3 and ny//3==y//3)):
        return True
    return False

# return score, (x, y, num)
# score = 1 : AI win, 0 : neutral, -1 : Player win
# return a best move for each user(AI or player) in current depth
def backtrack(moves, possible_moves, depth, maxdepth, time_st):
    #print("backtrack", depth, moves)
    AIturn = (depth % 2 == 0)
    if depth == maxdepth or time.time() - time_st > 2.5 :
        for nextmove in possible_moves:
            if any(is_move_collision(pastmove, nextmove) for pastmove in moves):
                continue
            return 0, nextmove
        if AIturn: # AI has nothing to move
            return -1, (-1,-1,-1)
        else: # Player has nothing to move
            return 1, (-1,-1,-1)

    candidate, curscore = (-1,-1,-1), -1
    if not AIturn:
        curscore = 1
    for nextmove in possible_moves:
        if any(is_move_collision(pastmove, nextmove) for pastmove in moves):
            continue
        moves.append(nextmove)
        score, _ = backtrack(moves, possible_moves, depth+1, maxdepth, time_st)
        if AIturn:
            if score == 1: # immediate win
                moves.pop()
                return 1, nextmove
            else:
                if curscore < score:
                    curscore = score
                    candidate = nextmove
        
        else:
            if score == -1: # immediate win
                moves.pop()
                return -1, nextmove

            else:
                if curscore > score:
                    curscore = score
                    candidate = nextmove    
    
        moves.pop()
    return curscore, candidate


def mymove(x=-1, y=-1, num=-1):
    update_move(x, y, num)
    # If 3 or more cands are left for some grid, any choice is okay
    needmoretime = False
    mx = -1
    for i in range(9):
        for j in range(9):
            mx = max(mx, candidates[i][j].count(True))

    if mx >= 4:
        needmoretime = True    
    myL1 = movelist()
    if not myL1:
        return (-1, -1, -1)

    if needmoretime:
        elem = random.choice(myL1)
        update_move(elem[0], elem[1], elem[2])
        return elem

    random.shuffle(myL1)

    
    if len(myL1) <= 10:
        score, recommend_move = backtrack([], myL1, 0, 20, time.time())
    elif len(myL1) <= 15:
        score, recommend_move = backtrack([], myL1, 0, 5, time.time())
    elif len(myL1) <= 25:
        score, recommend_move = backtrack([], myL1, 0, 4, time.time())
    elif len(myL1) <= 80:        
        score, recommend_move = backtrack([], myL1, 0, 3, time.time())
    else:
        score, recommend_move = backtrack([], myL1, 0, 2, time.time())
    
    if recommend_move[0] == -1:
        recommend_move = myL1[0]
        #print("wrong..")
        #exit()
    update_move(recommend_move[0], recommend_move[1], recommend_move[2])
    return recommend_move

win = 0
lose = 0

def newconn():
    global win, lose
    pt = 0
    r = remote('localhost', 9001)
    x, y, num = -1, -1, -1
    while True:
        print(f"NOW PT is {pt}, W {win} L {lose}")
        r.recvuntil(b'> ')
        r.sendline(b'2') # FLAG MODE
        r.recvuntil(b'> ')
        r.sendline(b'F')        
                
        # initialize board & candidates
        board = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    candidates[i][j] [k]=True

        while True:
            z = r.recvuntil(b'> ')
            x, y, num = mymove(x, y, num)
            r.sendline(f'{x} {y} {num}'.encode())
            status = r.recvuntil(b'You').decode()
            if status[:9] == "AI move >":
                x, y, num = map(int, status[9:].split('\n')[0].split())

            if "[-]" in status:
                lose += 1
                pt -= 1
                break
            if "[+]" in status:
                win += 1
                pt += 1
                break

        
        if pt == 10:
            r.interactive()

        if pt < 0:
            break

    try:
        r.close()
    except: pass

num = 0
while True:
    num += 1
    print(f"====== {num}-th connection, W {win} L {lose} ======")
    newconn()

# AI vs random = 308 692 (69.2%)