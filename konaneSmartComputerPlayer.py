"""
@author: Chinedu Emeka

This is an AI agent which plays the game of Konane. 
It uses an evaluation function along with minimax (alpha beta pruning used to improve efficiency).
Implementation is in Python 2.7

"""



from copy import deepcopy; #importing functionality that will help me copy lists later on



#  Given a move that is possible to make, this method makes it. 
#  Inputs are:
#  board sq the player in question, 'x' or 'o' othersq  the player being jumped over	from_rowfrom_colto_rowto_col
def make_move(board, sq, othersq, from_row, from_col, to_row, to_col):
 
	(jump_over, jump_land) = jumppathValues(from_row, from_col, to_row, to_col)
	for i,j in jump_over:
                board[i][j] = ' '
                board[to_row][to_col] = sq
                board[from_row][from_col] = ' '
	return True;



class Konane:
	def __init__(self, board, who, print_board):
                self.board = board
                self.print_board = print_board
                self.who = who

	# checks if the current player has any possible moves left. 
	def gameDone(self, mover):
                possibleMoves = genmoves(self.board, mover); 
                if (len(possibleMoves) !=  0):
                        return None 
                return 1;


	# this method is responsible for determining the next move of the computer
	def move(self):
   	 
               
                possibleMoves = genmoves(self.board, self.who); #generate a list of all possible moves for all x's or o's. this is a list of tuples
                print "These are the possible moves for {player} = {val}".format(val = possibleMoves,  player = self.who);

                #the rootNode has data about the current state of the board. 
                rootNode = Node(0, self.board, None, self.who);
                
                #run minimax is called to determine the best move, which it returns. 
                bestMove = run_minimax(rootNode);

                #if minimax does not return a move, then we have a default move. However, the if statement below should never evaluate to true
                #This is because, if there are no moves, then the game would be over.
                
                if bestMove == None:
                        bestMove = (1,2,3,8);
                        
                return bestMove;
          
#This method is the evaluation function. It takes a board, and a player and returns an estimate of how good a current game state is.
#The goal is to minimize the opponent's moves, while maximizing the current player's move, with greater emphasis placed on maximizing the current player's move

def staticEval(board, who):
    #ALERT! If any changes are to be made to a board, then we would need a deep copy of the board.
    #Not making a deepcopy makes the code faster.
        
        miniBoard = board;
        othersq = "unknown"
        if (who == "x"):
                othersq = "o"
        else:
                othersq = "x";

        movesForMe = genmoves(miniBoard, who);
        a = len(movesForMe);
        a = a * 5

        movesForOpponent = genmoves(miniBoard, othersq);
        b = len(movesForOpponent);
        b = b * 3;

        
        score = 0;

        if (b == 0):
          score = 1000000;
        else:
            #a and b are weighted. a has a larger weight than b    
            score =  a - b;
            
        return score;



#  The Node class contains:
#	chlidren (list of child nodes)
#	level (0=root)
#	score ('' = unvisited node)
#	terminal (None = interior node)
#	best (None = not selected as best, anything else = selected)
#




class Node:
	def __init__(self, level, board, move, who, score='', terminal=None):
                self.children = []
                self.score = score
                self.level = level
                self.terminal = terminal
                self.best = None
                self.board = board;
                self.move = move;
                self.who = who;
        




    
	 
def makeChildren(node, level):
	possibleMoves = genmoves(node.board, node.who); #generate a list of all possible moves for all x's or o's. this is a list of tuples
	otherSq = "unknown"
	if (node.who == "x"):
    	  otherSq = "o"
	else:
    	  otherSq = "x";
   	 
	for move in possibleMoves:
                boardCopy = deepcopy(node.board);
                make_move(boardCopy, node.who, otherSq, move[0], move[1], move[2], move[3]);
                newNode = Node(node.level + 1, boardCopy, move, otherSq);
                node.children.append(newNode);


#run_minimax returns the best node at the top level
def run_minimax(gametree):
   val = run_minimaxAB(gametree, float("inf"), float("-inf"), 0, 3)
   bestMove = None;
   for child in gametree.children:
 	if (child.best == True):
     	   bestMove = child.move
     	   break;
   return bestMove;


