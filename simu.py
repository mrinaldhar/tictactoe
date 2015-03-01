import sys
import random
import signal

#Timer handler, helper function

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))

moves = (0,1,2,3,4,5,6,7,8)
X_token = -1
Open_token = 0
O_token = 1
rtokens = {-1: 'x', 0: '-', 1:'o'}
tokens = {'x': -1, 'o': 1, '-': 0}
MARKERS = ['-', 'o', 'x']
END_PHRASE = ('draw', 'win', 'loss')

HUMAN = 1
COMPUTER = 0

##
WINPOS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
final_board={0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{}}

small_board = 0;
CAUSES = ('draw', 'win', 'loss')


def winner(final_board,player,next_player):
	for each in WINPOS:
		sum = 0
		for i in each:
			if(final_board[i]['win'] == rtokens[player]):
				sum += 1
			elif(final_board[i]['win'] == rtokens[next_player]):
				sum -= 1
		if sum == 3:
		        return 100000
		elif sum == -3: 
		        return -100000
	return 0

def config_win(small_config):
#	# print 'small_config'
#	# print small_config
	for each in WINPOS:
		sum = tokens[small_config[each[0]]] + tokens[small_config[each[1]]] + tokens[small_config[each[2]]]
		if sum == 3:
			small_config['win'] = 'o'
			return
		if sum == -3:
			small_config['win'] = 'x'
			return
		else:
			small_config['win'] = '-'

def availMoves(board):
	temp = []
	currBoard = board['board']
	for x in xrange(0,3):
		for y in xrange(0,3):
#      	                # print 'THIS:', board['board']
			if currBoard[x][y] == '-':
				temp.append((x,y))
	return temp

def move_left(board):
	for each in moves:
		if board[each] == '-':
			return True
	return False

def eval_small(small_board,player,next_player):
	sum = 0
	oppo_sum = 0
	heuristic = 0
	global WINPOS
	for each in WINPOS:
		sum = 0
		oppo_sum = 0
	        for i in each:
	            if(small_board[i] == rtokens[player]):
			    sum += 1
	            elif(small_board[i] == rtokens[next_player]):
                            oppo_sum += 1
		if(sum > 0):
	        	heuristic = heuristic + (pow(10,sum))
		if(oppo_sum > 0):
	        	heuristic = heuristic - (pow(10,oppo_sum))
	return heuristic

def evaluate(final_board,player,next_player):
	global WINPOS
	heuristic = 0
        for each in WINPOS:
		 sum = 0
	         oppo_sum = 0
	         if(final_board[each[0]]['win'] == rtokens[player]):
			 sum += 1;
		 if(final_board[each[1]]['win'] == rtokens[player]):
			 sum += 1;
		 if(final_board[each[2]]['win'] == rtokens[player]):
			 sum += 1;
#       if((final_board[each[1]]['win'] == rtokens[next_player]) or (final_board[each[0]]['win'] != rtokens[next_player]) or (final_board[each[2]]['win'] != rtokens[next_player])):
#			 sum = 0; #As their is no chance of winning in this position
                 if(final_board[each[0]]['win'] == rtokens[next_player]):
			 oppo_sum -= 1;
	         if(final_board[each[1]]['win'] == rtokens[next_player]):
			 oppo_sum -= 1;
		 if(final_board[each[2]]['win'] == rtokens[next_player]):
			 oppo_sum -= 1;
		 if(sum>0):
		 	heuristic = heuristic + 100*pow(10,sum)
		 if(oppo_sum < 0):
		 	heuristic = heuristic - 100*pow(10,-oppo_sum)
	for small_board in final_board:
	        heuristic = heuristic + eval_small(final_board[small_board], player, next_player)
	return heuristic


