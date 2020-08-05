import random


def generate_maze(rows, cols):
    edges = [] #Lista di archi
    for i in range(rows):
        for j in range(cols):
            neighbors = generate_edges_by_coordinates(i, j, rows, cols)
            for neigh in neighbors:
                edges.append(neigh)
    random.shuffle(edges)
    #implementation randomized kruskhal algorithm
    edges_to_draw = []
    parent = {}
    for i in range(rows):
        for j in range(cols):
            edge = (i, j)
            parent[edge] = edge
    while len(edges) != 0:
        edge = random.choice(edges)
        edges.remove(edge)
        cell1 = find_parent(parent, edge[0])
        cell2 = find_parent(parent, edge[1])
        if cell1 != cell2:
            edges_to_draw.append(edge)
            parent[cell2] = cell1
    maze = [["X" for i in range(rows + rows - 1)] for i in range(cols + cols - 1)] #Labirinto vuoto
    for edge in edges_to_draw:
        cell1 = edge[0]
        cell2 = edge[1]
        meanRow = (cell1[0] + cell2[0])
        meanCol = cell1[1] + cell2[1]
        maze[cell1[0] * 2][cell1[1] * 2] = " "
        maze[cell2[0] * 2][cell2[1] * 2] = " "
        maze[meanRow][meanCol] = " "
    maze.insert(0, ["X" for i in range(cols + cols - 1)])
    maze.insert(2*rows, ["X" for i in range(cols + cols - 1)])
    for i in range(2*rows + 1):
        maze[i].insert(0, "X")
    for i in range(2*rows + 1):
        maze[i].insert(2*cols, "X")
    return maze

def print_maze(maze):
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows):
        for j in range(cols):
            print(maze[i][j], end = " ")
        print()

def generate_edges_by_coordinates(i, j, rows, cols):
    edges = []
    current = (i, j)
    neibright = (i, j + 1)
    neibBottom = (i + 1, j)
    if neibright[1] < cols:
        edges.append((current, neibright))
    if neibBottom[0] < rows:
        edges.append((current, neibBottom))
    return edges

def find_parent(parent, cell):
    while parent[cell] != cell:
        cell = parent[cell]
    return cell

#===============================TEST=======================================================
#maze = generate_maze(15,15)
#print_maze(maze)