#run_minimaxAB is the same as run_minimax but applies cutoffs to the tree. In addition, it also has information about how many layers deep we've gone.
#If we have reached the maximum number of layers specified, it stops descending and calls staticEval to evaluate the board.   
def run_minimaxAB(gametree, A, B, i, limit):
   if gametree.terminal == True:
  	return gametree.score;
   elif i >= limit: #we've gone as many times as we're allowed. This allows us to stop going forward and simply score what we have
   	if i  % 2 == 0:
        	return staticEval(gametree.board, gametree.who)
   	else:
        	return -1 * staticEval(gametree.board, gametree.who)
   else:
  	bestChild = None; #no best child yet
  	if gametree.level % 2 == 0: #we are at a max level
                score = float("-inf")
                makeChildren(gametree, i)
            
                if len(gametree.children) == 0:
                        val =  staticEval(gametree.board, gametree.who);
                        return val;
                bestChild = gametree.children[0]
                for child in gametree.children:
                        val = run_minimaxAB(child, A, score, i + 1, limit);
                        if val > score:
                           score = val;
                           
                           if i == 0:   #only get info about the bestChild if we are at the top layer of the game tree. 
                                bestChild = child;
                                
                        if score > A:
                           break;
                        
                if i == 0: #if we are at the top node, then set bestChild.best.  
                   bestChild.best = True;
                gametree.score = score;
                return score;
        
  	elif gametree.level % 2 == 1: #we are at a min level
                score = float("inf")
                makeChildren(gametree, i)
                if len(gametree.children) == 0:
                        val =  -1 * staticEval(gametree.board, gametree.who);
                       # print "The value being returned here is {}".format(val);
                        return  val;
                for child in gametree.children:
                        val = run_minimaxAB(child, score, A, i + 1, limit);
                        if val < score:
                          score = val;
                         
                        if score < B:
                          break;
                
                gametree.score = score;
                return score;



# ----------------------------------------------------------------------------------------
#From this point on, the methods here are "konaneutils."   


#  List of all possible board positions for each player
def each_players_places():

    places = {'x':[], 'o':[]}
    for i in range(8):
        for j in range(0,8,2):
            if i%2 == 0:
                places['x'].append((i, j))
                places['o'].append((i, j+1))
            else:
                places['o'].append((i, j))
                places['x'].append((i, j+1))
    return places


places = each_players_places();

# Determine whether a piece is moveable
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


#  Compute the squares being jumped over in a proposed move.
#  Returns two lists:
#    (i,j) tuples of the jumped-over positions.
#    (i,j) tuples of the intermediate landing positions
#
def jumppath(lorow, locol, hirow, hicol):
    if lorow == hirow:
        jump_over = [(hirow, j) for j in range(locol+1, hicol, 2)]
        jump_land = [(hirow, j) for j in range(locol+2, hicol, 2)]
        return (jump_over, jump_land)
    elif locol == hicol:
        jump_over = [(i, hicol) for i in range(lorow+1, hirow, 2)]
        jump_land = [(i, hicol) for i in range(lorow+2, hirow, 2)]
        return (jump_over, jump_land)
    else:
        return (None, None)


# For one starting position, all possible jump destinations
def dests_from(from_row, from_col):
    dests = []
    for j in range(from_col%2, 8, 2):
        if not j==from_col:
            dests.append((from_row, j))
    for i in range(from_row%2, 8, 2):
        if not i==from_row:
            dests.append((i, from_col))
    return dests

#  This is a variation of the original jumppath method found in konaneutils.py. This method is used in conjuction with the movePossible method to ascertain if a move is possible. 
def jumppathValues(from_row, from_col, to_row, to_col):
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


#this method tells us if a move is possible or not. 
def movePossible(board, sq, from_row, from_col, to_row, to_col):  
    if (sq == "x"):
        othersq = "o";
        
    elif (sq == "o"):
        othersq = "x";
        
    if not board[from_row][from_col] == sq:
        return False
    if not board[to_row][to_col] == ' ':
        return False;
    (jump_over, jump_land) = jumppathValues(from_row, from_col, to_row, to_col)
    if not jump_over:
        return False;
    for i,j in jump_over:
        if not board[i][j] == othersq:
            return False;
    for i,j in jump_land:
        if not board[i][j] == ' ':
            return False;
    return True;

#  Generate all possible moves
#  Returns list of 4-tuples
#
def genmoves(b, mover):  #original genmoves
    successors = []

    for from_row, from_col in places[mover]:  # places that mover can be
        if not moveable(from_row, from_col, b):
            continue;
        dests = dests_from(from_row, from_col)
        for to_row, to_col in dests:
            if movePossible(b, mover, from_row, from_col, to_row, to_col) == False:
                continue;
            succ = (from_row, from_col, to_row, to_col);
            if succ:
                successors.append(succ)

    return successors
