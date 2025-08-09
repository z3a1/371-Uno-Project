import socket
import pickle
import threading
from entities import Player
from entities import Card
HOST = '127.0.0.1'
PORT = 53333

class ClientState:
    def __init__(self, playerNum: int = 0):
       

        self.isGameRunning = False
        # The assigned player object for the given client
        # self.playerObj = {}
        self.playerObj = Player(playerNum=playerNum, cards=[])
        # self.playerObj["playerNum"] = playerNum
        # Card Object of the last card played 
        self.lastPlayedCard = None
        # Map Set Of Player Num and Cards -> self.cardLengths
        self.otherPlayerCards = []
        self.currentPlayerTurn = 0
        self.numOfPlayers = 0
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cSocket.connect((HOST,PORT))
        self.waitingRoom = False ##player can choose to enter waiting for game
        self.error = False ##if someone disconnects, they get error screen
        # Function Call To Check if we need to recieve anything
        self.unoCaught = [0,0,0,0]

        self.uno = -1

        # currTurn: Whos current turn is it, turns: How many turns the game has taken
        self.turns = 0
        self.menu = True
        self.gameStart = False

        self.onGameRecv = None 
        threading.Thread(target=self.handleRecv, daemon=True).start()

    
    # Token and the data
    def handleSend(self,action,data):
        # Action States: [WAITING,READY,PLAYING] Only send data for the ready and playing
        # In game tokens: [Drawing, or Placing card]
        # Waiting: [NoneType], Ready: [NoneType], Playing: [Card Objects]
        #Assert fails if client is not connected
        # assert(not self.isServerDisconnect())
        payload = pickle.dumps({"token": action, "data": data})
        self.cSocket.sendall(payload)


    # Returns the given cards of the player obj
    def getPlayersCard(self,playerIdx):
        if playerIdx > self.numOfPlayers or playerIdx < 0:
            return None
        else:
            return self.givenCards[playerIdx]


    # Helper function to parse if the res is a python dictionary, assumes it is and the check is done in
    # Handle recv function
    def parseServerRecv(self, res):
        print("parseServerRcv")
        print(res)
        for i, (idx,val) in enumerate(res.items()):
            if idx == "waitingRoom":
                self.waitingRoom = val
            elif idx == "startGame":
                self.isGameRunning = val
            elif idx == "playerNum":
                # self.playerObj["playerNum"] = val
                self.playerObj.playerNum = val
                # self.numOfPlayers = val
            elif idx == "currentPlayerTurn":
                self.currentPlayerTurn = val
            elif idx == "numOfPlayers":  
                self.numOfPlayers = val
            elif idx == "playerCards":
                self.playerObj.cards =val
            elif idx == "otherCards":
                self.otherPlayerCards = val  
            elif idx == "lastPlayedCard":
                self.lastPlayedCard = val
            elif idx == "drawnCard":
                print("Drawn Card: {val.color} {val.val}")
                self.playerObj.addCard(val)
        if self.onGameRecv:
            self.onGameRecv()
                        
        

    def handleRecv(self):
        # Recieve the data then extract the map and determine if the val for the key is data
        # Key: lastPlayed Card, otherplayer card states, is game done, current turn of player
        # Values: Card, List[Tuple(PlayerNum, Card)], Bool, Int
        while True:
            # assert(self.isServerDisconnect())
            # if(not self.isGameRunning):
            res = pickle.loads(self.cSocket.recv(65535))
            if(isinstance(res,dict)):
                self.parseServerRecv(res)
                while self.isGameRunning:
                    res = pickle.loads(self.cSocket.recv(65535))
                    if(isinstance(res,dict)):
                        if(self.isGameRunning):
                            print("self.isGameRunning: {self.isGameRunning}")
                        # gameStillRunning = res["isGameRunning"]
                        if self.isGameRunning:
                            self.parseServerRecv(res)
                        else:
                            self.isGameRunning = False
                    else:
                        print(res)
