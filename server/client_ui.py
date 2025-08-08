import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from clientState import ClientState
from ui import *
import queue


HOST = '127.0.0.1'
PORT = 53333

class GUI:
    def __init__(self):
        # Window init
        self.root = tk.Tk()
        self.root.title("CMPT 371 Project UNO")
        self.root.geometry("600x600")
        self.root.resizable(0,0)
        self.root.state('zoomed')

        self.clientManager = ClientState()
        self.clickState = Click()

        # self.clientManager.onGameRecv = self.checkRecv
        print_menu(self.root, self.clickState)
        # Run the application
        self.root.bind("<Button-1>",self.handleMenuBtn)
        # Fails because non blocking operation isn't completed, force it to fail on init
        # Then call it again when trying to join waiting lobby

        self.msg_queue = queue.Queue()
        # threading.Thread(target=self.listen_to_server, daemon=True).start()
        # self.poll_server()
        self.clientManager.onGameRecv = lambda: self.root.after(0, self.updateUI)
        self.root.mainloop()

        
    def handleMenuBtn(self,event):
        # if hasattr(event, 'widget') and event.widget.widgetName == 'button':
        #     return
        if self.clickState.joinWaitingRoom:
            print(self.clientManager.playerObj.playerNum)
            self.clientManager.handleSend(action="JOIN GAME",data={})
            waiting_room(self.root, self.clientManager.numOfPlayers, self.clickState)
        elif self.clickState.credits:
            print_credits(self.root,0,self.clickState)
        elif self.clickState.menu:
            print_menu(self.root, self.clickState)
        elif self.clickState.instructions:
            print_instructions(self.root,0,self.clickState)
        elif self.clickState.startGame:
            # self.clientManager.handleSend(action="START GAME", data={"playerNum": self.clientManager.playerObj["playerNum"]})
            # print(self.clientManager.playerObj["playerNum"])
            self.clientManager.isGameRunning = True
            self.clientManager.handleSend(action="START GAME",data={"playerNum": self.clientManager.playerObj.playerNum})
            print(self.clientManager.lastPlayedCard)
            print_board(self.root, 
                        self.clientManager.playerObj,
                        self.clientManager.currentPlayerTurn, 
                        self.clientManager.lastPlayedCard, 
                        self.clientManager.otherPlayerCards, 
                        self.clientManager.numOfPlayers, 
                        self.clickState)
            
        elif self.clickState.drawCard:
            self.clientManager.handleSend(action="DRAW",data={"playerNum": self.clientManager.playerObj.playerNum})
        else:
            for idx,state in enumerate(self.clickState.hand):
                if state:
                    print(state)
                    break
        self.clickState.reset()
    # def listen_to_server(self):
    #     while True:
    #         try:
    #             data = self.clientManager.cSocket.recv(65535)
    #             if not data:
    #                 print("Server closed connection")
    #                 break
    #             message = pickle.loads(data)
    #             self.msg_queue.put(message)
    #         except Exception as e:
    #             print("Error receiving from server:", e)
    #             break    

    # def poll_server(self):
    #     while not self.msg_queue.empty():
    #         msg = self.msg_queue.get()
    #         self.handle_server_message(msg)
    #     self.root.after(100, self.poll_server) 

    # def handle_server_message(self, message):
    #     if message.get("waitingRoom"):
    #         player_num = message.get("playerNum")
    #         self.clientManager.numOfPlayers = player_num
    #         waiting_room(self.root, player_num, self.clickState)

    #     elif message.get("startGame"):
    #         self.clientManager.isGameRunning = True
    #         print(self.clientManager.isGameRunning)
    #         self.clientManager.playerObj["playerNum"] = message["playerNum"]
    #         self.clientManager.lastPlayedCard = message["lastPlayedCard"]
    #         self.clientManager.givenCards = message["playerCards"]
    #         self.clientManager.currentPlayerTurn = message["currentPlayerTurn"]
    #         print("currently printingf board for player", self.clientManager.playerNum)
    #         print_board(self.root, 
    #             self.clientManager.playerObj,
    #             self.clientManager.currentPlayerTurn, 
    #             self.clientManager.lastPlayedCard, 
    #             self.clientManager.otherPlayerCards, 
    #             self.clientManager.numOfPlayers, 
    #             self.clickState)

    #     elif message.get("winner"):
    #         winner = message["winner"]
    #         tk.messagebox.showinfo("Game Over", f"Player {winner} wins!")

    def updateUI(self):
        if not self.clientManager.isGameRunning:
            waiting_room(self.root,self.clientManager.numOfPlayers,self.clickState)
        else:
            print_board(
                self.root,
                self.clientManager.playerObj,
                self.clientManager.currentPlayerTurn,
                self.clientManager.lastPlayedCard,
                self.clientManager.otherPlayerCards,
                self.clientManager.numOfPlayers,
                self.clickState
            )

if __name__ == "__main__":
    GUI()
    