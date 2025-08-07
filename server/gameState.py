from entities import * 
from random import randint,seed

class GameState:
    def __init__(self, numOfPlayers = 0):
        self.numOfPlayers = numOfPlayers
        self.players = []
        # Primarily used to keep track of individual players length of cards
        self.cardLengths = []
        self.colors = ['red','green','blue','yellow']
        self.turns = 1
        # These fields are important for gui
        self.currTurn = 0
        self.isGameOver = False
        self.seed = seed()
        self.startingMaxCards, self.lowestCard, self.highestCard, self.lowestColorIdx, self.highestColorIdx = 8, 0, 9, 1, 3
        self.menu = True ##initial screen when program runs
        self.waitingRoom = False ##player can choose to enter waiting for game
        self.gameStart = False ##game has offically started
        self.error = False ##if someone disconnects, they get error screen
        cardVal = randint(self.lowestCard,self.highestCard)
        colorIdx = randint(self.lowestColorIdx,self.highestColorIdx)
        self.lastCardPlayed = Card(self.colors[colorIdx],"number",cardVal) 

    # Used to generate a random deck depending on the seed, generating the value of the card and what color it can have
    def initializeDeck(self) -> list:
        # startingMaxCards = 8, lowestCard = 0, highestCard = 9 ,lowestColorIdx = 1, highestColorIdx = 4
        deck = []
        for i in range(self.startingMaxCards):
            cardVal = randint(self.lowestCard,self.highestCard)
            colorIdx = randint(self.lowestColorIdx,self.highestColorIdx)
            deck.append(Card(self.colors[colorIdx],"number",cardVal))
        
        return deck
    
    #Assert that the player exists
    #If they do exist, generate a new card with a new seed and add that card to the player's list
    #Update number of cards in the card length arr
    def drawCardForPlayer(self, playerNum: int) -> Card:
        if(playerNum > len(self.players) or playerNum < 0):
            # return False
            return None
        else:
            self.seed = seed()
            cardVal = randint(self.lowestCard,self.highestCard)
            colorIdx = randint(self.lowestColorIdx,self.highestColorIdx)
            self.players[playerNum].addCard(Card(self.colors[colorIdx],"number",cardVal))
            self.cardLengths[playerNum] += 1
            # return True
            return (Card(self.colors[colorIdx],"number",cardVal))

    #Same logic as adding card but we are returning the recently popped card for that player
    def placePlayerCard(self,playerNum: int, cardIdx: int) -> Card:
        if(playerNum > len(self.players) or playerNum < 0) or (cardIdx > len(self.players[playerNum].cards) or cardIdx < 0):
            return None
        self.cardLengths[playerNum] -= 1
        return self.players[playerNum].cards.pop(cardIdx)
    
    #Checks which player obj is the winner, returns -1 if no one has won
    def checkWinner(self) -> int:
        for player in self.players:
            if len(player.cards) == 0:
                return player.playerNum
        return -1
    
    def checkUno(self) -> int:
        for player in self.players:
            if len(player.cards) == 1:
                return player.playerNum
        return -1

    #Upon init of connection, game state adds a new player IF there are less than 4 players
    def addNewPlayer(self) -> None:
        if(self.numOfPlayers < 4):
            self.players.append(Player(self.initializeDeck()))
            self.cardLengths.append(7)
