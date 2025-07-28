import socket
from threading import Thread, Lock
import threading
import time
import pickle
from gameState import GameState

HOST = '127.0.0.1'
PORT = 53333 

clients = []
client_num =0
lock = Lock()
currGame = GameState()
#start = 1 if game has started
start = 0

def broadcast_message(message):
    for client in clients:
        client_socket = client['client_socket']
        
        client_socket.sendall(message.encode())

def check_start_conditions(client, client_socket, start):
    if len(clients) < 2:
        print(len(clients))
        client_socket.sendall("Waiting for more players to connect...\n".encode())
        time.sleep(1)
    else:
        broadcast_message("Press start to begin game!")
        ##if users want a game with 2 or 3 players must press start
        if start == 1 or client_num == 4:
            broadcast_message(f"All players connected! Player {turn}'s turn.\n")
            time.sleep(1)
            start = 1
    return start

def handle_client(conn, addr, client):
    global turn
    global currGame
    client_num = client['client_num']
    client_socket = client['client_socket']
    
    # if the player makes a valid action - changes to one to indicate to change who's turn it is
    # turn_taken = 0
    
    while True:
             
        ## find a way for this to only be done initially???
        with lock:
            ## only starts when we have enough people
            if start == 0:
                if len(clients) < 2:
                    # print(len(clients))
                    # client_socket.sendall("Waiting for more players to connect...\n".encode())
                    message = client_socket.recv(1024).decode() #can replace with conn
                    print(message)
                    print(client_num)
                    print(currGame.players)
                    print(currGame.numOfPlayers)
                    res = {"playerNum": currGame.players[0].playerNum , "cards": currGame.players[0].cards}
                    resEncode = pickle.dumps(res)
                    client_socket.sendall(resEncode)
                    time.sleep(1)
                    continue
                else:
                    broadcast_message("Press start to begin game!")
                    if start == 1:
                        broadcast_message(f"All players connected! Player {currGame.turns}'s turn.\n")
                        time.sleep(1)
        
        message = client_socket.recv(1024).decode() #can replace with conn
        
        with lock:
            
            if turn != client_num:
                ## sents a message only to that socket if it is not their turn
                client_socket.sendall("It's not your turn!\n".encode())
                time.sleep(1)
                continue
                
            ## if it is the turn of the correct player
            if turn == client_num:
                if(message == "1"):
                    turn_taken = 1
                    broadcast_message("Player "+ str(client_num) + " has used 1\n")
                        
                elif(message == "2"):
                    turn_taken = 1
                    broadcast_message("Player "+ str(client_num) + " has used 2\n")
                    
                #send to the other clients (update them)
                else:
                    broadcast_message("Player "+ str(client_num) + " did not take an action")
                        
        if turn_taken == 1:
            
            if turn == len(clients):
                turn = 1
            else:
                turn = turn + 1
            broadcast_message(f"It is now Player {turn}'s turn\n")

                
    # conn.close()

def listen(s):
    global client_num
    while True:
        conn, addr = s.accept()
        print("Player Added: ", addr)
    
        # with conn: 
        # data = conn.recv(1024)
        # if not data:
        #     break
       
        # print(data.decode())
        # conn.sendall(b'back at you TCP')

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

    
  