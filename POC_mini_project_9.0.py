"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
import random
import codeskulptor

codeskulptor.set_timeout(200)

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        # Checks if the current row and column is zero
        if self.get_number(target_row, target_col) != 0:
            return False
        
        # Checks for the row below and see if it is solved
        # by reiterating through the lower list
        for dummy_idx in range(target_row + 1, self._height):
            for dummy_jdx in range(self._width):
                if self.get_number(dummy_idx, dummy_jdx) != (dummy_idx * self._width + dummy_jdx):
                    return False
        
        # Reiterates through the current column to the right
        # of the current row to see if they are solved
        for dummy_idx in range(target_col + 1, self._width):
            if self.get_number(target_row, dummy_idx) != (self._width * target_row + dummy_idx):
                return False
        
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        
        # Checks for invariant and give the current position
        # of the tile
        assert self.lower_row_invariant(target_row, target_col)
        location = self.current_position(target_row, target_col)
        
        # Reach for the target cell
        solve_string = self.reach_position(target_row, target_col, location)
        copy_solve_string = list(solve_string)
        solve_string = solve_string[0:len(solve_string) - 1]
        
        # Update the string using the solved position
        self.update_puzzle(solve_string)
        
        # Reiterate through the loop lower row invariant is
        # not true
        while self.lower_row_invariant(target_row, target_col - 1) is False:
            
            move_string = self.position_tile(target_row, target_col, (target_row, target_col), copy_solve_string)    
            
            # Update the puzzle copy and the string
            self.update_puzzle(move_string)
            solve_string += move_string
        
        return solve_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # Assert the lower row invariant is true
        assert self.lower_row_invariant(target_row, 0), "Lower row invariant at row = " + str(target_row)
        
        # Move the zero to position row m - 1, col = 1
        self.update_puzzle("ur")
        
        # Drag the number on the column into the 3 x 2 square
        # Let the zero reach the target location
        location = self.current_position(target_row, 0)
        zero_position = self.current_position(0, 0)
        
        # Fetch string is the difference from the zero location to the target location
        if self.current_position(target_row, 0) == (target_row, 0):
            solve_string = ""
        else:
            fetch_string = self.reach_position(zero_position[0], zero_position[1], location)
            solve_string = fetch_string[0:len(fetch_string) - 1]
            fetch_string = list(fetch_string)
        
        self.update_puzzle(solve_string)
        
        # Relocates the position of the target tile to
        # (i - 1, 1) and the zero tile to (i - 1, 0) 
        while self.lower_row_invariant(target_row - 1, self._width - 1) is False:
            
            zero_position = self.current_position(0, 0)

            # Case 1: when the zero col number is placed at its solved
            # location move the zero to (target_row - 1, self._width - 1)
            if self.current_position(target_row, 0) == (target_row, 0):
                move_string = self.reach_position(zero_position[0], zero_position[1], (target_row - 1, self._width - 1))
            # Case 2: the target is not at its solved position but
            # it is at (target_row - 1, 1)
            elif (zero_position == (target_row - 1, 0)) and (self.current_position(target_row, 0) == (target_row - 1, 1)):
                move_string = "ruldrdlurdluurddlu"
            else:
                move_string = self.position_tile(target_row, 0, (target_row - 1, 1), fetch_string)
                
            # Update string
            self.update_puzzle(move_string)
            solve_string += move_string
            
        return "ur" + solve_string
    
    def position_tile(self, target_row, target_col, location, copy_solve_string):
        """
        A helper function to position a tile to its target
        solved position.
        """
        
        if self.current_position(target_row, target_col) == location:
            if self.current_position(0, 0)[0] < self.current_position(target_row, target_col)[0]:
                move_string = "ld"
            else:
                move_string = "ulld"
        
        else:
            assert type(copy_solve_string) is list, "Target move type is not list!"
            assert len(copy_solve_string) > 0, "Target move is empty"
            target_move = copy_solve_string.pop(-1)
            
            if target_move == "l":
                move_string = self.move_left_right(target_row, target_col, target_move)
            elif target_move == "r":
                move_string = self.move_left_right(target_row, target_col, target_move)
            else:
                move_string = self.move_down(target_row, target_col)
        
        return move_string
    
    ##########################################################
    # Helper Move Functions
    
    def move_left_right(self, target_row, target_col, target_move):
        """
        Helper function to move the target block to the left.
        """
        if target_move == 'r':
            if self.current_position(target_row, target_col)[1] > self.current_position(0, 0)[1]:
                move_string = "r"
            elif self.current_position(target_row, target_col)[0] < self.current_position(0, 0)[0]:
                move_string = "lur"
            else:
                if self.current_position(target_row, target_col)[0] == 0:
                    move_string = "dllur"
                else:
                    move_string = "ulldr"
        
        elif target_move == 'l':
            if self.current_position(target_row, target_col)[1] < self.current_position(0, 0)[1]:
                move_string = "l"
            elif self.current_position(target_row, target_col)[0] < self.current_position(0, 0)[0]:
                move_string = "rul"
            else:
                if self.current_position(target_row, target_col)[0] == 0:
                    move_string = "drrul"
                else:
                    move_string = "urrdl"            
        
        return move_string
    
    def move_down(self, target_row, target_col):
        """
        Helper function to move the target block down.
        """
        
        if (self.current_position(target_row, target_col)[0] < self.current_position(0, 0)[0]):
            move_string = "u"
        elif (self.current_position(target_row, target_col)[0] > self.current_position(0, 0)[0]):
            move_string = "lddru"
        else:
            if (self.current_position(target_row, target_col)[1] > self.current_position(0, 0)[1]):
                move_string = "dru"
            elif self.current_position(target_row, target_col)[0] == 0:
                move_string = "dlludru"
            else:
                move_string = "ullddru"
        return move_string
    
    def reach_position(self, target_row, target_col, location):
        """
        A helper function to reach to the target position.
        target_row and target_col is the place where zero tile is located and the location
        is the target place
        """
        
        solve_string = ""
        assert type(location) is tuple or type(location) is list, "the variable location must be a tuple or list"
        assert len(location) == 2, "The variable location has to be of length two"
        assert location[0] >= 0, "Invalid Value!"
        assert location[1] >= 0, "Invalid Value!"
        assert target_row >= 0, "Invalid Value for row = " + str(target_row)
        assert target_col >= 0, "Invalid Value for col = " + str(target_col)    
        
        # calculate the number of up direction
        num_of_ups = target_row - location[0]
        assert num_of_ups >= 0, "Invalid Value! number of up directions = " + str(num_of_ups)
        assert num_of_ups <= self._height, "Invalid Value! number of up directions cannot be more than height: " + str(num_of_ups)
        
        # calculate the number of left or right directions
        num_of_lrs = target_col - location[1]
        assert abs(num_of_lrs) <= self._width, "Invalid Value! number of left / right cannot be more than width"
        
        # prints out the string
        for dummy_ups in range(num_of_ups):
            solve_string += "u"
        if num_of_lrs > 0:
            for dummy_lrs in range(num_of_lrs):
                solve_string += "l"
        else:
            for dummy_lrs in range(abs(num_of_lrs)):
                solve_string += "r"
        
        return solve_string
    
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Checks whether the zero is at (0, target_col)
        if self.current_position(0, 0) != (0, target_col):
            return False
        
        # Checks whether the row to the right of the zero
        # is placed at its solved position
        for dummy_col in range(target_col + 1, self._width):
            if self.current_position(0, dummy_col) != (0, dummy_col):
                return False
        
        # Checks whether the tiles in row 1 below target_col and
        # target_col + 1 are solved
        for dummy_col in range(target_col, self._width):
            if self.current_position(1, dummy_col) != (1, dummy_col):
                return False
        
        # Checks whether the rest of the row below row 1 are solved
        for dummy_row in range(2, self._height):
            for dummy_col in range(0, self._width):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):
                    return False
        
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        
        # Checked the invariant at row 0
        assert self.row0_invariant(target_col) is True, "Invariant violated for solved row0"
        
        # Move the 0 from the top of the row 1 col to row 1
        self.update_puzzle("ld")
        
        zero_position = self.current_position(0, 0)
        location = self.current_position(0, target_col)
        
        # Gererate a fetch string
        if self.current_position(0, target_col) != (0, target_col):
            solve_string = self.reach_position(zero_position[0], zero_position[1], location)
            copy_solve_string = list(solve_string)
            solve_string = solve_string[0:len(solve_string) - 1]
        else:
            solve_string = ""
            copy_solve_string = list(solve_string)
        
        # Update puzzle based on the solve_string
        self.update_puzzle(solve_string)
        
        # Move the zero tile until the target tile is placed
        # in its solved location
        while self.current_position(0, target_col) != (0, target_col):
            if (self.current_position(0, target_col) == (1, target_col - 1)) and (self.current_position(0, 0) == (1, target_col - 2)):
                move_string = "urdlurrdluldrruld"
            elif (self.current_position(0, target_col) == (1, target_col - 1)):
                move_string = "ld"
            else:
                move_string = self.position_tile(0, target_col, (1, target_col - 1), copy_solve_string)
            
            solve_string += move_string
            self.update_puzzle(move_string)
        
        # Check for invariance in the row 1 to the left of 
        # the target column
        assert self.row1_invariant(target_col - 1)
        
        return "ld" + solve_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        solve_string = ""
        
        # Check for invariance
        assert self.row1_invariant(target_col), "Invariant not true!"
        
        # Places the number in the target_col
        solve_string = self.solve_interior_tile(1, target_col)
        
        # Check that the invariance is not violated
        assert self.row1_invariant(target_col - 1)
        
        # Move the zero to the row above the solved tile column
        self.update_puzzle("ur")
        
        return solve_string + "ur"

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        
        # Check invariance at column 1 row 1
        assert self.row1_invariant(1) is True, "Invariant violated!"
        
        solve_string = ""
        # Move the zero tile to the upper left corner
        self.update_puzzle("lu")
        
        # Cycle through the moves until all the puzzle is solbed
        while self.row0_invariant(0) is False:
            solve_string += "rdlu"
            self.update_puzzle("rdlu")
        
        return "lu" + solve_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        
        solve_string = ""
        # First step is to move the zero into the last
        # row and column
        while self.current_position(0, 0)[1] != self._width - 1:
            self.update_puzzle("r")
            solve_string += "r"
        while self.current_position(0, 0)[0] != self._height - 1:
            self.update_puzzle("d")
            solve_string += "d"
        
        # Step 1: Solve last m - 2 rows of the puzzle
        for dummy_row in range(self._height - 1, 1, -1):
            
            # Solve every columns but the first column
            for dummy_col in range(self._width - 1, 0, -1):
                
                # Check the invariant of the current row and column
                assert self.lower_row_invariant(dummy_row, dummy_col) is True, "Invariant Violated at row = " + str(dummy_row) + "Invariant Violated at col = " + str(dummy_col)
                
                # Solve the puzzle
                solve_string += self.solve_interior_tile(dummy_row, dummy_col)
                
                # Check the invariant of the current row and the column to the left
                assert self.lower_row_invariant(dummy_row, dummy_col - 1) is True, "Invariant Violated at row = " + str(dummy_row) + "Invariant Violated at col = " + str(dummy_col - 1)
            
            # Solve the first column (col = 0)
            solve_string += self.solve_col0_tile(dummy_row)
            
            # Check the invariant of the next row and the last column
            assert self.lower_row_invariant(dummy_row - 1, self._width - 1)
            
        # Solve the n - 2 columns of the first two rows
        for dummy_col in range(self._width - 1, 1, -1):
            
            # Solve the second row and then the first row
            # Check for invariance at the second and then first row
            assert self.row1_invariant(dummy_col) is True, "Invariant Violated at row = 1, col = " + str(dummy_col)
            solve_string += self.solve_row1_tile(dummy_col)
            assert self.row0_invariant(dummy_col) is True, "Invariant Violated at row = 0, col = " + str(dummy_col)
            solve_string += self.solve_row0_tile(dummy_col)
            assert self.row1_invariant(dummy_col - 1) is True, "Invariant Violated at row = 1, col = " + str(dummy_col)
        
        # Solve the final 2 x 2
        assert self.row1_invariant(1) is True, "Invariant Violeted!"
        solve_string += self.solve_2x2()
        assert self.row0_invariant(0) is True, "Invariant Violated!"
        
        return solve_string

