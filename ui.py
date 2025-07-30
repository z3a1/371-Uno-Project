import tkinter as tk
import tkinter.font as tkFont
from tkinter import *

#returns 0 if user did not atttempt to join game, 1 if yes
#ie open socket if return value is 1
def print_menu(root, num_players):
    clear_root(root)
    root.title("Main Menu")
    root.geometry('600x600')
    root.configure(bg='light yellow')
    menu_font = tkFont.Font(family="Verdana", size=24, weight=tk.NORMAL)

    #1 if user clciks Join Game, 0 otherwise
    user_click = tk.IntVar()
    user_click.set(0)

    join_game = tk.Button(root, text="Join Game", font=menu_font, command=lambda: testy("HELLPPPP"))
    join_game.place(x=240, y=200)
    instructions = tk.Button(root, text="Instructions", font=menu_font, command=lambda: print_instructions(root, num_players))
    instructions.place(x=240, y=260)
    credits = tk.Button(root, text="Credits", font=menu_font, command=lambda: print_credits(root, num_players))
    credits.place(x=240, y=320)
     
    return 0
#player: int from [0, 3]
#hand: list of up to 7 elements
#the last three cards played
def print_board(root, player, hand, deck):
    root.title("Main Game")
    root.geometry('600x600')
    turn_info()
    return

def turn_info(root, player):
    turn_font = tk.font.Font(family="Arial", size=24, weight=tk.NORMAL)
    turn_text = "It is now Player {player}'s turn."
    turn_label = tk.Label(root, text=turn_text, font=turn_font)
    turn_label.place(x=100, y=50)
    return

def get_click_val():
    global click_val

##craete individual card
def init_card(num, col, type, root):
    if col == 0:
        card_col = "blue"
    elif col == 1:
        card_col = "red"
    elif col == 2:
        card_col = "yellow"
    else: 
        card_col = "red"

    canvas = Canvas(root, bg="white",
           height=200, width=500)
    canvas.place(x=50, y=500)
    card = canvas.create_rectangle(100, 220, 150, 100, outline="black", fill=card_col, width=2)
    return 

#print all cards at bottom of screen
def print_hand(cards):
    return 0

#clear screen
def clear_root(root):
    for widget in root.winfo_children():
        widget.destroy()

def print_credits(root, num_players):
    clear_root(root)
    root.configure(bg='purple')
    creds_font = tkFont.Font(family="Arial", size=14)
    creds = (
        "GAME CREATED BY:\n\n"
        "-- Serena Dhillon\n"
        "-- Jennifer Grinberg\n"
        "-- Paul Colonia \n"
        "-- Amir Nur Saidy\n"
        "-- Please sort by alphabet! n"
    )

    label = tk.Label(root, text=creds, font=creds_font, bg='purple', fg='white', justify='left')
    label.pack(pady=100, padx=20)

    back_button = tk.Button(root, text="Back", font=creds_font, command=lambda: print_menu(root, num_players))
    back_button.pack(pady=20)
    return 0

def print_instructions(root, num_players):
    clear_root(root)
    root.configure(bg='sky blue')
    instr_font = tkFont.Font(family="arial", size=14)
    instructions = (
        "HOW TO PLAY:\n\n"
        "-- Designed for 2-4 players\n"
        "-- Initially dealt 7 cards\n"
        "-- Each card has a colour or number\n"
        "-- You will take turns playing a card"
        "-- The card you play must be either the same number\n"
        "or colour...\n"
        "-- If you cannot or willnot play, then you mist draw \n"
        "a card...\n\n"
        " OBJECTIVE: \n\n"
        "Be the first to run out of cards!\n\n"
        "-- Special Rules:\n"
        "-- If you or someone has one card remained, press UNO!\n"
    )

    label = tk.Label(root, text=instructions, font=instr_font, bg='sky blue', fg='white', justify='left')
    label.pack(pady=100, padx=20)

    back_button = tk.Button(root, text="Back", font=instr_font, command=lambda: print_menu(root, num_players))
    back_button.pack(pady=20)
    return 0

def you_win(root):
    return 0

def you_lose(root):
    root.title("YOU LOSE")
    root.configure(bg="red")
    root.geometry("600x600")
    msg = tk.Label(root, text="Hello, Tkinter!", font=("Helvetica", 64), bg="red", fg="white")
    msg.pack(pady=100)
    return 0

##DEMO RUN##
#DELETE FOR FINAL VERSION#

root = tk.Tk()
print_menu(root, 3)
#instructions(root, 3)
root.mainloop()