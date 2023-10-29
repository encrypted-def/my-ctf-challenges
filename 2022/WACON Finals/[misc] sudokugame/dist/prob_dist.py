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


def AImove(x=-1, y=-1, num=-1):
    # I waste about 2 hours to write a AI code but will not be released XD
    return (-1, -1, -1)


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