"""
This module plays the full 2048 game
"""

# Import the working merge code from previous project
# import user41_rePnzXlncg_6 as merge

# Import the test suite and random library
import poc_2048_gui
import random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing the tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

# Helper function
def merge(line):
    """
    This function merges a single row or column in 2048.
    Takes a list of numbers, sorts them, and merges them
    as according to 2048 rules and returns the list of
    merged numbers the same length as the input line.
    """

    # The sorting step
    # Creates a list of zeros the same length as line
    sorted_list = []
    for dummy_line in line:
        sorted_list.append(0)
        
    # Sorts non-zero elements into the a new intermediate
    # list
    idx = 0
    for dummy_line in line:
        if not dummy_line == 0:
            sorted_list[idx] = dummy_line
            idx += 1
    
    # The merging step
    # Creates a list of zeroes to the new_list the same
    # length as the given line. This will be the list that
    # stores the merged numbers
    new_list = []
    for dummy_line in sorted_list:
        new_list.append(0)
    
    # Merges the sorted non-zero elements to the list
    idx = 0
    for dummy_line in sorted_list:
        if not dummy_line == 0:
            
            # Store the element into the list if the
            # current element of the list is zero
            if new_list[idx] == 0:
                new_list[idx] = dummy_line
            
            # If an element in the sorted list is equal to 
            # the one stored on the list merge them 
            # together and assigns new spot to store the
            # next element by incrementing the index
            elif new_list[idx] == dummy_line:
                new_list[idx] = 2 * dummy_line
                idx += 1
                
            # If sorted element is not equal to the one in
            # the stored list, store elements on the next
            # list
            else:
                idx += 1
                new_list[idx] = dummy_line
                
    return new_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._tiles = [[0] * self._grid_width for dummy_height in range(self._grid_height)]
        
        # Pre-compute the list of initial tiles for each
        # directions
        self._initial_tiles_up = [[0, col] for col in range(self._grid_width)]
        self._initial_tiles_down = [[self._grid_height-1, col] for col in range(self._grid_width)]
        self._initial_tiles_left = [[row, 0] for row in range(self._grid_height)]
        self._initial_tiles_right = [[row, self._grid_width-1] for row in range(self._grid_height)]
        
        # Stores the initial tiles in a dictionary
        self._tiles_dictionary = {UP: self._initial_tiles_up,
                                DOWN: self._initial_tiles_down,
                                LEFT: self._initial_tiles_left,
                                RIGHT: self._initial_tiles_right}
        
    def __str__(self):
        """
        Return a string representation of the tile for
        debugging arranged by rows.
        """
        tile_string = ''
        for dummy_tile_row in self._tiles:
            tile_string = str(dummy_tile_row) + "\n"
        return tile_string
    
    def tile_initial_string(self):
        """
        Return strings of initial tiles. For testing and
        debugging purposes only.
        """
        
        # Combines the list of initial tiles together
        combined_tiles = [self._initial_tiles_up,
                          self._initial_tiles_down,
                          self._initial_tiles_left,
                          self._initial_tiles_right]
        directionals = ['up', 'down', 'left', 'right']
        
        # Stores the string for use in return
        indices_string = ''
        dummy_directional_index = 0
        for tiles_string_dummy in combined_tiles:
            indices_string += ('For ' + str(directionals[dummy_directional_index]) + ': ')
            indices_string += (str(tiles_string_dummy) + '\n')
            dummy_directional_index += 1
        return indices_string
    
    def reset(self):
        """
        Reset the game with a new tile and two randomly
        placed tiles.
        """
        self._tiles = [[0] * self._grid_width for dummy_height in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
        
    def new_tile(self):
        """
        Randomly spawn a new tile in an empty tile.
        """
        
        # Searches the entire column for every empty grid
        # and the stores the location of at which row and 
        # column to a list
        empty_tile_coordinates = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if (self._tiles[row][col] == 0):
                    empty_tile_coordinates.append([row, col])
        
        # Choses the coordinates of empty tiles randomly
        # from the list of empty tiles obtained previously
        empty_tile_length = len(empty_tile_coordinates)
        empty_tile_idx = random.randrange(empty_tile_length)
        [row, col] = empty_tile_coordinates[empty_tile_idx]
        
        # Stores a either 2 or 4 in the randomly chosen tile
        # Stores 2 90% of the time and 4 10% of the time
        if (random.randrange(0, 10) == 0):
            self.set_tile(row, col, 4)
        else:
            self.set_tile(row, col, 2)
        
    def get_grid_height(self):
        """
        Returns the height of the grid.
        """
        return self._grid_height
    
    def get_grid_width(self):
        """
        Returns the width of the grid.
        """
        return self._grid_width
    
    def move(self, direction):
        """
        Move all tiles in a given direction and add new
        tiles if any tiles moved.
        """
        
        # Calls the precomputed list of initial tiles
        # to be used in merging
        start_cell_array = self._tiles_dictionary[direction]
        direct = OFFSETS[direction]
        previous_tile_list = [list(tile_row) for tile_row in self._tiles]
        
        # If traversing in either vertical direction
        # Set the limits of steps to be the height
        # If horizontal direction set the limit to be
        # the width
        if (direction == UP) or (direction == DOWN):
            num_steps = self._grid_height
        else:
            num_steps = self._grid_width
        
        # Scans the tiles from the initial tiles
        # gets the value from the tiles
        for start_cell in start_cell_array:
            merge_list = []
            for step in range(num_steps):
                row = start_cell[0] + step * direct[0]
                col = start_cell[1] + step * direct[1]
                merge_list.append(self.get_tile(row, col))
            
            # Rewrites the tiles with the merged list one
            for step, value in list(enumerate(merge(merge_list))):
                row = start_cell[0] + step * direct[0]
                col = start_cell[1] + step * direct[1]
                self.set_tile(row, col, value)
                
        if not previous_tile_list == self._tiles:
            self.new_tile()
    
    def set_tile(self, row, col, value):
        """
        Set the tile at a certain row and column position
        to be of a given value.
        """
        self._tiles[row][col] = value
    
    def get_tile(self, row, col):
        """
        Return the value of the tile at a certain position
        """
        return self._tiles[row][col]

# Testing for merge module

print merge([2, 4, 2, 2])

# Brings the GUI for 2048 Game

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
