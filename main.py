import random
# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"


class Map:     
    """
    Simple 2D world for the robot.
    We will use a grid with:
      N = normal terrain
      O = obstacle
      W = water
      H = hill
    """
    
    # -->STEP 1: Initialize the map with rows and columns
    def __init__(self, rows, cols): # self refer to the object being created, in this case the l object.
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
    def fill_random_grid(self, n_prob = 65, h_prob = 15, w_prob = 10, o_prob = 10):
            """
            Fill the grid with random terrain:
            - Most cells are 'N'
            - Some cells 'O' (obstacle)
            - Some cells 'W' (water)
            - Some cells 'H' (hill)
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
    def print_grid(self):
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
                
    def animate_path(self, path, delay=0.3):
        """
        Animate robot movement step-by-step.
        Shows:
        🤖 = robot current position
        * = path already visited
        """
        import time

        visited = set()  # will store travelled cells

        for step in path:
            x_pos, y_pos = step
            visited.add(step)  # mark current position as visited

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
    def in_bounds(self, x, y):
        """
        Check if the position (x, y) is inside the grid. 
        Return True if it is inside or False it is outside.
        This is a helper function, don't need to call as object.method().
        """
        #checking the boundaries
        #check if x is less than 0 (above the top of the grid)
        if x < 0:
            return False
        #check if y is less than 0 (left of the grid)
        if y < 0:
            return False
        #check if x is greater than or equal to the last row index(below the bottom of the grid)
        if x >= self.rows:
            return False
        #check if y is greater than or equal to the last column index(right of the grid)
        if y >= self.cols:
            return False
        # if all checks passed, it is inside the grid
        return True       
    
    #--> STEP 5: Check if a position is an obstacle or free    
    def check_obstacle(self, x, y):
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
    def find_moves(self, x, y):
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
    def move_cost(self, x, y):
        """
        Return the movement cost of entering the cell (x, y).
        Costs:
            N = 1 (normal terrain)
            H = 3 (hill)
            W = 5 (water)
            O = obstacle (very high cost so robot never enters)
        """

        # get the terrain type at this position
        terrain = self.grid[x][y]

        # check the terrain and return the cost
        if terrain == 'N':
            return 1  # normal ground, easy to walk, cost 1
        elif terrain == 'H':
            return 3  # hills are harder to climb, cost 3
        elif terrain == 'W':
            return 5  # water is very slow, cost 5
        else:
            # For 'O' (obstacle) or any unknown symbol
            # we return infinite cost, which means "do not go here".
            return float('inf')




    # def bfs(self):
    #     """
    #     BFS(breadth first search) algorithm pathfinder.
    #     Finds a path from start to goal.
    #     Returns path as a list of (x, y) or None if no path.
    #     """
        
    #     # Import deque for efficient queue operations, deque allows O(1) time complexity for appending and popping from both ends
    #     # It use FIFO (first in first out) principle. BFS, allows fast .append() (add to end) and .popleft() (remove from front)
    #     # from collections import deque
    #     # Colletion is a built-in module in Python (built in libary) that containn special data structures like deque, that are more efficient than standard lists or dictionary for certain operations.
    #     from collections import deque
        
    #     queue = deque() # initialize empty queue
    #     queue.append(self.start) # add starting position to the queue (0,0)

    #     # this is a dictionary, store where we came from for each position
    #     # key = position (x, y), value = previous position (x, y)
    #     parent = {self.start: None}   
        
    #     while queue: # this loop will run until the queue is empty
            
    #         row, col = queue.popleft()

    #         # goal reached → stop early
    #         if (row, col) == self.goal:
    #             break

    #         # check all four directions
    #         for next_row, next_col in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                
    #             # skip if outside grid OR obstacle
    #             if not self.in_bounds(next_row, next_col):
    #                 continue
    #             if self.check_obstacle(next_row, next_col):
    #                 continue

    #             # skip if already visited
    #             if (next_row, next_col) in parent:
    #                 continue

    #             # mark where we came from & add to queue
    #             child = (next_row, next_col)
    #             parent_cell = (row, col)
    #             parent[child] = parent_cell

    #             queue.append(child)

    #     # if we never reached goal
    #     if self.goal not in parent:
    #         return None

    #     # rebuild path from goal → back to start
    #     path = []
    #     current = self.goal
    #     while current is not None:
    #         path.append(current)
    #         current = parent[current]

    #     path.reverse()
    #     return path


    # def dijkstra(self):
    #     """
    #     Dijkstra's Algorithm pathfinder.
    #     Finds the lowest-cost path from start to goal, considering terrain costs.
    #     Returns path as a list of (x, y) or None if no path.
    #     """
    #     # heapq module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm (min-heap).
    #     import heapq  

    #     # shorthand for start and goal positions which tuple with (row, col index)
    #     start = self.start
    #     goal = self.goal

    #     # Priority queue: stores (cost, position)
    #     # crete an empty list for the heap
    #     #by default, we start with cost 0 at the starting position
    #     priority_queue = []
        
    #     heapq.heappush(priority_queue, (0, start)) #cost and position

    #     # Cost from start to each cell so far
    #     #it also help me to track visited cells with their lowest cost found, and update if a cheaper path is found
    #     # key in the dictionary is position (row, col), value is cost from start to that position
    #     cost_so_far = {start: 0}

    #     # Store where we came from, which will be used to rebuild the path
    #     parent = {start: None}


    #     # loop until there are no more cells to process
    #     while priority_queue:
    #         # Get cell with lowest cost so far
    #         current_cost, (row, col) = heapq.heappop(priority_queue)

    #         # Skip this cell if we already found a cheaper way to reach it
    #         if current_cost > cost_so_far[(row, col)]:
    #             continue

    #         # Stop if goal is reached
    #         if (row, col) == goal:
    #             break

    #         # Check all 4 possible moves
    #         for next_row, next_col in [
    #             (row - 1, col), (row + 1, col),
    #             (row, col - 1), (row, col + 1)
    #         ]:

    #             # Skip invalid cells
    #             if not self.in_bounds(next_row, next_col):
    #                 continue
    #             if self.check_obstacle(next_row, next_col):
    #                 continue

    #             # Calculate new cost for this move, remeber costs not
    #             # I am referring to value  of yhe key in the dictionary (example position(0,0) values 0)+ the cost to enter the next cell
    #             # move cost is using  as refernce the coordinate  of the next cell
    #             new_cost = cost_so_far[(row, col)] + self.move_cost(next_row, next_col)

    #             # if this path doesn't exist yet OR is ezxist but is cheaper than previous cost
    #             if (next_row, next_col) not in cost_so_far or new_cost < cost_so_far[(next_row, next_col)]:
    #                 cost_so_far[(next_row, next_col)] = new_cost  # update or save the cost 
    #                 parent[(next_row, next_col)] = (row, col) # record where we came from, first part is child, second part is parent

    #                 # Add to heap with priority based on new cost
    #                 heapq.heappush(priority_queue, (new_cost, (next_row, next_col)))

    #     # If goal never reached
    #     if goal not in parent:
    #         print("\nNo valid path found — the goal is unreachable due to obstacles or blocked terrain.")
    #         return None

    #     # Rebuild path
    #     path = []
    #     current = goal
    #     #loop until we reach the start position, which parent is None
    #     while current is not None:
    #         path.append(current)
    #         current = parent[current]
    #     path.reverse()
    #     return path

    #--> STEP 8: Heuristic function for A* algorithm
    def heuristic(self, x, y): #this function takes in the current position (x, y) , this value wiill came from the A* algorithm
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
    def a_star(self):
        """
        A* (A-star) Algorithm pathfinder.
        Finds the lowest-cost path from start to goal,
        using both real movement cost and estimated (heuristic) cost.
        Returns path as a list of (x, y) or None if no path is found.
        """

        import heapq  # we use heapq for the priority queue (min-heap)

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
                    priority = new_cost + self.heuristic(next_row, next_col)

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





 

    # # test BFS
    # print("\nTest BFS\n")
    # path = land1.bfs()

    # if path is None:
    #     print("No path found from start to goal.")
    # else:
    #     print("Path found:")
    #     print(path)
    #     print("Path length:", len(path))

    # path = land1.dijkstra()
    # if path:
    #     print("\nPath found:")
    #     print(path)
    #     print("\nPath length:", len(path))
    #     print("\nTotal movement cost:", sum(land1.move_cost(x, y) for x, y in path))
    
if __name__ == "__main__":
    print("Welcome to Arslan's Land.\n")

    land1 = Map(10, 10)

    # Generate map
    land1.fill_grid()
    land1.fill_random_grid(n_prob=60, h_prob=20, w_prob=10, o_prob=20)

    print("Legend: N=Normal, O=Obstacle, W=Water, H=Hill, S=Start, G=Goal\n")

    print("Generated Map:\n")
    land1.print_grid()

    print("\nRunning A* Algorithm...\n")
    path = land1.a_star()

    if path:
        print("\nRobot movement animation:\n")
        land1.animate_path(path, delay=1.0)

        # =============================
        # FINAL SUMMARY AFTER ANIMATION
        # =============================
        print("\n===== FINAL RESULTS =====\n")
        print(f"Map size used: {land1.rows} x {land1.cols}")
        print(f"Start: {land1.start}")
        print(f"Goal: {land1.goal}\n")

        print("Tested A* Algorithm\n")
        print("Path found:")
        print(path)

        print(f"\nPath length: {len(path)}")
        print(f"Total movement cost: {sum(land1.move_cost(x, y) for x, y in path)}")

    else:
        print("\nNo path could be found — goal is unreachable due to obstacles.")
