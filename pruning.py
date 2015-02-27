board = "- - - - - - - - -".split()
import sys
import random
import getopt

moves = (0,1,2,3,4,5,6,7,8)
X_token = -1
Open_token = 0
O_token = 1
rtokens = {-1: 'X', 0: '-', 1:'O'}
tokens = {'X': -1, 'O': 1, '-': 0}
MARKERS = ['-', 'O', 'X']
END_PHRASE = ('draw', 'win', 'loss')

HUMAN = 1
COMPUTER = 0

##
WINPOS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
final_board={}


#Json Schema for the structure for the final_board
#final_board = {
#               0(This represents the small board number) : { 0:'',1:'',2:''......8:'',win:('o' for o and 'x' for x and '-' for none)  This contains the info about that small board}
#		}
#An example for the above json schema
#final_board = { 0:{1:'x',2:'o',3:'-',4:'x',5:'-',6:'x',7:'-',8:'-','win':'-'}}

def winner(board):
	for each in WINPOS:
		sum = tokens[final_board[each[0]]['win']]+tokens[final_board[each[1]]['win']]+tokens[board[each[2]]['win']]
		if sum == 3 or sum == -3:
			return tokens[board[each[0]]]
	return 0

def availMoves(board):
	temp = []
	currBoard = board['board']
	for x in xrange(0,3):
		for y in xrange(0,3):
#			print 'THIS:', board['board']
			if currBoard[x][y] == '-':
				temp.append((x,y))
	return temp

CAUSES = ('draw', 'win', 'loss')
def move_left(board):
	for each in moves:
		if board[each] == '-':
			return True
	return False
board[0] = 'X'
board[2] = 'O'
board[1] = 'X'
small_board = 0;
def minmax(board,small_board,player, next_player, alpha, beta):
	winnr = winner(final_board)
	if winnr!=Open_token:
		return winnr
	elif not move_left(board):
		return 0
	if small_board!=10:
	    for move in moves:
		if final_board[small_board][move] == rtokens[Open_token]:
			final_board[small_board][move] = rtokens[player]
			val = minmax(final_board,small_board,next_player, player, alpha, beta)
			final_board[small_board][move] = rtokens[Open_token]
			if player == O_token:  # Maximizing player
				if val > alpha:
					alpha = val
				if alpha >= beta:
					return beta
			else:  # X_token player, minimizing
				if val < beta:
					beta = val
				if beta <= alpha:
					return alpha
            if player == O_token:
		retval = alpha
	    else:
		retval = beta
	return retval

def determine(final_board,small_board):
	if small_board!= 10:
	    best_val = -2
	    my_moves = []
	    for move in moves:
	    	    if final_board[small_board][move] == rtokens[Open_token]:
		            final_board[small_board][move] = rtokens[O_token]
			    val = minmax(final_board,small_board,X_token, O_token, -2, 2)
			    final_board[small_board][move] = rtokens[Open_token]
			    print move, ' causes ', CAUSES[val]
			    if val> best_val:
				    best_val = val
				    my_moves = [move]
			    elif val == best_val:
				    my_moves.append(move)
	return random.choice(my_moves)
print board
#small_board = 10 represents the free choice to play at any board
final = determine(board,small_board)
print "I pick ", final
