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



if __name__ == "__main__":
    print("This is Arslan's Land.")

    land1 = Map(10, 10)

    print("Map size:", land1.rows, "x", land1.cols)
    print("Start:", land1.start)
    print("Goal:", land1.goal)