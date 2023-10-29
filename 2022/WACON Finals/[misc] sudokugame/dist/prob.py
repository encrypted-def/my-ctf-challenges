#!/usr/bin/python3
import time, random

RULE = '''a) Board is 9x9(0-indexed), fill any empty grid with 1-9 digits like ordinary sudoku
b) If duplication of digits in each column / each row / each nine 3x3 subgrids is occured by their moves, then lose
c) You move first. So if all 81 grids are filled, AI cannot make a move and you win
d) If you want to put a digit 2 on the grid (4, 8), then type '4 8 2' without quotes
e) If you provide a wrong query, you immediately lose
f) The point is initialized to 0. If you win(resp. lose) at FLAG mode, you earn +1(resp. -1) point.
g) If the point reaches +10 then you will earn a FLAG.
h) In FLAG mode, your each moves must be given in 3 seconds
i) In Practice mode, AI is the same but there is no time limit for your practice. Of course, practice mode is not affect on the point
'''

MENU = '''1. Rule
2. FLAG mode
3. Practice mode
> '''

def is_duplicate(board):
    for i in range(9):
        col = [board[j][i] for j in range(9)]
        for num in range(1,10):
            if board[i].count(num) > 1:
                return True
            if col.count(num) > 1:
                return True
    
    for i in range(3):
        for j in range(3):
            subgrid = [board[x][y] for x in range(3*i, 3*i+3) for y in range(3*j, 3*j+3)]
            for num in range(1,10):
                if subgrid.count(num) > 1:
                    return True            

    return False


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
    if depth == maxdepth or time.time() - time_st > 0.9:
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


def AImove(x=-1, y=-1, num=-1):
    update_move(x, y, num)
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


def print_board(board):
    for row in board:
        s = ''.join(str(x) for x in row)
        print(s.replace('0','.'))


def play(TL):
    showboard = True
    
    while True:
        tf = input("Do you want to see a board for each moves?(T/F) > ")
        if tf == 'T':
            break
        elif tf == 'F':
            showboard = False
            break
        else:
            print("Invalid choice")
    
    board = [[0]*9 for _ in range(9)]


    x,y,num=-1,-1,-1
    while True:
        if showboard:
            print_board(board)

        time_st = time.time()
        
        
        try:
            x, y, num = list(map(int, input("Your turn > ").split()))
        except:
            print("[-] Invalid format. You lose")
            return False        
        
        if time.time() - time_st > TL:
            print("[-] time over. You lose")
            return False        
        if x < 0 or x >= 9 or y < 0 or y >= 9 or board[x][y] != 0:
            print("[-] wrong coordinates. You lose")
            return False
        if not 1 <= num <= 9:
            print("[-] wrong number. You lose")
            return False
        board[x][y] = num
        if is_duplicate(board):
            print("[-] duplicate. You lose")
            return False

        try:
            x, y, num = AImove(x, y, num)
            print(f"AI move > {x} {y} {num}")
        except:
            print("[+] Invalid format. You win")
            return True        
        if x < 0 or x >= 9 or y < 0 or y >= 9 or board[x][y] != 0:
            print("[+] wrong coordinates. You win")
            return True
        if not 1 <= num <= 9:
            print("[+] wrong number. You win")
            return True
        board[x][y] = num
        if is_duplicate(board):
            print("[+] duplicate. You win")
            return True
        
def gogo():
    pt = 0
    while pt < 10:
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    candidates[i][j][k]=True
        print(f"Hello player, your point = {pt}")
        idx = input(MENU)
        if idx == '1':
            print(RULE)
        elif idx == '2':
            if play(3):
                pt += 1
            else:
                pt -= 1
        elif idx == '3':
            play(100000000000000000000)
        else:
            print("Invalid choice")

    print("Good job! Flag is", open("flag.txt").read())
                    
gogo()