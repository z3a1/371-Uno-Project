
class Card:
    def __init__(self,color = "red",cType = "number", val = 0):
        self.color = color
        self.type = cType
        self.val = val
    def __eq__(self, c):
        if not isinstance(c, Card):
            return False
        return (
            self.color == c.color and
            self.type == c.type and
            self.val == c.val)


# The turn variable is to be initally set to false
class Player:
    def __init__(self, cards, playerNum = 0):
        self.playerNum = playerNum
        self.cards = cards
        self.turn = False

    def addCard(self,card):
        self.cards.append(card)
    
    def playCard(self,index):
        if index > len(self.cards) or index < 0:
            return -1
        else:
            return self.cards.pop(index)
        