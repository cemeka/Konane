#!/usr/bin/env python
#
#  Computer-to-computer Konane driver.
#
#  To use:
#     python konanec2c.py user1.py user2.py ... (at least 2 users)
#
#  Where each user.py or user.pyc file contains a Konane class.
#
#  User .pyc files (already compiled) can also be used  instead of .py
#

import sys
import os.path
import time

#  Import list of modules.
#
def fetch_modules(modlist):
    mods = {}
    for modname in modlist:
        modname, ext = os.path.splitext(modname)
        try:
            modul = __import__(modname)
        except ImportError:
            print "Cannot import", modname
        mods[modname] = modul
    return mods

#  Prompt user for two contestants
#
def pick_contestants(mods):
    s = raw_input("New game? [y]/n: ")
    if not (len(s) == 0 or s[0] == 'y' or s[0] == 'Y'):
        sys.exit()
    # if len(mods.keys()) == 2:
    #    return mods.keys()
    print mods.keys()
    while 1:
        c1 = raw_input("Contestant X: ")
        if c1 == 'exit' or c1 == 'quit': sys.exit()
        if c1 in mods: break
    while 1:
        c2 = raw_input("Contestant O: ")
        if c1 == 'exit' or c1 == 'quit': sys.exit()
        if c2 in mods: break
    return (c1, c2)
        

#  Encode a move (four numbers) into two board positions
#
def encode_move(from_row, from_col, to_row, to_col):
    if not (0 <= from_row and from_row <= 7 and
            0 <= to_row and to_row <= 7 and
            0 <= from_col and from_col <= 7 and
            0 <= to_col and to_col <= 7):
        print "Illegal move from=(%d,%d) to=(%d,%d)" % \
               (from_row, from_col, to_row, to_col)
        sys.exit(1)
    else:
        return str(from_row) + 'abcdefgh'[from_col] + ' ' + \
               str(to_row)  + 'abcdefgh'[to_col]


#  Move.  Return None if move is not possible.
#  If the move is possible, the board is modified.
#
#  Inputs are:
#     board
#     sq       the player in question, 'x' or 'o'
#     othersq  the player being jumped over
#     from_row
#     from_col
#     to_row
#     to_col
#
#  make_move leaves . (dot) in place of the removed pieces, and
#  capitalizes the moved piece for emphasis.  cleanup_move() is
#  called to clean this stuff up after printing.
#
def make_move(board, sq, othersq, from_row, from_col, to_row, to_col):
    if not board[from_row][from_col] == sq: return None
    if not board[to_row][to_col] == ' ': return None
    (jump_over, jump_land) = jumppath(from_row, from_col, to_row, to_col)
    if not jump_over: return None
    for i,j in jump_over:
        if not board[i][j] == othersq: return None
    for i,j in jump_land:
        if not board[i][j] == ' ': return None
    for i,j in jump_over:
        board[i][j] = '.'
    for i,j in jump_land:
        board[i][j] = '.'
    board[to_row][to_col] = sq.capitalize()
    board[from_row][from_col] = '.'
    return 1

#  Cleanup_move cleans out the emphasis characters left my make_move
#
def cleanup_move(b):
    for i in range(len(b)):
        for j in range(len(b[i])):
            char = b[i][j]
            if char == '.' or char == '*':
                b[i][j] = ' '
            else:
                b[i][j] = b[i][j].lower()

                
#  Compute the squares being jumped over in a proposed move.
#  Returns two lists:
#    (i,j) tuples of the jumped-over positions.
#    (i,j) tuples of the intermediate landing positions
#
def jumppath(from_row, from_col, to_row, to_col):
    if from_row == to_row:
        jump_over = [(to_row, j) for j \
            in range(min(from_col, to_col)+1, max(from_col, to_col), 2)]
        jump_land = [(to_row, j) for j \
            in range(min(from_col, to_col)+2, max(from_col, to_col), 2)]
        return (jump_over, jump_land)
    elif from_col == to_col:
        jump_over = [(i, to_col) for i \
            in range(min(from_row, to_row)+1, max(from_row, to_row), 2)]
        jump_land = [(i, to_col) for i \
            in range(min(from_row, to_row)+2, max(from_row, to_row), 2)]
        return (jump_over, jump_land)

    else:
        return (None, None)

#  Return None if the game is lost for a mover
#
#  Checks each possible place the mover can be, and sees if a
#  move is possible.
#
def game_lost(mover, b):
    for i, j in places[mover]:
        if moveable(i, j, b): return None
    return 1

# Return 1 when a piece is moveable from this position
#
def moveable(from_row, from_col, b):
    if b[from_row][from_col] == ' ': return None
    if from_row > 1:
        if (not b[from_row-1][from_col] == ' ') and \
            (b[from_row-2][from_col] == ' '): return 1
    if from_row < 6:
        if (not b[from_row+1][from_col] == ' ') and \
            (b[from_row+2][from_col] == ' '): return 1
    if from_col > 1:
        if (not b[from_row][from_col-1] == ' ') and \
            (b[from_row][from_col-2] == ' '): return 1
    if from_col < 6:
        if (not b[from_row][from_col+1] == ' ') and \
            (b[from_row][from_col+2] == ' '): return 1
    return None                

        
#  List of all possible board positions for each player
#
pieces = ('x', 'o')
places = {'x':[], 'o':[]}
def each_players_places():
    for i in range(8):
        for j in range(8):
            places[pieces[(i+j)%2]].append((i, j))


#  Populate the board
#
def populate_board():
    board = []
    for i in range(8):
        board.append([ pieces[(i+j)%2] for j in range(8)])
                       
    board[3][3] = ' '
    board[3][4] = ' '
    return board

#  A simple function to print the board
#
#  Optional emph argument is an (i,j) tuple board location to emphasize
#
def print_board(b):
    print '  a b c d e f g h'
    for i in range(len(b)):
        print str(i) + ' ' + ' '.join(b[i])


#  Usage messages
#
def usage():
    print "Usage: konanec2c.py user1.py user2.py ... (2 or more)"
    
# ----------- MAIN PROGRAM STARTS HERE
#
if len(sys.argv) < 3:
    usage()
mods = fetch_modules(sys.argv[1:])

if len(mods) < 2:
    usage()

each_players_places()
while 1:
    board = populate_board()
    c1, c2 = pick_contestants(mods)
    u1 = mods[c1].Konane(board, 'x', print_board)
    u2 = mods[c2].Konane(board, 'o', print_board)

    whonames = {'x' : c1, 'o' : c2 }
    players  = {'x' : u1, 'o' : u2 }
    times    = {'x' : 0.0, 'o' : 0.0 }
    mover, other = 'x', 'o'
    print_board(board)
    print
    
    while 1:
        if game_lost(mover, board):
            print other, "WINNER: ", whonames[other], " t=", times[other]
            print mover, " loser: ", whonames[mover], " t=", times[mover]
            break
        t0 = time.clock()
        fromto = players[mover].move()
        t1 = time.clock()
        times[mover] += (t1-t0)
        print mover, whonames[mover], "moves", encode_move(*fromto), " t=", t1-t0
        if not make_move(board, mover, other, *fromto):
            print "Illegal Move: forfeit"
            break
        else:
            print_board(board)
        cleanup_move(board)
        print
        # time.sleep(1)
        mover, other = other, mover

sys.exit(1)