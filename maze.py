class Maze(object):
    """A pathfinding problem."""

    def __init__(self, grid, location):
        """Instances differ by their current agent locations."""
        self.grid = grid
        self.location = location

    def __hash__(self):
        return hash(self.location)

    def __eq__(self, maze):
        return self.location == maze.location

    def __ne__(self, maze):
        return self.location != maze.location

    '''def display(self):
        """Print the maze, marking the current agent location."""
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if (r, c) == self.location:
                    print('*', end=" ")
                else:
                    print(self.grid[r][c], end=" ")
            print("")
        print(" ")'''

    def moves(self):
        """Return a list of possible moves given the current agent location."""
        # YOU FILL THIS IN
        moves = []
        loc = self.location
        loc
        #scorro tutte le posizioni, se disponibili le aggiungo
        if self.grid[loc[0]][loc[1]-1] == " ":
            moves.append((loc[0],loc[1]-1))
            
        if self.grid[loc[0]-1][loc[1]] == " ":
            moves.append((loc[0]-1,loc[1]))
            
        if self.grid[loc[0]][loc[1]+1] == " ":
            moves.append((loc[0],loc[1]+1))
            
        if self.grid[loc[0]+1][loc[1]] == " ":
            moves.append((loc[0]+1,loc[1]))
        return moves

    def neighbor(self, move):
        """Return another Maze instance with a move made."""
        # YOU FILL THIS IN
        newMaze = Maze(self.grid, move)
        return newMaze