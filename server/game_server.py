import socket
from threading import Thread, Lock
import threading
import time
import pickle
from gameState import GameState
from entities import Player 

HOST = '127.0.0.1'
PORT = 53333 

clients = []
client_num =0
lock = Lock()
currGame = GameState()
start = 0 ## = 1 if game as started 


def broadcast_message(message):
    for client in clients:
        client_socket = client['client_socket']
        
        try:
            client_socket.sendall(pickle.dumps(message))
            
        except socket.error as e:
            print(f"Error sending message to a client")
            client_socket.close() 
            clients.remove(client)
            
    

def check_start_conditions(client_socket, start, turn, data):
    if len(clients) == 1: ## so that one player cannot start the game
        client_socket.sendall("Not enough players\n")
    else:
        start = 1 
        ##if users want a game with 2 or 3 players must press start
        if start == 1: # or client_num == 4
            currGame.gameStart = True

            playerNum = data.get("playerNum")
            initializeCards = currGame.players[playerNum].cards
            broadcast_message({"playerNum": playerNum, "playerCards": initializeCards, "isGameRunning": True})
            
            time.sleep(1)
            start = 1
    return start

def handle_client(conn, addr, client):
    global currGame
    global start
    client_socket = client['client_socket']
    
    # if the player makes a valid action - changes to one to indicate to change who's turn it is
    turn_taken = 0 

    ## this is where you join the game 
    while True:
        
        try:
            message = pickle.loads(client_socket.recv(65535))
            #Remove once start conditions works with GUI
            token = message.get("token")
            data = message.get("data")
            
            if not message:   
                print(f"Client disconnected")
                raise ConnectionResetError(f"Player has disconnected.")
            
            ## OUTSIDE GAME  
            if start == 0 and currGame.gameStart == False:
                ## join game - puts the player in the waiting room and adds them to client list 
                if (token == 'JOIN GAME'):
                    client_num += 1
                    currGame.numOfPlayers += 1
                    currGame.addNewPlayer()
                    clients.append(client)
                    broadcast_message({"playerNum": client_num, "isGameRunning": False})
                
                ## start game - prompts the game to start 
                if (token == 'START GAME'):
                    start = check_start_conditions(client_socket, start, currGame.turns, data)
            
                # with lock:
                #     ## only starts when we have enough people
                #     start = check_start_conditions(client_socket, start, currGame.turns)
                
            
            ## IN GAME 
            if start == 1 and currGame.gameStart == True:
                client_num = client['client_num']

                with lock:
                    
                    if currGame.turns != client_num:
                        print("client_num", client_num)
                        ## sents a message only to that socket if it is not their turn
                        message = "It's not your turn!\n"
                        client_socket.sendall(pickle.dumps(message))
                        time.sleep(1)
                        continue
                    
                    if currGame.turns == client_num:
                        
                        
                        ## needs to be outside the lock 
                        if (token == "UNO"):
                            playerNum = data.get("playerNum")
                            ## create an uno function in the client state
                            
                        
                        if (token=="PLACE"):
                            turn_taken=1
                            playerNum = data.get("playerNum")
                            cardIdx = data.get("cardIdx")
                        
                            card =currGame.placePlayerCard(playerNum, cardIdx) ## needs to be comepared with the last card 
                        
                            broadcast_message({"playerNum": playerNum, "placedCard": card, "isGameRunning": True})
                            
                            winner = currGame.checkWinner()
                            if winner != -1:
                                currGame.gameStart = False
                                start = 0
                                broadcast_message({"winner": winner,  "isGameRunning": False})
                                

                        if(token == "DRAW"):
                            turn_taken=1
                            playerNum = data.get("playerNum")
                            card = currGame.drawCardForPlayer(playerNum)
                        
                            ##If we use deckLength
                            # deckLength = len(currGame.players[playerNum].cards)
                            # broadcast_message({"playerNum": playerNum, "deckLength": deckLength, "isGameRunning": True})

                            broadcast_message({"playerNum": playerNum, "drawnCard": card, "isGameRunning": True})
                            
                                
                if turn_taken == 1:
                    
                    with lock:
                    
                        if currGame.turns == len(clients):
                            currGame.turns = 1
                        else:
                            currGame.turns = currGame.turns + 1
                            print("currGame.turns", currGame.turns)
                            turn_taken = 0
                        # broadcast_message(f"It is now Player {currGame.turns}'s turn\n")

        
        except (socket.error, ConnectionResetError) as e:
            print(f"Error during data exchange: {e}")
            if (start == 1 and currGame.gameStart == True):
                # broadcast_message("A PLAYER DISCONNECTED, CLOSING GAME. Restart the game to play again\n")
                with lock:
                    print('in lock')
                    print('client lenght,len(clients)')
                    for client in clients:
                        print(client)
                        try:
                            print('closing')
                            client['client_socket'].close() 
                            print('close')
                        except Exception as ex:
                            print(f"Error closing socket for a client")
                            
                            # clients.remove(client)   
                print('out of lock')
            if (start == 0 and currGame.gameStart == False):
                pass
            return 
            

    # conn.close()

def listen(s):
    global client_num
    while True:
        conn, addr = s.accept()
        print("Player Added: ", addr)
        client = {'client_num': client_num,'client_socket': conn}
        Thread(target=handle_client, args = (conn, addr,client)).start()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(4) #(amount of conncetions)
        print("Waiting for connection")
   
        listen(s)
        


if __name__ == "__main__":
    main()

    
