"""
Map and Weighted A* Pathfinding System
--------------------------------------

This module defines a 2D grid world and implements the weighted A* algorithm
for pathfinding. It includes grid generation, obstacle handling, terrain cost
evaluation, and path animation.
ANSI color codes are used for better console visualization.
"""

import random
import heapq  # we use heapq for the priority queue (min-heap)
import os
import time

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class Map:     
    """
    Simple 2D world for the robot.
    We will use a grid with:
      N = normal terrain (cost 1)
      O = obstacle (blocked)
      W = water (cost 5)
      H = hill  (cost 3)
      
    The map stores start and goal positions, generates random terrain,
    checks movements, and supports A* pathfinding.
    """
    
    # -->STEP 1: Initialize the map with rows and columns
    def __init__(self, rows: int, cols:int) -> None: # self refer to the object being created, in this case the l object.
        # number of rows and columns
        self.rows = rows
        self.cols = cols

        # this will the grid (list of lists)
        self.grid = []

        # set start and goal positions and start at top-left
        # This is a tuple with row and column index
        # tuple is immutable so cannot be changed and keep the same order of values,
        # and also can be used as a key in a dictionary or added to a set,and they  are hashable.
        self.start = (0, 0)
        # goal at bottom-right
        # In this case have 10 rows and 10 columns so it will be 9,9, as indexing starts from 0 not 1
        self.goal = (rows - 1, cols - 1) 
        
    #--> STEP 2: Fill the grid with normal terrain 'N'
    def fill_grid(self):
            """
            Fill the grid with only normal terrain 'N'.
            """
            # create with an empty list for the grid or reset the grid
            self.grid = [] 
            #iteration through each row index
            for x in range(self.rows):
                row_list = [] # create an empty list for each row
                
                # iteration through each column index
                for y in range(self.cols):
                    row_list.append('N') # append 'N' to the row list
                    
                self.grid.append(row_list) # append the row list to the grid
    
    #--> STEP 2b: Fill the grid with random terrain types
    def fill_random_grid(self, n_prob: int = 65, 
                         h_prob:int = 15, 
                         w_prob:int = 10,
                         o_prob:int = 10
                         )-> None:
            """
            Fill the grid with random terrain:
            - Most cells are 'N'- n_prob %
            - Some cells 'O' (obstacle) - o_prob %
            - Some cells 'W' (water) - w_prob %
            - Some cells 'H' (hill) - h_prob %
            - Check if start and goal are not obstacles so they are not blocked.
            - Automatically balance probabilities if they don’t add up to 100%
            """
            # check that the probability entered by user
            total_prob = n_prob + h_prob + w_prob + o_prob
            
            # if total not equal to 100, adjust automatically
            if total_prob != 100:
                print(f"Probabilities total {total_prob}%. Adjusting automatically to 100%.\n")
                
            # declare and calculate scaling factor
            # this makes sure the total adds up to 100
            
                scale = 100 / total_prob
                
            # adjust each probability   
                n_prob = int(n_prob * scale)
                h_prob = int(h_prob * scale)
                w_prob = int(w_prob * scale)
                o_prob = int(o_prob * scale) 
                
                
            self.grid = [] # create with an empty list for the grid or reset the grid
            
            # iteration through each row index
            for x in range(self.rows):
                row_list = [] # create an empty list for each row
                
                # iteration through each column index
                for y in range(self.cols):
                    # choose a random number between 1 and 100
                    rand_num = random.randint(1, 100)
                    
                    #decide terrain type based on random number
                    # check which range the random number falls into 
                    if rand_num <= n_prob:
                        terrain_type = 'N'
                    elif rand_num <= n_prob + h_prob:
                        terrain_type = 'H'
                    elif rand_num <= n_prob + h_prob + w_prob:
                        terrain_type = 'W'
                    else:
                        terrain_type = f"{RED}O{RESET}"
                    
                    row_list.append(terrain_type) # append the terrain type to the current row list
                    
                self.grid.append(row_list) # append the row list to the grid
                
            # make sure start and goal are not obstacles
            self.grid[self.start[0]][self.start[1]] = 'N'  # set start position to 'N'
            self.grid[self.goal[0]][self.goal[1]] = 'N'    # set goal position to 'N'
  
     
    #--> STEP 3: Print the grid to the console
    def print_grid(self) ->None:
            """
            Print the grid to the console.
            Start will be'S' and Goal will be 'G'.
            """
            # iterate through each row index
            for x in range (self.rows):
                # iterate through each column of the row index
                for y in range (self.cols):
                    
                    # check if the current position is starting position
                    #x is row index and y is column index
                    if (x, y) == self.start: 
                        print('S', end=' ')
                    # check if the current position is goal position
                    elif (x, y) == self.goal:
                        print('G', end=' ')
                    # else print what else is in the grid at that position, in this will be 'N'
                    #Then also 'O', 'W' or 'H'
                    else:
                        print(self.grid[x][y], end=' ')
                        
                print()  # new line after each row
                
    #--> STEP 3b( but step 10 for me): Animate the robot moving along a path         
    def animate_path(self, path, delay=0.3):
        """
        Animate robot movement step-by-step.
        Shows:
        🤖 = robot current position
        * = path already visited
        """
        visited = set()  # will store teh cell already travelled cells

        for step in path:
            x_pos, y_pos = step
            visited.add(step)  # add the current step to visited set(path)

            os.system('cls' if os.name == 'nt' else 'clear')  # clear console for animation effect
            
            print("\n====================")
            print(" Robot step:", step)
            print("====================")

            for x in range(self.rows):
                for y in range(self.cols):
                    if (x, y) == self.start:
                        print(f"{YELLOW}S{RESET}", end=" ")
                    elif (x, y) == self.goal:
                        print(f"{MAGENTA}G{RESET}", end=" ")
                    elif (x, y) == (x_pos, y_pos):
                        print("🤖", end=" ")
                    elif (x, y) in visited:
                        print(f"{GREEN}*{RESET}", end=" ")
                    else:
                        print(self.grid[x][y], end=" ")
                print()  # move to next line after each row

            time.sleep(delay)

      
      
    #--> STEP 4: Check if a position is inside the grid boundaries       
    def in_bounds(self, x:int, y:int) -> bool:
        """
        Check if the position (x, y) is inside the grid. 
        Return to boolean values, True if it is inside or False it is outside the grid.
        This is a helper function, don't need to call as object.method().
        """
        #check if x is less than 0 (above the top of the grid)
        if x < 0 or y < 0  or x >= self.rows or y >= self.cols:
            return False # outside the grid
        return True       
    
    #--> STEP 5: Check if a position is an obstacle or free    
    def check_obstacle(self, x:int, y:int) -> bool:
        """
        Check if the cell (x, y) is an obstacle or outside the grid.
        Return True if it is blocked (obstacle or outside).
        Return False if it is free (walkable terrain).
        This is also a helper function, don't need to call as object.method().
        
        """

        # First check if the position is outside the grid boundaries
        if not self.in_bounds(x, y):
            return True   # outside = which is also an obstacle for pathfinding logic

        # Now check if the terrain at this cell is an obstacle 'O'
        if 'O' in self.grid[x][y]:
            return True   # actual obstacle

        # Otherwise the cell is free to move into
        return False
    
    #--> STEP 6: Find valid moves from a position
    def find_moves(self, x:int, y:int) -> list:
        """
        This function finds valid moves from position (x, y), which is a cell in the grid and also check 
        for obstacles.
        Return a list of valid move positions (up, down, left, right).
        """

        moves = []  # list to return

        # UP → (x - 1, y) 
        if self.in_bounds(x - 1, y) and not self.check_obstacle(x - 1, y):
            moves.append((x - 1, y))

        # DOWN → (x + 1, y)
        if self.in_bounds(x + 1, y) and not self.check_obstacle(x + 1, y):
            moves.append((x + 1, y))

        # LEFT → (x, y - 1)
        if self.in_bounds(x, y - 1) and not self.check_obstacle(x, y - 1):
            moves.append((x, y - 1))

        # RIGHT → (x, y + 1)
        if self.in_bounds(x, y + 1) and not self.check_obstacle(x, y + 1):
            moves.append((x, y + 1))

        return moves
    
    
    #--> STEP 7: Calculate movement cost for a position
    def move_cost(self, x:int, y:int) -> int:
        """
        Return the movement cost of entering the cell (x, y).
        x: row index  y: column index
        Returns: int cost value -> 1 (normal), 3 (hill), 5 (water), inf (obstacle)
        """

        # get the terrain type at this position
        terrain = self.grid[x][y]

        # check the terrain and return the cost
        if terrain == 'N':
            return 1  
        elif terrain == 'H':
            return 3 
        elif terrain == 'W':
            return 5 
        else:
            # For 'O' (obstacle) or any unknown symbol
            # we return infinite cost, which means "do not go there".
            return float('inf')


    #--> STEP 8: Heuristic function for A* algorithm
    def heuristic(self, x:int, y:int) ->int: #this function takes in the current position (x, y) , this value wiill came from the A* algorithm
        """
        Heuristic function for A*.
        It estimates how far (x, y) is from the goal using
        Manhattan distance (only up, down, left, right moves).

        h(x, y) = |x - goal_x| + |y - goal_y|
        """

        # goal position (row, col)
        # self.goal is a tuple (goal_row, goal_col)
        goal_x, goal_y = self.goal

        # Manhattan distance = horizontal distance + vertical distance
        #abs is absolute value function, which gives the positive distance between two values
        distance = abs(x - goal_x) + abs(y - goal_y)

        # return the estimated distance, which is the heuristic value
        return distance

    #--> STEP 9: A* Algorithm implementation
    def a_star(self, weight:float= 1.0) -> list:
        """
        A* (A-star) Algorithm pathfinder.
        Finds the lowest-cost path from start to goal,
        using both real movement cost made so far plus estimated (heuristic) movement cost left.
         -g(n): actual cost from start to current cell n
         -h(n): estimated cost from n to goal (heuristic)
         -weight: heuristic weight. Values > 1 make it greedier (faster but less optimal).
         -The finl cost is : f(n) = g(n) + weight * h(n)
        Returns path as a list of (x, y) or None if no path is found.
        """

        # shorthand for start and goal positions which are tuples (row, col index)
        start = self.start
        goal = self.goal

        # Priority queue: stores (priority, position)
        # Here priority = cost_so_far + heuristic
        priority_queue = []
        heapq.heappush(priority_queue, (0, start))  # start has priority 0 at the beginning

        # Track cost from start to each cell (like in Dijkstra)
        cost_so_far = {start: 0}

        # Store parent cell for reconstructing path later
        parent = {start: None}

        while priority_queue:
            # Get the cell with the lowest total estimated cost (f = g + h)
            current_priority, (row, col) = heapq.heappop(priority_queue)

            # Skip if this is an outdated entry with higher cost
            if current_priority > cost_so_far[(row, col)] + self.heuristic(row, col):
                continue

            # Stop if we reached the goal
            if (row, col) == goal:
                break

            # Explore all 4 possible movements (up, down, left, right)
            for next_row, next_col in [
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1)
            ]:

                # Skip if cell is outside the grid or blocked
                if not self.in_bounds(next_row, next_col):
                    continue
                if self.check_obstacle(next_row, next_col):
                    continue

                # Step cost = cost from current cell + cost to move into next cell
                new_cost = cost_so_far[(row, col)] + self.move_cost(next_row, next_col)

                # If we haven't visited next cell OR found a cheaper path to it
                if (next_row, next_col) not in cost_so_far or new_cost < cost_so_far[(next_row, next_col)]:
                    cost_so_far[(next_row, next_col)] = new_cost
                    parent[(next_row, next_col)] = (row, col)

                    # f = g + h (actual cost so far + estimated cost to goal)
                    priority = new_cost + weight *self.heuristic(next_row, next_col)

                    # Add to heap with its priority
                    heapq.heappush(priority_queue, (priority, (next_row, next_col)))

        # If goal never reached
        if goal not in parent:
            print("\nNo valid path found — the goal is unreachable due to obstacles or blocked terrain.")
            return None

        # Rebuild the final path from goal back to start
        path = []
        current = goal
        #loop until we reach the start position, which parent is Non
        while current is not None:
            path.append(current)
            current = parent[current]

        path.reverse()
        return path
