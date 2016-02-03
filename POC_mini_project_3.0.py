"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 200       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This functions should take the current board and make
    moves by two players
    """
    
    # Proceed with the game there is at least an empty square or
    # the game has not yet have a winner
    while board.check_win() == None:
        
        # Get a list of empty squares
        empty_square_list = board.get_empty_squares()
    
        # Randomly picked one of the coordinates of the list
        get_random_square = random.randrange(len(empty_square_list))
        get_row_col = empty_square_list[get_random_square]
        rand_row = get_row_col[0]
        rand_col = get_row_col[1]
    
        # Use the randomly obtained square and column to place
        # the "X" or "O"
        board.move(rand_row, rand_col, player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function should update the scores
    """
    # If current player win, then add the scores from the
    # current player and subtract the scores from the
    # other player
    if board.check_win() == player:
        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] += SCORE_CURRENT
                if board.square(dummy_row, dummy_col) == provided.switch_player(player):
                    scores[dummy_row][dummy_col] -= SCORE_OTHER
                    
    # If lose then subtract score of the other player and
    # add the scores from the other player
    elif board.check_win() == provided.switch_player(player):
        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] -= SCORE_CURRENT
                if board.square(dummy_row, dummy_col) == provided.switch_player(player):
                    scores[dummy_row][dummy_col] += SCORE_OTHER
    
    # If draw, then do nothing
    else:
        pass
    
def get_best_move(board, scores):
    """
    This function should return the best move from the
    list of empty squares and takes the best move as the
    one with the maximum score
    """
    
    # This should list all the empty squares
    empty_square_list = board.get_empty_squares()
    
    # Initializes the score to have a point of comparison
    row, col = empty_square_list[0]
    max_score = scores[row][col]
    max_row_col = (row, col)
    
    # Reiterates the list of empty squares and check for
    # the maximum scores
    for empty_square_dummy in empty_square_list:
        row, col = empty_square_dummy
        if scores[row][col] > max_score:
            max_score = scores[row][col]
            max_row_col = (row, col)

    return max_row_col

def mc_move(board, player, trials):
    """
    This function combines the previous functions
    """
    
    # Create a clone of the board
    scores = [[0] * board.get_dim() for dummy_idx in range(board.get_dim())]
    for dummy_trial in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
    
    return get_best_move(board, scores)

# Test functions
# Board = provided.TTTBoard(3, False, None)

# print scores

# Test the board
# print str(board), "board should be empty and 3x3\n"

# Test the board with 4 x 4 or higher
# board = provided.TTTBoard(4, False, None)
# print str(board), "board should be empty and 4x4"
# print "Evaluated:", board.get_dim(), "This should be: 4"
# print "Evaluated:", board.square(0, 0), "This should be: 1"
# print "Empty Squares:", board.get_empty_squares(), "Expected: all of them"
# print board.check_win(), "Expected: NONE"
# print board.get_empty_squares()[0]

# Test the board with a provided 3 x 3 board
# board = provided.TTTBoard(3, False, [[1, 3, 3], [1, 2, 3], [2, 3, 2]])
# print str(board), "board should be [ , X, O], [ , X, O], and [X, O, X] and 3x3"
# print "Evaluated:", board.get_dim(), "This should be: 3"
# print "Empty Squares:", board.get_empty_squares(), "Expected: (0, 0) and (1, 0)"
# board.move(0, 0, 3)
# print str(board)
# board.move(0, 0, 2)
# print str(board)
# board.move(1, 0, 2)
# print str(board)
# print board.check_win(), "Expected: (3) Draw"

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
