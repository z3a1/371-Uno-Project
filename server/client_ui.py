import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import pickle
from clientState import ClientState

HOST = '127.0.0.1'
PORT = 53333

class GUI:
    def __init__(self):
        # Window init
        self.root = tk.Tk()
        self.root.title("Tkinter.Ttk Widgets Example")
        self.root.geometry("500x500")
        self.root.resizable(0,0)
        self.style = ttk.Style()

        self.clientManager = ClientState()
        self.clientManager.onGameRecv = self.checkRecv
        

        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.connect((HOST,PORT))

        # Run the application
        self.root.mainloop()
    
    
    def pauseTimer(self):
        self.isPauseTimer = not self.isPauseTimer
        if not self.isPauseTimer:
            self.root.after(1000,self.updateTimer)

    def sendMessageToServer(self):
        # payload = self.message.get()
        # TODO: Call Client State and get token
        # pass
        payload = self.message.get()
        if(payload == "DRAW"):
            self.clientManager.handleSend("DRAW", {"playerNum": self.clientManager.playerID})
        elif(payload == "INITIALIZE"):
            self.clientManager.handleSend("INITIALIZE", {"playerNum": self.clientManager.playerID})
        elif(payload == "START GAME"):
            self.clientManager.handleSend("START GAME", {"playerNum": self.clientManager.playerID})
        
      
    def sendCardToServer(self, card):
        # if(card.type == "number"):
        #     cRes = {"playerNum" : self.playerNum , "action": "PLACE", "cardIdx": self.givenCards.index(card)}
        #     cResEncoded = pickle.dumps(cRes)
        #     self.socket.sendall(cResEncoded)
        #TODO Call Client State
        # pass
        idx = self.clientManager.givenCards.index(card)
     
        self.clientManager.handleSend("PLACE", {"playerNum": self.clientManager.playerID, "cardIdx": idx})
      

    
    def checkRecv(self):
        #TODO: Call Client state and check the recieve and parse data there
        # pass
      # Clear previous buttons
        
        for btn in self.cardBtnArr:
            btn.destroy()
        self.cardBtnArr.clear()
       
        for card in self.clientManager.getPlayerGivenCards(self.clientManager.playerID):
            btn = tk.Button(self.root, text=str(card.val), bg=card.color, command=lambda c=card: self.sendCardToServer(c))
            btn.pack()
            self.cardBtnArr.append(btn)
          

    def updateTimer(self):

        if self.timer > -1 and self.isPauseTimer != True:
            print("Going Down")
            self.timer -= 1
            self.timerStrContainer.set(str(self.timer))
            self.root.after(1000,self.updateTimer)
        elif self.timer == -1:
            messagebox.showerror("UH OH", "TIMES UPPPP!")
            self.timer = 10
            self.root.after(1000,self.updateTimer)
        elif self.isPauseTimer and self.timer > -1:
            messagebox.showinfo("PAUSED","PAUSED TIMER")


if __name__ == "__main__":
    GUI()