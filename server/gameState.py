from entities import * 
from random import randint,seed

class GameState:
    def __init__(self, numOfPlayers = 0):
        self.numOfPlayers = numOfPlayers
        self.players = []
        self.colors = ['red','green','blue','yellow']
        self.turns = 1
        self.currTurn = 0
        self.isGameOver = False
        self.seed = seed()
        self.startingMaxCards, self.lowestCard, self.highestCard, self.lowestColorIdx, self.highestColorIdx = 8, 0, 9, 1, 3

    def initializeDeck(self) -> list:
        # startingMaxCards = 8, lowestCard = 0, highestCard = 9 ,lowestColorIdx = 1, highestColorIdx = 4
        deck = []
        for i in range(self.startingMaxCards):
            cardVal = randint(self.lowestCard,self.highestCard)
            colorIdx = randint(self.lowestColorIdx,self.highestColorIdx)
            deck.append(Card(self.colors[colorIdx],"number",cardVal))
        
        return deck
    
    def drawCardForPlayer(self, playerNum: int) -> bool:
        if(playerNum > len(self.players) or playerNum < 0):
            return False
        else:
            self.seed = seed()
            cardVal = randint(self.lowestCard,self.highestCard)
            colorIdx = randint(self.lowestColorIdx,self.highestColorIdx)
            self.players[playerNum].addCard(Card(self.colors[colorIdx],"number",cardVal))
            return True

    def placePlayerCard(self,playerNum: int, cardIdx: int) -> Card:
        if(playerNum > len(self.players) or playerNum < 0) or (cardIdx > len(self.players[playerNum].cards) or cardIdx < 0):
            return None
        return self.players[playerNum].cards.pop(cardIdx)
    
    def checkWinner(self) -> int:
        for player in self.players:
            if len(player.cards) == 0:
                return player.playerNum
        return -1


    def addNewPlayer(self) -> None:
        self.players.append(Player(self.initializeDeck()))
