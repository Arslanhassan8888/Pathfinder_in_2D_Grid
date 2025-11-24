class Map:     
    """
    Simple 2D world for the robot.
    We will use a grid with:
      N = normal terrain
      O = obstacle
      W = water
      H = hill
    """
    def __init__(self, rows, cols): # self refere to the object being created, in this case the l object.
        # number of rows and columns
        self.rows = rows
        self.cols = cols

        # this will the grid (list of lists)
        self.grid = []

        # set start and goal positions and start at top-left
        # This is a tuple with row and column index
        # tuple is immutable so cannot be changed and keep the same order of values
        self.start = (0, 0)
        # goal at bottom-right
        # In this case have 10 rows and 10 columns so it will be 9,9, as indexing starts from 0 not 1
        self.goal = (rows - 1, cols - 1) 

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
                
                
                

if __name__ == "__main__":
    print("This is Arslan's Land.")

    land1 = Map(10, 10)

    print("Map size:", land1.rows, "x", land1.cols)
    print("Start:", land1.start)
    print("Goal:", land1.goal)
    
# TESTING FILL GRID METHOD

    land1.fill_grid()

    print("\nGrid filled with 'N':")
    for row in land1.grid:
        print(row)