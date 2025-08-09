import socket
from threading import Thread, Lock
import threading
import time
import pickle
from gameState import GameState
from entities import Player 
import os

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

def send_individual_message(client_num,message):
    currClient = clients[client_num - 1]
    cSocket = currClient["client_socket"]
    try:
        cSocket.sendall(pickle.dumps(message))
    except socket.error as e:
        print("ERROR: {e}")
        cSocket.close()
        clients.remove(currClient)
        

            
    

def check_start_conditions(client_socket, start, turn, data):
    global currGame
    if len(clients) == 1: ## so that one player cannot start the game
        #TODO: Should be client send all xD
        client_socket.sendall(pickle.dumps({"Error": "Not enough players\n"}))
    else:
        start = 1 
        ##if users want a game with 2 or 3 players must press start
        if start == 1: # or client_num == 4
            currGame.gameStart = True

            playerNum = data.get("playerNum")
            print(playerNum)
            currGame.turns = playerNum
            # Player number has to be offset because of how arrays start!!!

            # print(initializeCards)
            for idx,client in enumerate(clients):
                initializeCards = currGame.players[idx].cards
                send_individual_message(client_num=idx,message={"playerNum": idx, "startGame": True, "playerCards": initializeCards, "otherCards": currGame.cardLengths ,"lastPlayedCard": currGame.lastCardPlayed ,"isGameRunning": True})
            
            time.sleep(1)
            start = 1
    return start

def handle_client(conn, addr, client):
    global currGame
    global start
    global client_num
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
                    client["client_num"] = client_num
                    currGame.numOfPlayers += 1
                    currGame.addNewPlayer(client_num)
                    clients.append(client)
                    
                    broadcast_message({"playerNum": currGame.players[client_num - 1].playerNum , "waitingRoom": True, "numOfPlayers":currGame.numOfPlayers,"lastPlayedCard": currGame.lastCardPlayed ,"isGameRunning": False})
                
                ## start game - prompts the game to start 
                if (token == 'START GAME'):
                    start = check_start_conditions(client_socket, start, currGame.turns, data)
            
                # with lock:
                #     ## only starts when we have enough people
                #     start = check_start_conditions(client_socket, start, currGame.turns)
                
            
            ## IN GAME 
            if start == 1 and currGame.gameStart == True:
                client_num = client['client_num'] + 1
                print(client_num)

                with lock:
                    broadcast_message({"currentPlayerTurn": client_num})
                    if (token == "UNO"):
                        playerNum = data.get("playerNum")
                        uno = currGame.checkUno()
                        if(uno != -1):
                            if(playerNum != uno):
                                broadcast_message({"playerNum": uno, "drawnCard": card})
                            else:
                             broadcast_message({"playerNum": playerNum, "uno":uno}) ##THEY HAVE ONE
                        else:
                            broadcast_message({"playerNum": playerNum, "drawnCard": card})                   

                    if currGame.turns != client_num:
                        print("client_num" + str(client_num) + " currGame.turns: " + str(currGame.turns))
                        ## sents a message only to that socket if it is not their turn
                        message = "It's not your turn!\n"
                        client_socket.sendall(pickle.dumps({"message": message}))
                        time.sleep(1)
                        continue

                  

                    if currGame.turns == client_num:

                        if (token=="PLACE"):
                            print("IN PLACE")
                            turn_taken=1
                            playerNum = data.get("playerNum")
                            cardIdx = data.get("cardIdx")
                            print("cardIdx", cardIdx)
                        
                            card = currGame.placePlayerCard(playerNum, cardIdx - 1) ## needs to be comepared with the last card 
                            if card:
                                broadcast_message({"playerNum": playerNum, "lastPlayedCard": card})
                                print("Card num: " + str(card.val) + "Card color: " + card.color)
                                currGame.lastCardPlayed = card
                                send_individual_message(playerNum, {"playerNum":playerNum, "playerCards": currGame.players[playerNum].cards})
                                print("Last Card: " + currGame.lastCardPlayed.color + " " + str(currGame.lastCardPlayed.val))
                                winner = currGame.checkWinner()
                                if winner != -1:
                                    currGame.gameStart = False
                                    start = 0
                                    broadcast_message({"winner": winner,  "isGameRunning": False})

                        if(token == "DRAW"):
                            turn_taken=1
                            playerNum = data.get("playerNum")
                            card = currGame.drawCardForPlayer(playerNum)
                            print("Card: {card}")
                            if card:
                                currGame.lastCardPlayed = card
                                # broadcast_message({"playerNum": playerNum, "drawnCard": card})
                                send_individual_message(playerNum - 1,{"playerNum": playerNum, "drawnCard": card})
                        
                            ##If we use deckLength
                            # deckLength = len(currGame.players[playerNum].cards)
                            # broadcast_message({"playerNum": playerNum, "deckLength": deckLength, "isGameRunning": True})

                            
                                
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
                            broadcast_message({"isGameRunning": False})
                            client['client_socket'].close() 
                            print('close')
                        except Exception as ex:
                            print(f"Error closing socket for a client")
                            
                            # clients.remove(client)   
                    os._exit(1)
                print('out of lock')
            if (start == 0 and currGame.gameStart == False):
                pass
            return
        
        # These were added just for the different test cases that a client closes their end
        except EOFError as e:
            # When client leaves, connection is still valid, catch the EOFError to force exit the server
            print(e)
            os._exit(1)
        except (socket.error, WindowsError) as e:
            print(e)
            os._exit(1)

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

    
