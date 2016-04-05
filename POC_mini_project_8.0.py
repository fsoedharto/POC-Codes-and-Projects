"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import math
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(80)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    
    # Call a variable called other player
    other_player = provided.switch_player(player)
    
    # The base case
    if board.check_win() != None:
        if board.check_win() == player:
            return SCORES[player], None
        elif board.check_win() == other_player:
            return SCORES[other_player], None
        else:
            return SCORES[board.check_win()], None
    
    # Recursive case
    else:
        
        # Gets all the empty squares
        score_move_list = []
        for dummy_move in board.get_empty_squares():
            board_clone = board.clone()
            board_clone.move(dummy_move[0], dummy_move[1], player)
            scoring = mm_move(board_clone, other_player)
            score_move_list.append((scoring[0], dummy_move))
        
        max_score = float('-inf')
        min_score = float('+inf')
        max_move = None
        min_move = None
        
        if player == provided.PLAYERX:
            for dummy_move_score in score_move_list:
                if dummy_move_score[0] > max_score:
                    max_score = dummy_move_score[0]
                    max_move = dummy_move_score[1]
            return max_score, max_move
        else:
            for dummy_move_score in score_move_list:
                if dummy_move_score[0] < min_score:
                    min_score = dummy_move_score[0]
                    min_move = dummy_move_score[1]
            return min_score, min_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
