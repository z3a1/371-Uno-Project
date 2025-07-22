import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 53333

def receive_data(s):
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)
        
    


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        Thread(target=receive_data, args=(s,)).start()
        while True:
            #token =
            message = input()
            s.sendall(message.encode())
            
 


if __name__ == "__main__":
    main()

    