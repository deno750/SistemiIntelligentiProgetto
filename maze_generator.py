import random


def generate_maze(rows, cols):
    maze = [["X" for i in range(rows)] for i in range(cols)] #Labirinto vuoto
    edges = [] #Lista di archi
    for i in range(rows):
        for j in range(cols):
            neighbors = generate_edges_by_coordinates(i, j, rows, cols)
            for neigh in neighbors:
                edges.append(neigh)
    random.shuffle(edges)
    #implementation randomized kruskhal algorithm
    selected_cells = []
    num_of_cells = rows * cols
    edges_to_draw = []
    removed_edges = []
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
        else:
            removed_edges.append(edge)

    for edge in edges_to_draw:
        cell1 = edge[0]
        cell2 = edge[1]
        maze[cell1[0]][cell1[1]] = "*"
        maze[cell2[0]][cell2[1]] = "*"
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
maze = generate_maze(3,3)
print_maze(maze)
