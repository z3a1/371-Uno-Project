import socket
import pickle

HOST = '127.0.0.1'
PORT = 53333

class ClientState:
    def __init__(self, playerNum: int = 0):
        #Player Cards
        self.isGameRunning = True
        # Key: PlayerNum, Val: Card Array
        self.givenCards = {}
        # Card Object of the last card played 
        self.lastPlayedCard = None
        # Map Set Of Player Num and Cards
        self.otherPlayerCards = None
        self.currentPlayerTurn = 0
        self.playerID = playerNum
        self.numOfPlayers = 0
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cSocket.connect((HOST,PORT))

        # Function Call To Check if we need to recieve anything
        self.handleRecv()

    
    def isServerDisconnect(self) -> bool:
        #Try checking if the socket can still recieve
        #Ignore if the data is 0 and check if exception happens
        try:
            res = pickle.loads(self.cSocket.recv(65535))
            if not res or res:
                return True
        except Exception as e:
            print(e)
            self.isGameRunning = False
            return False

    
    # Token and the data
    def handleSend(self,action,data):
        # Action States: [WAITING,READY,PLAYING] Only send data for the ready and playing
        # In game tokens: [Drawing, or Placing card]
        # Waiting: [NoneType], Ready: [NoneType], Playing: [Card Objects]
        #Assert fails if client is not connected
        assert(self.isServerDisconnect())
        payload = pickle.dumps({"token": action, "data": data})
        self.cSocket.sendall(payload)


    def getPlayersCard(self,playerIdx):
        if playerIdx > self.numOfPlayers or playerIdx < 0:
            return None
        else:
            return self.givenCards[playerIdx]


        
        

    def handleRecv(self):
        # Recieve the data then extract the map and determine if the val for the key is data
        # Key: lastPlayed Card, otherplayer card states, is game done, current turn of player
        # Values: Card, List[Tuple(PlayerNum, Card)], Bool, Int
        assert(self.isServerDisconnect())
        res = pickle.loads(self.cSocket.recv(65535))
        gameStillRunning = res["isGameRunning"]
        if gameStillRunning:
            for i, (idx,val) in enumerate(res.items()):
                if idx == "lastPlayedCard":
                    self.lastPlayedCard = val
                elif idx == "playerCards":
                    self.givenCards = val
                elif idx == "isGameDone":
                    self.isGameRunning = val
                elif idx == "currPlayerTurn":
                    self.currentPlayerTurn = val
        else:
            self.isGameRunning = False
