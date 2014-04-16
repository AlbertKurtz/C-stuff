from random import randint
import subprocess
import sys

N=10
TURNS=10

board = []

for x in range(N):
    board.append(["O"] * N)

def print_board(board):
    for row in board:
        print " ".join(row)
        
def clear():
    subprocess.call("clear", shell=True)


def refresh():
    for i in range(N + 4):
        sys.stdout.write("\033[A\033[2K")
    sys.stdout.flush()

print "\n\n   www              www   a      rrrrrrr\n    www            www   aaa     rr   rrr\n     www          www   aa aa    rr    rrr\n      www   w    www   aa   aa   rr   rrr\n       ww  w  w  ww   aa     aa  rrrrrrr \n       ww w    w ww   aaaaaaaaa  rr    rr\n        ww      ww   aa       aa rr     rr\n        w        w   aa       aa rrr     rr\n\n"
raw_input("press Enter")

clear()
print_board(board)

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)


for turn in range(TURNS):
		
    print "Turn ", turn +1
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    refresh()
    if guess_row-1 == ship_row and guess_col-1 == ship_col:
        print "Congratulations, Commander! You sunk enemy's battleship!"
        break
    else:
        if (guess_row < 0 or guess_row > N) or (guess_col < 0 or guess_col > N):
            print "Commander, are you drunk? Out of range"
        elif(board[guess_row-1][guess_col-1] == "X"):
            print "You have already tried that position, commander"
        else:
            print "Enemy is still hidden!"
            board[guess_row-1][guess_col-1] = "X"
            if (turn==TURNS):
                print 'You\'ve lost the battle!'
        
        print_board(board)
