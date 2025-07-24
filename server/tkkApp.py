import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class GUI:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Tkinter.Ttk Widgets Example")
        self.root.geometry("500x500")
        self.root.resizable(0,0)
        self.timer = 10
        self.pause = False

        # Create a label widget
        self.label = ttk.Label(self.root, text="This is a Tkinter.Ttk Label")
        self.label.pack()

        # Create an entry widget
        self.entry = ttk.Entry(self.root)
        self.entry.pack()
        

        # Create a button widget
        self.button = ttk.Button(self.root, text="Click Me To Pause", command=self.pauseTimer)
        self.button.pack()

        self.stringVar = tk.StringVar(master=self.root,value=str(self.timer))

        self.timerLabel = tk.Label(self.root,textvariable=self.stringVar)
        self.timerLabel.pack()

        self.root.after(1000,self.updateTimer)

        # Run the application
        self.root.mainloop()
    
    def pauseTimer(self):
        self.pause = not self.pause
        if not self.pause:
            self.root.after(1000,self.updateTimer)
    
    def updateTimer(self):

        if self.timer > -1 and self.pause != True:
            print("Going Down")
            self.timer -= 1
            self.stringVar.set(str(self.timer))
            self.root.after(1000,self.updateTimer)
        elif self.timer == -1:
            messagebox.showerror("UH OH", "TIMES UPPPP!")
            self.timer = 10
            self.root.after(1000,self.updateTimer)
        elif self.pause and self.timer > -1:
            messagebox.showinfo("PAUSED","PAUSED TIMER")


if __name__ == "__main__":
    GUI()