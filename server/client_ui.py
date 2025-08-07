import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from clientState import ClientState
from ui import *


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
        self.clientManager.handleRecv()
        self.root.mainloop()

    def handleMenuBtn(self,event):
        # if hasattr(event, 'widget') and event.widget.widgetName == 'button':
        #     return
        print(event.widget.widgetName)
        print(self.clickState.menu, self.clickState.instructions, self.clickState.joinWaitingRoom)
        if event.widget:
            if event.widget.widgetName == 'button':
                if self.clickState.joinWaitingRoom:
                    waiting_room(self.root,self.clientManager.numOfPlayers, self.clickState)
                if self.clickState.credits:
                    print_credits(self.root,0,self.clickState)
                if self.clickState.menu:
                    print_menu(self.root, self.clickState)
                if self.clickState.instructions:
                    print_instructions(self.root,0,self.clickState)
                self.clickState.reset()
        
        self.clientManager.handleRecv()
    

if __name__ == "__main__":
    GUI()