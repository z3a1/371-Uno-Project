import socket as s
import sys
import _thread   
    

if __name__ == "__main__":
    with s.socket(s.AF_INET, s.SOCK_STREAM) as server:
        server.connect(('127.0.0.1',8080))
        while True:
            res = input("Enter the Prompt: ")
            if res == "end":
                break
            else:
                server.send(res.encode())
        s.close()
