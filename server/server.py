import socket as s
import sys
import time
import _thread as t


def handleNewClient(cSocket, hAddr,cName):
    while True:
        payload = cSocket.recv(1024)
        if payload.decode() == "end":
            break
        print(f"Payload from: ${cName}\nData: ${payload}")
    cSocket.close()



if __name__ == "__main__":
    with s.socket(s.AF_INET, s.SOCK_STREAM) as server:
        hostName = s.gethostname()
        print(hostName)
        server.bind(("127.0.0.1",8080))
        server.listen(5)

        while True:
            c, addr = server.accept()
            try:
                t.start_new_thread(handleNewClient,(c,hostName,addr))
            except (KeyboardInterrupt, SystemExit):
                break
        s.close()