import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

class GUI:
    def __init__(self):
        # Window init
        self.root = tk.Tk()
        self.root.title("Tkinter.Ttk Widgets Example")
        self.root.geometry("500x500")
        self.root.resizable(0,0)

        self.timer = 10
        self.isPauseTimer = False
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST,PORT))


        self.label = ttk.Label(self.root, text="This is a Tkinter.Ttk Label")
        self.label.pack()

        self.message = tk.StringVar()


        self.entry = ttk.Entry(self.root,textvariable=self.message)
        self.entry.pack()
        
        self.entryBtn = ttk.Button(self.root,text = "Send to Server", command=self.sendMessageToServer)
        self.entryBtn.pack()

        self.button = ttk.Button(self.root, text="Click Me To Pause", command=self.pauseTimer)
        self.button.pack()

        self.timerStrContainer = tk.StringVar(master=self.root,value=str(self.timer))

        self.timerLabel = tk.Label(self.root,textvariable=self.timerStrContainer)
        self.timerLabel.pack()

        #Init Timer
        self.root.after(1000,self.updateTimer)

        # Run the application
        self.root.mainloop()
    
    def pauseTimer(self):
        self.isPauseTimer = not self.isPauseTimer
        if not self.isPauseTimer:
            self.root.after(1000,self.updateTimer)

    def sendMessageToServer(self):
        payload = self.message.get()
        Thread(target=receive_data, args=(self.socket,)).start()
        self.socket.sendall(payload.encode())

    
    def updateTimer(self):

        if self.timer > -1 and self.pause != True:
            print("Going Down")
            self.timer -= 1
            self.timerStrContainer.set(str(self.timer))
            self.root.after(1000,self.updateTimer)
        elif self.timer == -1:
            messagebox.showerror("UH OH", "TIMES UPPPP!")
            self.timer = 10
            self.root.after(1000,self.updateTimer)
        elif self.pause and self.timer > -1:
            messagebox.showinfo("PAUSED","PAUSED TIMER")


if __name__ == "__main__":
    GUI()