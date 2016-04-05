"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        # Reset the obstacle grid to be empty
        poc_grid.Grid.clear(self)
        
        # Reset the zombie and human lists to be empty 
        self._human_list = list([])
        self._zombie_list = list([])
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
        
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
        
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for dummy_zombie in self._zombie_list:
            yield dummy_zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for dummy_human in self._human_list:
            yield dummy_human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # Initializes the visited and distance_field grids
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_width * self._grid_height\
                           for dummy_width in range(self._grid_width)] for\
                          dummy_height in range(self._grid_height)]
        boundary = poc_queue.Queue()
        
        # Fill the boundary with the chosen entity type
        if entity_type == ZOMBIE:
            for dummy_zombie in self.zombies():
                boundary.enqueue(dummy_zombie)
        elif entity_type == HUMAN:
            for dummy_human in self.humans():
                boundary.enqueue(dummy_human)
       
        # Set the boundary cell visited to be full and set the distance
        # field to be zero
        for dummy_boundary in boundary:
            visited.set_full(dummy_boundary[0], dummy_boundary[1])           
            distance_field[dummy_boundary[0]][dummy_boundary[1]] = 0
        
        # Implement the BFS Method, reiterate over the list until
        # there is nothing left
        while len(boundary) != 0:
            
            # Dequeue the boundary
            current_cell = boundary.dequeue()
            
            # Set the neighbor cells depending on the entity type
            neighbor_cells = visited.four_neighbors(current_cell[0], current_cell[1])
            
            # Reiterates over the list of neighbor cells
            for dummy_neighbor in neighbor_cells:
                # If the cell hasn't been visited set it as full and
                # set the distance field to be +1 depending on the distance
                # of the current cell also add the current neighbor to the
                # boundary list
                if visited.is_empty(dummy_neighbor[0], dummy_neighbor[1]) and self.is_empty(dummy_neighbor[0], dummy_neighbor[1]):
                    
                    # Set the cell to be visited
                    visited.set_full(dummy_neighbor[0], dummy_neighbor[1])
                    
                    # Set the distance field to be the current cell
                    # distance + 1
                    distance_field[dummy_neighbor[0]][dummy_neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    
                    # Enqueue the boundary
                    boundary.enqueue(dummy_neighbor)
        
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_grids = list([])
        for dummy_human in self.humans():
            
            # Calculate the eight neighbors for humans
            eight_neighbors = self.eight_neighbors(dummy_human[0], dummy_human[1])
            
            # Initialize the maximum distance as the distance from
            # on the current cell
            max_distance = zombie_distance_field[dummy_human[0]][dummy_human[1]]
            max_distance_cell = dummy_human
            for dummy_neighbors in eight_neighbors:
                distance = zombie_distance_field[dummy_neighbors[0]][dummy_neighbors[1]]
                if self.is_empty(dummy_neighbors[0], dummy_neighbors[1]):
                    if distance >= max_distance:
                        max_distance = distance
                        max_distance_cell = dummy_neighbors
            
            # Move the humans into the grid that will give the
            # maximum distance
            human_grids.append((max_distance_cell[0], max_distance_cell[1]))
        
        self._human_list = list(human_grids)
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_grids = list([])
        for dummy_zombies in self.zombies():
            
            # Calculates the four neighbors for zombies
            four_neighbors = self.four_neighbors(dummy_zombies[0], dummy_zombies[1])
        
            # Initialize the maximum distance as the distance from
            # on the current cell
            max_distance = human_distance_field[dummy_zombies[0]][dummy_zombies[1]]
            max_distance_cell = dummy_zombies
            for dummy_neighbors in four_neighbors:
                distance = human_distance_field[dummy_neighbors[0]][dummy_neighbors[1]]
                if self.is_empty(dummy_neighbors[0], dummy_neighbors[1]):
                    if distance <= max_distance:
                        max_distance = distance
                        max_distance_cell = dummy_neighbors
            
            # Move the humans into the grid that will give the
            # maximum distance
            zombie_grids.append((max_distance_cell[0], max_distance_cell[1]))
        
        self._zombie_list = list(zombie_grids)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
