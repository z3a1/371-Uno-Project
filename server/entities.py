
class Card:
    def __init__(self,color = "r",cType = "number", val = 0):
        self.color = color
        self.type = cType
        self. val = val


# The turn variable is to be initally set to false
class Player:
    def __init__(self, cards):
        self.cards = cards
        self.turn = False

    def addCard
    
    def playCard(self,index):
        if index > len(self.cards) or index < 0:
            return -1
        else:
            return self.cards.pop(index)
        