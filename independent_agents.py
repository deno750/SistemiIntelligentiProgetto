import time
import random


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


class Agent(object):
    def __init__(self, position, destination, path, grid):
        self.position = position
        self.destination = destination
        self.path = path
        self.grid = grid
        
    def __pos__(self):
        return self.position
    def __dest__(self):
        return self.destination
    def __path__(self):
        return self.path
    def insert_dest(self, dest):
        self.destination = dest
        self.path = [] #resetto il path quando accetto una nuova destinazione
    
    '''method that perform breadth search to find a path from actual position to destination'''
    def bfs(self):
        #potrei anche dichiarare qui il maze e il goal
        maze = Maze(self.grid, self.position)
        goal = Maze(self.grid, self.destination)
        
        frontiera = []
        visitati = []
        percorso = {}
        #metto l'inizio nella frontiera
        frontiera.append(maze.location)
        while frontiera: #cioè finché non è vuota
            elem = frontiera.pop(0) #rimuovo il primo elemento
            parent = Maze(maze.grid, elem)
            visitati.append(parent.location)
            
            child = parent.moves()
            rimuovere = False
            for c in child:
                for visit in visitati: #verifico che questo elemento non sia già stato visitato
                    if c == visit:
                        rimuovere = True
                if not rimuovere:
                    frontiera.append(c) #se non è già stato visitato lo aggiungo alla frontiera
                    percorso[c] = elem #aggiungo il figlio con il suo genitore al dizionario
                else:
                    rimuovere = False
            #if c==(19,18): #se voglio andare in qualunque direzione non possono esserci uscite
             #   frontiera = []
        
        new_path = []
        primo = visitati[0]
        figlio = goal.location
        #partendo dalla fine recupero i genitori inserendoli nel new_path
        genitore = percorso[figlio]
        while True:
            new_path.append(genitore)
            if genitore == primo:
                break #se arrivo al punto d?origine interrompo
            figlio = genitore
            genitore = percorso[figlio]
        
        new_path.reverse()
        new_path.append(goal.location)
        
        self.path = new_path
    
    '''this method return the next position of the agent in it's path'''
    def next_position(self):
        if self.position == (1,1) and self.destination == (1,1): #così quando raggiunge la fine non sparisce ma resta fermo
            return self.position
        if self.position == self.destination: #così quando raggiunge la destinazione torna indietro
            '''qui dovrei ricalcolare il percorso per tornare a casa'''
            self.destination = (1,1)
            self.bfs()
            return self.position
        for i in range(len(self.path)-1):     #cerco posizione attuale nel path
            if self.path[i] == self.position:
                #update actual position
                next_pos = self.path[i+1]
                self.position = next_pos
                return next_pos
    



def meta_generation(grid):
    '''generate random positions until one is good'''
    while True:
        x = random.randint(1,21)
        y = random.randint(1,23)
        if grid[y][x] == ' ' and ( x!=1 or y!=1):  #la griglia è messa al contrario, l'inizio non è considerato valido
            break
    
    return (y,x)

def draw_agents(grid, lista):
    """Print the maze, marking the current agent location."""
    #for j in range(len(lista)):
    """Print the maze, marking the current agent location."""
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if (r, c) == lista[0] or (r, c) == lista[1]: # RISOLVERE STA COSA!!!!
                print('*', end=" ")
            else:
                print(grid[r][c], end=" ")
        print("")
    print(" ")

def main():
    '''The grid are created at the start of the program and it remains the same for the entire execution'''
    grid = ["XXXXXXXXXXXXXXXXXXXXXXX",  #dimensioni: (23,21)
            "X     XX              X",
            "X XXXXXX XXXX XXXX XXXX",
            "X XXXXXX XXXX XXXX XXXX",
            "X        XX     XX    X",
            "X XXXX XXXXXXXX XX XX X",
            "X XXXX XXXXXXXX XX XX X",
            "X XX   XX             X",
            "X XXXX XXXX XX XX XXX X",
            "X XXXX XXXX XX XX XXX X",
            "X XXXX   XX XX XX     X",
            "X    XXX          XXXXX",
            "X    XXX XXXXXXXX XXXXX",
            "X XXX    XXXXXXXX     X",
            "X    XXX XX XX    XXXXX",
            "XXXX XXX XX XX XXXXXXXX",
            "X     XX XX XX XXX    X",
            "XXXXX    XX XX XX  XXXX",
            "XXXXX XX XX    XX  XXXX",
            "X     XX XXXX XXX     X",
            "X XX     XX   XXX   XXX",
            "X XX XXXXXX XX XXXX XXX",
            "X XX XXXXXX XX XXXX   X",
            "X XX                XXX",
            "XXXXXXXXXXXXXXXXXXXXXXX"]
    
    print("PROVE")
    '''start = (1,1)
    dest = (1,1)
    path = []
    agent1 = Agent(start, dest, path, grid)
    agent2 = Agent(start, dest, path, grid)
    
    print("prima tappa")
    meta1 = meta_generation(grid)  #creo nuova destinazione
    print(meta1)
    agent1.insert_dest(meta1)      #la passo all'agente
    agent1.bfs()                  #perché possa calcolare il percorso
    #print(agent1.__path__())
    
    meta2 = meta_generation(grid)  #creo nuova destinazione
    print(meta2)
    agent2.insert_dest(meta2)      #la passo all'agente
    agent2.bfs()                  #perché possa calcolare il percorso
    #print(agent2.__path__())'''
    
    '''creo lista di agenti'''
    n = 2
    list_of_agents = []
    start = (1,1)
    dest = (1,1)
    path = []
    for i in range(n):
        new_agent = Agent(start, dest, path, grid)
        list_of_agents.append(new_agent)
    print(len(list_of_agents))
    #prova:
    '''meta1 = meta_generation(grid)
    list_of_agents[0].insert_dest(meta1) 
    list_of_agents[0].bfs()
    meta2 = meta_generation(grid)
    list_of_agents[1].insert_dest(meta2) 
    list_of_agents[1].bfs()'''
    
    print("inizio while")
    while True:
        prob_meta = random.randint(1,5)    # 20% di probabilità di generare una nuova meta
        meta = ()
        if prob_meta == 1:
            meta = meta_generation(grid)
        print(meta)
        '''cerco fra gli agenti uno che possa accettare la nuova meta'''
        for i in range(len(list_of_agents)):
            if list_of_agents[i].__dest__() == (1,1) and meta != ():
                list_of_agents[i].insert_dest(meta)
                print("meta accettata")
                list_of_agents[i].bfs()
                time.sleep(1)
                break   #solo uno accetta una certa meta
        
        
        '''calcolo percorso agente'''
        list_of_positions = []
        for i in range(len(list_of_agents)):
            list_of_positions.append(list_of_agents[i].next_position())  #salvo tutte le successive posizioni degli agenti
        draw_agents(grid, list_of_positions)
        time.sleep(0.3)
        
        '''ora devo fare che la meta cambia sempre e viene presa da un agente
           solo dopo che ha raggiunto il precedente obbiettivo'''
    





if __name__ == '__main__':
    main()