# This will generate random tiles
#def random_tile_gen(height, width):
#    """
#    Generates Random Tiles
#    """
#    
#    choice_of_tiles = []
#    for dummy_idx in range(height * width):
#        choice_of_tiles.append(dummy_idx)
#    
#    all_tiles = []
#    for dummy_row in range(height):
#        row_tiles = []
#        for dummy_col in range(width):
#            number = choice_of_tiles.pop(random.randrange(len(choice_of_tiles)))
#            row_tiles.append(number)
#        all_tiles.append(row_tiles)
#    return all_tiles

# Test case for random tile generator
# print random_tile_gen(4, 5)
    
# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(6, 6))
# puzzle = Puzzle(4, 4, [[1, 2, 3, 9],\
#                                          [4, 5, 6, 7],\
#                                          [8, 10, 12, 11],\
#                                          [0, 13, 14, 15]])

#k =  puzzle.reach_position(3, 0, (3, 0))
#k = list(k)
#k.pop(-1)
# print puzzle.solve_col0_tile(3)
#puzzle.update_puzzle(puzzle.reach_position(3, 0, (2, 2)))
# print puzzle
#m = puzzle.position_tile(3, 0, (2, 1), k)
#print m
#puzzle.update_puzzle(m)
#print puzzle
#puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print puzzle
#print puzzle.lower_row_invariant(2, 1)
#print puzzle.current_position(0, 0)
#print puzzle.solve_interior_tile(2, 1)
#print puzzle
#puzzle = Puzzle(3, 3, [[3, 0, 2], [1, 4, 5], [6, 7, 8]])
#print puzzle.row0_invariant(1)
# puzzle = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
# print puzzle
# print puzzle.solve_row1_tile(2)
# print puzzle
# puzzle = Puzzle(3, 3, [[4, 1, 5], [2, 3, 8], [6, 7, 0]])
# print puzzle
# puzzle.solve_puzzle()
# print puzzle
# puzzle = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
# puzzle.solve_puzzle()
# print puzzle
#puzzle = Puzzle(4, 5, [[5, 15, 3, 4, 9], [6, 10, 7, 8, 14], [2, 1, 11, 12, 13], [0, 16, 17, 18, 19]])
#print puzzle.solve_col0_tile(3)

