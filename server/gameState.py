from server.entities import *
from random import randint,seed

class GameState:
    def __init__(self, numOfPlayers):
        self.numOfPlayers = numOfPlayers
        self.players = []
        self.colors = ['r','g','b','y']

        for i in range(self.numOfPlayers):
            self.players.append(Player(self.initializeDeck()))

    def initializeDeck(self):
        seed()
        startingMaxCards = 8, lowestCard = 0, highestCard = 9 ,lowestColorIdx = 1, highestColorIdx = 4
        deck = []
        for i in range(startingMaxCards):
            cardVal = randint(lowestCard,highestCard)
            colorIdx = randint(lowestColorIdx,highestColorIdx)
            deck.append(Card(self.colors[colorIdx],None,cardVal))
        
        return deck