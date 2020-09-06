import time
import random
import maze_generator as mg
from maze import Maze
from agent import Agent
import sys

AGENTS_COLOR = '\033[91m'
METE_COLOR = '\033[34m'
LANDFILL_COLOR = '\033[92m'
CEND = '\033[0m'

def meta_generation(coordinates):
    index = random.randint(1, len(coordinates))
    return coordinates[index]

'''metodo che visualizza le posizioni attuali degli agenti'''
def draw_agents(grid, positions, destinations):
    """Print the maze, marking the current agent location."""
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            for j in range(len(positions)):
                if (r, c) == (1, 1): #Draws the LandFill position
                    print(LANDFILL_COLOR + 'T' + CEND, end= " ")
                    break
                elif (r, c) == positions[j]:
                    print(AGENTS_COLOR + '*' + CEND, end=" ")
                    break
                elif (r,c) == destinations[j]:
                    print(METE_COLOR + 'O' + CEND, end=" ")
                    break
                if j == len(positions)-1: #significa che sono arrivato in fine e non ho trovato agenti in quella posizione
                    print(grid[r][c], end=" ")
        print("")
    print(" ")
    

'''====================== METODO CHIAVE ======================='''

'''metodo per gestire le comunicazioni fra gli agenti affinché decidano chi mandare alla meta successiva'''
def choose_new_meta(agents, mete):   #prende lista di agenti e coda di mete
    if len(mete) == 0:    #soprattutto alle prime iterazioni può essere vuota
        return agents
    next_meta = mete[0]
    #QUELLO CHE FACEVA PRIMA
    '''for i in range(len(agents)):
            if agents[i].__dest__() == (1,1) and agents[i].__cap__() > 0:
                agents[i].insert_dest(next_meta)
                mete.pop(0)
                print("accettata:", end=" ")
                print(next_meta)
                
                agents[i].bfs()  #l'agente prescelto calcola immediatamente il suo percorso
                time.sleep(1)
                break   #solo uno accetta una certa meta'''
    
    #QUELLO CHE FA ORA
    '''ogni agente esprime un grado di preferenza pr la meta in questione e lo comunica agli altri'''
    print("preferences")
    for i in range(len(agents)):
        pref = agents[i].express_preference(next_meta)
        print(pref)
        for j in range(len(agents)):
            if j != i:   #devo evitare di inviare la preferenza all'agente stesso
                agents[j].receive(pref[0])
    '''terminate le comunicazioni delle preferenze, gli agenti valutano se modificare la propria meta'''
    for i in range(len(agents)):
        confirmed = agents[i].update_meta()
        if confirmed:
            mete.pop(0)
            #time.sleep(1)
            #pause()
            '''comunico a tutti di resettare le proprie liste perché la scelta è stata fatta'''
            for j in range(len(agents)):
                agents[j].reset()
            break   #interrompere il ciclo è come comunicare che la scelta è già stata fatta (?)
    return agents

'''============================================================'''

#supporto, solo per visualizzare il funzionamento lentamente
def pause():
    while True:
        n = str(input("press e to exit: "))
        if n == "e":
            sys.exit()
        else:
            break
    
    time.sleep(1)

def main():
    '''The grid are created at the start of the program and it remains the same for the entire execution'''
    grid = mg.generate_maze(25,25)
    coordinates = [] #Maze's viable coordinates
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == ' ':
                coordinates.append((r, c))
    
    
    '''creo lista di agenti'''
    n = int(input("enter number of agents: "))
    list_of_agents = []
    #start = coordinates[random.randint(1, len(coordinates))]
    #start = (1,1)
    #dest = (1,1)
    path = []
    for i in range(n):
        start = coordinates[random.randint(1, len(coordinates))]
        dest = start
        new_agent = Agent(start, dest, path, grid, 100)
        list_of_agents.append(new_agent)
    print(len(list_of_agents))
    
    '''LOOP INFINITO'''
    meta_queue = []
    while True:
        prob_meta = random.randint(1,5)    # 10% di probabilità di generare una nuova meta
        meta = ()
        if prob_meta == 1:
            meta = meta_generation(coordinates)
            meta_queue.append(meta)
        print(meta_queue)
        print("generata:", end=" ")
        print(meta)
        
        '''cerco fra gli agenti uno che possa accettare la nuova meta'''
        list_of_agents = choose_new_meta(list_of_agents, meta_queue)
        
        print("agent's capacities:")
        '''faccio muovere tutti gli agenti di un passo'''
        list_of_positions = []
        list_of_destinations = []
        for i in range(len(list_of_agents)):
            list_of_positions.append(list_of_agents[i].next_position())  #salvo tutte le successive posizioni degli agenti
            list_of_destinations.append(list_of_agents[i].__dest__())
            print(list_of_agents[i].__cap__())
        draw_agents(grid, list_of_positions, list_of_destinations)
        time.sleep(0.3)
    





if __name__ == '__main__':
    main()