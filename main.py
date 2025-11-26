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
    print("This is Arslan's Land.")

    land1 = Map(10, 10)

    print("Map size:", land1.rows, "x", land1.cols)
    print("Start:", land1.start)
    print("Goal:", land1.goal)
    
# TESTING FILL GRID METHOD

    land1.fill_grid()

    print("\n--- Printing Grid ---")
    land1.print_grid()