#tile = random_tile_gen(4, 5)
#puzzle = Puzzle(4, 5, tile)
#print "Before:"
#print puzzle
#puzzle.solve_puzzle()
#print "After:"
#print puzzle

#tile = [[15, 7, 6, 1, 19], [3, 4, 13, 5, 14], [2, 10, 16, 18, 11], [9, 8, 17, 12, 0]]
#tile = [[14, 2, 9, 7, 11], [18, 6, 4, 12, 8], [5, 16, 1, 15, 3], [13, 19, 10, 17, 0]]
#count = 0
#trials = 50
#for dummy_idx in range(trials):
#    tile = random_tile_gen(4, 5)
#    puzzle = Puzzle(4, 5, tile)
#    while puzzle.current_position(0, 0)[1] != puzzle.get_width() - 1:
#        puzzle.update_puzzle("r")
#    while puzzle.current_position(0, 0)[0] != puzzle.get_height() - 1:
#        puzzle.update_puzzle("d")
#    print "Before:"
#    print puzzle
#    puzzle.solve_interior_tile(3, 4)
#    puzzle.solve_interior_tile(3, 3)
#    puzzle.solve_interior_tile(3, 2)
#    puzzle.solve_interior_tile(3, 1)
#    print puzzle
#    puzzle.solve_col0_tile(3)
#    print puzzle
#    puzzle.solve_interior_tile(2, 4)
#    puzzle.solve_interior_tile(2, 3)
#    puzzle.solve_interior_tile(2, 2)
#    puzzle.solve_interior_tile(2, 1)
#    print puzzle
#    puzzle.solve_col0_tile(2)
#    print puzzle
#    puzzle.solve_row1_tile(4)
#    puzzle.solve_row0_tile(4)
#    puzzle.solve_row1_tile(3)
#    puzzle.solve_row0_tile(3)
#    puzzle.solve_row1_tile(2)
#    puzzle.solve_row0_tile(2)
#    print puzzle
#    print "After:"
#    print puzzle
#    if puzzle.row1_invariant(1):
#        count += 1
#print count, "out of", trials, "test(s) succeed."
    #print "After:"
    #print puzzle
#puzzle.solve_row1_tile(4)
#print puzzle
#puzzle.solve_row0_tile(4)
#print puzzle
#puzzle.solve_row1_tile(3)
#print puzzle
#puzzle.solve_row0_tile(3)
#print puzzle
#puzzle.solve_row1_tile(2)
#print puzzle
#puzzle.solve_row0_tile(2)
#print puzzle
#puzzle.solve_2x2()
#print puzzle
