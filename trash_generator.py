import random

class Trash:
    def __init__(self, quantity, viablePositions):
        self.quantity = quantity
        self.coordinates = generate_trash(viablePositions)
    
    def reduceQuantity(self, reduceBy):
        if reduceBy > self.quantity:
            self.quantity = 0
        else:
            self.quantity = self.quantity - reduceBy

def generate_trash(viablePositions):
    return viablePositions[random.randint(1, len(viablePositions) - 1)]

def trash_notifier(trash, agents):
    for agent in agents:
        agent.trash_observer(trash)
    for agent in agents:
        for colleague in agents:
            if agent == colleague:
                continue
            agent.receive_colleagues_preferences(trash, colleague.trashPreferences[trash])

    for agent in agents:
        agent.calculate_new_route(trash)

def trash_update_preferences(trashes, agents):
    for trash in trashes:
        trash_notifier(trash, agents)
    