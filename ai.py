from random import choice

#Credit to divyesh072019 for this code
def isMovesLeft(board) :
 
    for i in range(3) :
        for j in range(3) :
            if (not board[i][j]) :
                return True
    return False
 
def evaluate(b, bot, opponent) :
   
    # Checking for Rows for X or O victory.
    for row in range(3) :    
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :       
            if (b[row][0] == bot) :
                return 10
            elif (b[row][0] == opponent) :
                return -10
 
    # Checking for Columns for X or O victory.
    for col in range(3) :
      
        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) :
         
            if (b[0][col] == bot) :
                return 10
            elif (b[0][col] == opponent) :
                return -10
 
    # Checking for Diagonals for X or O victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
     
        if (b[0][0] == bot) :
            return 10
        elif (b[0][0] == opponent) :
            return -10
 
    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
     
        if (b[0][2] == bot) :
            return 10
        elif (b[0][2] == opponent) :
            return -10
 
    # Else if none of them have won then return 0
    return 0
 

def minimax(board, depth, is_max, bot, opponent) :
    score = evaluate(board, bot, opponent)
 
    # If Maximizer has won the game return his/her
    # evaluated score
    if (score == 10) :
        return score
 
    # If Minimizer has won the game return his/her
    # evaluated score
    if (score == -10) :
        return score
 
    # If there are no more moves and no winner then
    # it is a tie
    if (isMovesLeft(board) == False) :
        return 0
 
    # If this maximizer's move
    if (is_max) :    
        best = -1000
 
        # Traverse all cells
        for i in range(3) :        
            for j in range(3) :
              
                # Check if cell is empty
                if (not board[i][j]) :
                 
                    # Make the move
                    board[i][j] = bot
 
                    # Call minimax recursively and choose
                    # the maximum value
                    best = max( best, minimax(board,
                                              depth + 1,
                                              not is_max, bot, opponent) )
 
                    # Undo the move
                    board[i][j] = ""
        return best
 
    # If this minimizer's move
    else :
        best = 1000
 
        # Traverse all cells
        for i in range(3) :        
            for j in range(3) :
              
                # Check if cell is empty
                if (not board[i][j]) :
                 
                    # Make the move
                    board[i][j] = opponent
 
                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not is_max, bot, opponent))
 
                    # Undo the move
                    board[i][j] = ""
        return best
 
# This will return the best possible move for the player
def find_best_move(board, bot, opponent, mark_count) :
    best_val = -1000
    best_move = (-1, -1)
    board = [[box.text() for box in row] for row in board.values()]

    if mark_count < 9:
        if mark_count == 0:
            i = choice([0, 2])
            if i == 1:
                j = choice([0, 1, 2])
            else:
                j = choice([0, 2])
            return (i, j)
        else:
            for i in range(3) :    
                for j in range(3):
                 
                    # Check if cell is empty
                    if not board[i][j]:
                     
                        # Make the move
                        board[i][j] = bot
 
                        # compute evaluation function for this
                        # move.
                        move_val = minimax(board, 0, False, bot, opponent)
 
                        # Undo the move
                        board[i][j] = ""
 
                        # If the value of the current move is
                        # more than the best value, then update
                        # best/
                        if move_val > best_val:               
                            best_move = (i, j)
                            best_val = move_val
 
    return best_move
