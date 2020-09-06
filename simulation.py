import time
import random
import maze_generator as mg
from maze import Maze
from agent import Agent
import trash_generator as tg
import sys

AGENTS_COLOR = '\033[91m'
METE_COLOR = '\033[34m'
LANDFILL_COLOR = '\033[92m'
CEND = '\033[0m'

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

def main():
    grid = mg.generate_maze(25, 25)
    coordinates = [] #Maze's viable coordinates
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == ' ':
                coordinates.append((r, c))
    
    n = int(input("enter number of agents: "))
    agents = []
    path = []
    for i in range(n):
        start = coordinates[random.randint(1, len(coordinates))]
        dest = start
        name = "Agent" + str(i + 1)
        new_agent = Agent(name, start, dest, path, grid, 100)
        agents.append(new_agent)
    print(len(agents))

    trashes = []
    while True:
        trash_prob = random.randint(1, 5)
        if trash_prob == 1:
            trash = tg.Trash(20, coordinates)
            tg.trash_notifier(trash, agents)
            trashes.append(trash)

        list_of_positions = []
        list_of_destinations = []
        for i in range(len(agents)):
            agents[i].check_position_and_notify(agents)
            list_of_positions.append(agents[i].next_position())  #salvo tutte le successive posizioni degli agenti
            list_of_destinations.append(agents[i].__dest__())
        
        draw_agents(grid, list_of_positions, list_of_destinations)
        time.sleep(0.5)


if __name__ == '__main__':
    main()