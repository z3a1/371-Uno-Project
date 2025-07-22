import socket
from threading import Thread, Lock
import threading
import time

HOST = '127.0.0.1'
PORT = 53333 

clients = []
client_num =0
lock = Lock()
turn = 1

def broadcast_message(message):
    for client in clients:
        client_socket = client['client_socket']
        
        client_socket.sendall(message.encode())

def handle_client(conn, addr, client):
    global turn
    client_num = client['client_num']
    client_socket = client['client_socket']
    
    # if the player makes a valid action - changes to one to indicate to change who's turn it is
    turn_taken = 0
    
    while True:
             
        ## find a way for this to only be done initially???
        with lock:
            ## only starts when we have enough people
            if len(clients) < 2:
                print(len(clients))
                client_socket.sendall("Waiting for more players to connect...\n".encode())
                time.sleep(1)
                continue
            else:
                broadcast_message(f"All players connected! Player {turn}'s turn.\n")
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

    
  