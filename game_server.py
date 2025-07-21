import socket
from threading import Thread
import threading

HOST = '127.0.0.1'
PORT = 53333 

clients = []
client_num =0

def broadcast_message(message):
    for client in clients:
        client_socket = client['client_socket']
        
        client_socket.sendall(message.encode())

def handle_client(conn, addr, client):
    client_num = client['client_num']
    client_socket = client['client_socket']
    while True:
        message = client_socket.recv(1024).decode() #can replace with conn

        if(message == "1"):
            broadcast_message("Player "+ str(client_num) + " has used 1\n")
          
        elif(message == "2"):
            broadcast_message("Player "+ str(client_num) + " has used 2\n")
    
        #send to the other clients (update them)
        else:
            broadcast_message("Player "+ str(client_num) + " did not take an action")
        
    conn.close()

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

    
  