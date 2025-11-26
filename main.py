import random


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
            - Automatically
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
                    # 0-65: N -> 60% chance, 66-80: H -> 15% chance, 
                    # 81-90: W -> 15%, 91-100: O -> 10% chance
                    if rand_num <= n_prob:
                        terrain_type = 'N'
                    elif rand_num <= n_prob + h_prob:
                        terrain_type = 'H'
                    elif rand_num <= n_prob + h_prob + w_prob:
                        terrain_type = 'W'
                    else:
                        terrain_type = 'O'
                    
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
             
                

if __name__ == "__main__":
    print("Welcome to Arslan's Land." "\n")

    land1 = Map(10, 10)

    print("Map size:", land1.rows, "x", land1.cols)
    print("Start:", land1.start)
    print("Goal:", land1.goal, "\n")
    
# TESTING FILL GRID METHOD

    land1.fill_grid()

    land1.fill_random_grid(n_prob=50, o_prob=30)
    
    
    
    
    print("Legend: N=Normal, O=Obstacle, W=Water, H=Hill, S=Start, G=Goal\n")
    land1.print_grid()  