def valid_moves(final_board,last_move):
   	small_board = last_move[1]
	if (small_board == -1):
		small_boards = [0,1,2,3,4,5,6,7,8]
	elif(small_board == 0):
		small_boards = [0,1,3]
	elif (small_board == 2):
		small_boards = [1,2,5]
	elif (small_board == 6):
		small_boards = [3,6,7]
	elif (small_board == 8):
		small_boards  = [7,8,5]
	else:
		small_boards = [small_board]
 
	if (len(small_boards) > 0):
		temp_small_board = small_boards[:]
		for i in small_boards:
			if(final_board[i]['win']!=rtokens[Open_token]):
				temp_small_board.remove(i)
		small_boards = temp_small_board[:]
	if (len(small_boards)==0):
		small_boards = choose_board(final_board)
	valid_moves = []
	for small_board in small_boards:
 		for i in final_board[small_board]:
			if i!='win' and final_board[small_board][i] == rtokens[Open_token]:
				valid_moves.append((small_board,i))
#	# print "SEE THIS:::", valid_moves
 	return valid_moves

def minmax(final_board,player, next_player, alpha, beta,depth,last_move):
	winnr = winner(final_board,next_player,player)
	if winnr!=Open_token:
		return winnr*100
#	elif not move_left(final_board):
#		return 0
	moves = []
	moves = valid_moves(final_board,last_move)
	# print 'Moves'
	# print moves
	if 1:
		for move in moves:
#			# print 'depth ', depth
			if final_board[move[0]][move[1]] == rtokens[Open_token]:
		                temp_dict = {}
				for i in final_board:
				        temp_dict[i] = final_board[i]
				final_board[move[0]][move[1]] = rtokens[player]
				for i in final_board:
					config_win(final_board[i])
				i = 0
				string = ''
				while(i<depth):
					string = string + '    '
					i = i + 1
				# print string + 'move: ', move
				# print move
				# print move
				# print rtokens[player]
				if(depth==3):
					# print 'This is the val at depth 3'
					if(depth%2 != 0):
						val = evaluate(final_board,next_player,player)
					else:
						val = evaluate(final_board,player,next_player)
					# print val
				else:
					val = minmax(final_board,next_player, player, alpha, beta,depth+1,move)
					# print 'This is the val at initial depths'
					# print val
				# print "I am refreshing the array"
				final_board[move[0]][move[1]] = rtokens[Open_token]
				for i in final_board:
					config_win(final_board[i])
				# print 'alpha beta val', alpha, beta, val
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
				final_board = temp_dict
		if player == O_token:
			retval = alpha
		else:
			retval = beta
	return retval

def choose_board(final_board):   #This function will contain the intelligence for choosing the small board in case of free choice
	small_boards = []
	for small_board in final_board:
	        if (final_board[small_board]['win']==rtokens[Open_token]):
			for i in xrange(0,9):
				if (final_board[small_board][i]==rtokens[Open_token]):
					small_boards.append(small_board)
					break
	return small_boards

def determine(final_board,small_board):
	my_moves = []
	if (small_board == -1):
		small_boards = [0,1,2,3,4,5,6,7,8]
	elif(small_board == 0):
		small_boards = [0,1,3]
	elif (small_board == 2):
		small_boards = [1,2,5]
	elif (small_board == 6):
		small_boards = [3,6,7]
	elif (small_board == 8):
		small_boards  = [7,8,5]
	else:
		small_boards = [small_board]
	# print small_boards
	# print final_board
	# print "small_boards1", small_boards
	temp_small_board = small_boards[:]
	if (len(small_boards) > 0):
		for i in small_boards:
			# print i, final_board[i]['win']
			if(final_board[i]['win']!=rtokens[Open_token]):
				temp_small_board.remove(i)
	small_boards = temp_small_board[:]
	temp_list = []
	# print "small_boards2", small_boards

	if (len(small_boards) > 0):
		for small_board in small_boards:
			for i in xrange(0,9):
				if(final_board[small_board][i] == rtokens[Open_token]):
					temp_list.append(small_board)
					break
	small_boards = temp_list
	# print "small_boards", small_boards
	if (len(small_boards)==0):
		small_boards = choose_board(final_board)
	best = -10000000
	# print "SMALL_BOARDS::", small_boards
	temp_dict = {}
	for small_board in small_boards:
	        temp_dict = {}
		for i in final_board:
		        temp_dict[i] = final_board[i]
		temp = ret_val(final_board,small_board)
		# print "SOMETEMP::", temp
		if temp[0]>best:
			# print "TEMP..", temp[1]
			best = temp[0]
			my_moves = [temp[1]]
		final_board = temp_dict
	# print "LIST SIZE:", len(my_moves)
	return my_moves[0]


