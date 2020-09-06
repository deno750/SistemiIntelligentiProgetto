import random
import math
from maze import Maze

class Agent(object):
    def __init__(self, name, position, destination, path, grid, capacity):
        self.name = name
        self.position = position
        self.destination = destination
        self.path = path
        self.grid = grid
        self.capacity = capacity
        self.preferences_list = []
        self.my_pref = [0,0]  #primo elemento contiene preferenza, secondo contiene meta
        self.provis_dest = (0,0)  #le provvisorie per quando valuta le mete
        self.provis_path = []
        self.trashPreferences = {}
        self.colleaguesTrashPreferences = {}
        self.trashPath = {}
        
    def __pos__(self):
        return self.position
    def __dest__(self):
        return self.destination
    def __path__(self):
        return self.path
    def __cap__(self):
        return self.capacity
    def insert_dest(self, dest):
        self.destination = dest
        self.path = [] #resetto il path quando accetto una nuova destinazione
    def up_cap(self, cap):
        self.capacity = cap

    '''method that perform breadth search to find a path from actual position to destination'''
    def bfs(self, destination):
        #potrei anche dichiarare qui il maze e il goal
        maze = Maze(self.grid, self.position)
        goal = Maze(self.grid, destination)
        
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
        
        return new_path
        #if self.provis_dest != (0,0):
            #self.provis_path = new_path
        #else:
            #self.path = new_path
        
    
    '''this method return the next position of the agent in it's path'''
    def next_position(self):
        if len(self.path) == 0:
            return self.position
        position = self.path.pop(0)
        self.position = position
        return position

    def __calculate_preference(self, trash):
        path = self.bfs(trash.coordinates)
        distance = len(path)
        self.trashPath[trash] = path
        if distance == 0 or self.capacity == 0: 
            return -1
        preference = 1 / distance * 100 + (self.capacity - trash.quantity)
        return preference

    def trash_observer(self, trash):
        print(self.name + " received new trash location")
        preference = self.__calculate_preference(trash)
        self.trashPreferences[trash] = preference #choose good preference
        print(self.name + " has preference of " + str(preference))
        print(self.name + " has preferences: " + str(self.trashPreferences))
        self.colleaguesTrashPreferences[trash] = []

    #The agent receives a notification that the trash is picked, so it can remove this trash from it's queue
    def trash_picked_observer(self, trash):
        #remove the trash from agent's queue
        del self.trashPreferences[trash]
        del self.colleaguesTrashPreferences[trash]
        del self.trashPath[trash]
    
    #Notifies other agents that the trash is picked so they can remove the trash from their queue
    def trash_picked_notifier(self, trash, agents):
        #removes the trash from it's queue
        del self.trashPreferences[trash]
        del self.colleaguesTrashPreferences[trash]
        del self.trashPath[trash]
        #notifies other agents that the trash is picked
        for agent in agents:
            if agent == self:
                continue
            agent.trash_picked_observer(trash)

    def receive_colleagues_preferences(self, trash, pref):
        self.colleaguesTrashPreferences[trash].append(pref)
    
    def calculate_new_route(self, trash):
        agent_pref = self.trashPreferences[trash]
        colleagues_pref = max(self.colleaguesTrashPreferences[trash])
        if agent_pref > colleagues_pref:
            self.destination = trash.coordinates
            self.path = self.trashPath[trash]
            print(self.name + " is going to take trash at " + str(trash.coordinates))

    def check_position_and_notify(self, agents):
        if self.position == self.destination:
            for trash, v in self.trashPreferences.items():
                if trash.coordinates == self.position:
                    self.trash_picked_notifier(trash, agents)
                    break

