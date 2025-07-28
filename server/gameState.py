from entities import * 
from random import randint,seed

class GameState:
    def __init__(self, numOfPlayers = 0):
        self.numOfPlayers = numOfPlayers
        self.players = []
        self.colors = ['red','green','blue','yellow']
        self.turns = 1
        self.isGameOver = False
        self.currTurn = 0

    def initializeDeck(self):
        seed()
        # startingMaxCards = 8, lowestCard = 0, highestCard = 9 ,lowestColorIdx = 1, highestColorIdx = 4
        startingMaxCards, lowestCard, highestCard, lowestColorIdx, highestColorIdx = 8, 0, 9, 1, 3
        deck = []
        for i in range(startingMaxCards):
            cardVal = randint(lowestCard,highestCard)
            colorIdx = randint(lowestColorIdx,highestColorIdx)
            deck.append(Card(self.colors[colorIdx],None,cardVal))
        
        return deck

    def addNewPlayer(self):
        self.players.append(Player(self.initializeDeck()))
