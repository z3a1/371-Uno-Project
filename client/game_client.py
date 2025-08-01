import socket
from threading import Thread
import sys
import os

HOST = '127.0.0.1'
PORT = 53333

def receive_data(s):
    
    while True:
        try:
            
            data = s.recv(1024).decode()
            if not data:
                break
            print(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break
    
    print("Closing the connection...")
    os._exit(0)
        
    


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            Thread(target=receive_data, args=(s,)).start()
            while True:
                #token =
                message = input()
                s.sendall(message.encode())
    except (ConnectionError, Exception) as e:
        print(f"Error connecting to the server: {e}")
        sys.exit(1)
            
 


if __name__ == "__main__":
    main()

    