
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
        self.win = False

    def addCard(self,card):
        self.cards.append(card)
    
    def playCard(self,index):
        if index > len(self.cards) or index < 0:
            return -1
        else:
            return self.cards.pop(index)

# This manually checks which biutton is clicked
# boolean field is set when clicked, and server checks click for 
# valiation and processes meaning of clcik

class Click:
    def __init__(self):
        self.reset()

    def reset(self):
        self.joinWaitingRoom = False
        self.startGame = False
        self.drawCard = False
        self.menu = False
        self.instructions = False
        self.credits = False
        self.uno = False
        self.hand = [0] * 12 ## assume can't have over 12 cards

    def clicked(self, btnType):
        self.reset()
        if isinstance(btnType, tuple) and btnType[0] == 'hand':
            idx = btnType[1]
            self.hand[idx] = 1
        elif hasattr(self, btnType):
            setattr(self, btnType, True)