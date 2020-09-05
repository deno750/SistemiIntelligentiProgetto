import random
from maze import Maze

class Agent(object):
    def __init__(self, position, destination, path, grid, capacity):
        self.position = position
        self.destination = destination
        self.path = path
        self.grid = grid
        self.capacity = capacity
        self.preferences_list = []
        self.my_pref = [0,0]  #primo elemento contiene preferenza, secondo contiene meta
        self.provis_dest = (0,0)  #le provvisorie per quando valuta le mete
        self.provis_path = []
        
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
    def bfs(self):
        #potrei anche dichiarare qui il maze e il goal
        maze = Maze(self.grid, self.position)
        if self.provis_dest != (0,0):
            goal = Maze(self.grid, self.provis_dest)
        else:
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
        
        if self.provis_dest != (0,0):
            self.provis_path = new_path
        else:
            self.path = new_path
        
    
    '''this method return the next position of the agent in it's path'''
    def next_position(self):
        if self.position == self.destination: #così quando raggiunge la destinazione torna indietro
            '''se arriva a casa si svuota e ripristina la capacità'''
            if self.destination == (1,1):
                self.capacity = 100
            else:
                self.capacity = self.capacity - 20
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
        
    '''metodo con il quale l'agente esprime il proprio grado di preferenza per raggiungere un certo punto'''
    def express_preference(self, meta):
        #regole: preferenza nulla se il carico è al completo e se sta già raggiungendo una meta
        if self.capacity > 0 and self.destination == (1,1):
            #self.my_pref[0] = random.randint(1, 100) #bisogna inserire una regola di scelta
            self.provis_dest = meta
            self.bfs()
            dist = len(self.provis_path)
            self.my_pref[0] = round((1/dist) * 100, 3)
        else:
            self.my_pref[0] = 0
        self.my_pref[1] = meta
        return self.my_pref 
    
    '''metodo che aggiorna la lista preferenze aggiungendo quelle dei compagni'''
    def receive(self, pref):
        self.preferences_list.append(pref)
        self.preferences_list.sort()
        self.preferences_list.reverse()  #la inverto solo per comodità
        
    '''metodo per decidere se aggiornare la propria meta'''
    def update_meta(self):
        #print("mia e massimo  ", self.my_pref[0], " ", self.preferences_list[0])
        check = False
        if self.my_pref[0] > 0 and self.my_pref[0] >= self.preferences_list[0]:
            self.destination = self.my_pref[1]
            #print("accettata")
            check = True
            #self.bfs()
            self.path = self.provis_path
        '''invia un segnale di conferma, cosicché gli altri agenti sappiano che questo 
           ha deciso di prendere a carico la meta'''
        return check
    
    '''metodo per il ripristino della lista preferenze, verrà eseguito quando viene raggiunto un accordo'''
    def reset(self):
        self.preferences_list = []
        self.provis_dest = (0,0)
        self.provis_path = []