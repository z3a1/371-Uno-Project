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
            # client_socket.sendall(message.encode())
          
            client_socket.sendall(pickle.dumps(message))
            
        except socket.error as e:
            print(f"Error sending message to a client")
            client_socket.close() 
            clients.remove(client)
            
    

def check_start_conditions(client_socket, start, turn):
    if len(clients) == 1: ## so that one player cannot start the game
        client_socket.sendall("Not enough players\n".encode())
    else:
        # broadcast_message("Press start to begin game!")
        ## for now
        start = 1 
        ##if users want a game with 2 or 3 players must press start
        if start == 1 or client_num == 4:
            # broadcast_message(f"All players connected! Player {turn}'s turn.\n")
            time.sleep(1)
            start = 1
    return start

def handle_client(conn, addr, client):
    global currGame
    global start
    client_num = client['client_num']
    client_socket = client['client_socket']
    
    # if the player makes a valid action - changes to one to indicate to change who's turn it is
    turn_taken = 0 
    
    while True:
        try:
            message =pickle.loads(client_socket.recv(65535))
            #Remove once start conditions works with GUI
            token = message.get("token")
            data = message.get("data")
            if(token == "INITIALIZE"):
                playerNum = data.get("playerNum")
                initializeCards = currGame.players[playerNum].cards
                

                broadcast_message({"playerNum": playerNum, "playerCards": initializeCards, "isGameRunning": True})

            elif(token=="PLACE"):
                turn_taken=1
                playerNum = data.get("playerNum")
                cardIdx = data.get("cardIdx")
              
                card =currGame.placePlayerCard(playerNum, cardIdx)
               
                broadcast_message({"playerNum": playerNum, "placedCard": card, "isGameRunning": True})
                         

            if(token == "DRAW"):
                turn_taken=1
                playerNum = data.get("playerNum")
                card = currGame.drawCardForPlayer(playerNum)
             
                ##If we use deckLength
                # deckLength = len(currGame.players[playerNum].cards)
                # broadcast_message({"playerNum": playerNum, "deckLength": deckLength, "isGameRunning": True})

                broadcast_message({"playerNum": playerNum, "drawnCard": card, "isGameRunning": True})


            # # message = client_socket.recv(1024).decode() #can replace with conn
            # if not message:   
            #     print(f"Client disconnected")
            #     raise ConnectionResetError(f"Player has disconnected.")
            
            # ## here for now
            # if (message == 'start game'):
            #     start = check_start_conditions(client_socket, start, currGame.turns)

            # if (start == 0):
            #     with lock:
            #         ## only starts when we have enough people
            #         start = check_start_conditions(client_socket, start, currGame.turns)
                    
            # if start == 1:
            #     ## for when uno calling is possible  - or have it open all the time
            #         # if one person has one card:
            #         #     anyone can press the uno button but only the uno button
            #     # if message == 'UNO':
            #     #         broadcast_message("Player "+ str(client_num) + " called UNO\n")
                
            #     with lock:
            #         print(token)
            #         print(data)
            #         if currGame.turns != client_num:
            #             print("client_num", client_num)
            #             ## sents a message only to that socket if it is not their turn
            #             # client_socket.sendall("It's not your turn!\n")
            #             time.sleep(1)
            #             continue
                        
            #         ## if it is the turn of the correct player
            #         if currGame.turns == client_num:

            #             if(token=="PLACE"):
            #                 turn_taken=1
            #                 playerNum = data.get("playerNum")
            #                 cardIdx = data.get("cardIdx")
            #                 placedCard =currGame.placePlayerCard(playerNum, cardIdx)

            #                 broadcast_message({"playerNum": playerNum, "card": placedCard})
                            
            #                 #Tell other clients the action taken

            #             if(token == "DRAW"):
            #                 print(message)
            #                 turn_taken=1
            #                 playerNum = data.get("playerNum")
            #                 currGame.drawCardForPlayer(playerNum)
                           
            #                 deckLength = len(currGame.players[playerNum].cards)
            #                 broadcast_message({"playerNum": playerNum, "deckLength": deckLength})


                                
            #     if turn_taken == 1:
                    
            #         with lock:
                    
            #             if currGame.turns == len(clients):
            #                 currGame.turns = 1
            #             else:
            #                 currGame.turns = currGame.turns + 1
            #                 print("currGame.turns", currGame.turns)
            #                 turn_taken = 0
            #             # broadcast_message(f"It is now Player {currGame.turns}'s turn\n")

        
        except (socket.error, ConnectionResetError) as e:
            print(f"Error during data exchange: {e}")
            if (start == 1):
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
            if (start == 0):
                pass
            return 
            

    # conn.close()

def listen(s):
    global client_num
    while True:
        conn, addr = s.accept()
        print("Player Added: ", addr)
 

        client_num += 1
        currGame.numOfPlayers += 1
        currGame.addNewPlayer()
        client = {'client_num': client_num,'client_socket': conn}
        clients.append(client)
 
       
        Thread(target=handle_client, args = (conn, addr, client)).start()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(4) #(amount of conncetions)
        print("Waiting for connection")
   
        listen(s)
        


if __name__ == "__main__":
    main()

    
  