def ret_val(final_board,small_board):
	best_val = -1000000;
	# print "begin again!"
	my_moves = []
	temp_dict = {}
	for i in final_board:
	        temp_dict.update({i:final_board[i]})
#	# print 'This is the temp_dict'
#	# print temp_dict
#	# print 'This is the final board'
#	# print final_board
	moves = [0,1,2,3,4,5,6,7,8]
	# print moves
	for move in moves:
		if final_board[small_board][move] == rtokens[Open_token] and final_board[small_board]['win'] == rtokens[Open_token]:
		        for i in final_board:
			        config_win(final_board[i])
			# print "Hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
			# print 'Move: ', small_board,move
			final_board[small_board][move] = rtokens[O_token]
			val = minmax(final_board,-O_token,+O_token,-1000000,1000000,1,(small_board,move))
			# print "Val: ", val, small_board
#			# print "O_token ", O_token
			# print final_board[small_board]
#			# print "OLD", final_board[small_board][move]
			final_board[small_board][move] = rtokens[Open_token]
			for i in final_board:
				config_win(final_board[i])
#			# print "NEW", final_board[small_board][move]
#                        # print final_board

			if val > best_val:
				# print "VAL::", val
				# print "MOVE::", move
				best_val= val
				my_moves = [(small_board,move)]
			elif val == best_val:
				# print "2VAL::", val
				# print "2MOVE::", move
				my_moves.append((small_board, move))
         
			final_board = temp_dict
	# print "LIST SIZE2:", len(my_moves)
	return (best_val,my_moves[0])


class Player1:
	
	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		global O_token, X_token
		if flag == 'x':
			O_token = -1
			X_token = 1
		else:
			O_token = 1
			X_token = -1
		if(old_move == (-1,-1)):
			return (4,4)
		# print 'This is the temp_board'
		# print temp_board
		final_board={0:{},1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{}}
		small_board = 0;
		i = 0
		j = 0
		count = 0
		for x in xrange(0,9):
			for y in xrange(0,9):
				m = 3*(x/3) + (y/3)
				n = 3*(x%3) + (y%3)
				final_board[m][n] = temp_board[x][y]
				if (final_board[m][n] != '-'):
					count = count + 1
	        for i in final_board:
	                config_win(final_board[i])
		# print  final_board
		# print old_move
		x = old_move[1]
		y = old_move[0]
		small_board = 3*(y%3) + (x%3)
		# print 'small_board'
	  	final = determine(final_board,small_board)
		# print "Last move ", old_move
		# print final_board
	   	# print "I pick ", final
	        x = final[0]
	        y = final[1]
	        row = 3*(x/3) + (y/3)
	        column = 3*(x%3) + (y%3)
		# print "MY ANS::"
		# print (row, column)
	   	return (row,column)
	   	
class Player2:
	
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]
                
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]
	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0,1,3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

        #Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            if block_stat[i] != '-':
                blocks_allowed.remove(i)
        
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)
	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        #check for draw on the block.

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

def terminal_state_reached(game_board, block_stat):
	
        #Check if game is won!
        bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
                        #Changed scoring mechanism
                        # 1. If there is a tie, player with more boxes won, wins.
                        # 2. If no of boxes won is the same, player with more corner move, wins. 
                        point1 = 0
                        point2 = 0
                        for i in block_stat:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
                                        if i%3!=1 and j%3!=1:
                                            if game_board[i][j] == 'x':
                                                point1+=1
                                            elif game_board[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'P1'
			        elif point2>point1:
				    return True, 'P2'
                                else:
				    return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 60

	print_lists(game_board, block_stat)

	while(1):

		# Player1 will move
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
                update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

                # Now player2 plays

                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER + " won!"
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player1()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()

	# O_token = 1
	# simulate(obj2, obj1)
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
        num = random.uniform(0,1)
        if num > 0.5:
        	print "You are P2"
		simulate(obj2, obj1)
	else:
		print "You are P1"
		simulate(obj1, obj2)

