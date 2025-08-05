import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from clientState import *
from entities import *
import random

"""
Main GUI Functions

--How to use:
a) At each iteration of game loop, call the appropriate public gui function
(ie print_menu(), print_board(), print_result(), waiting_room(), 
disconnection(), etc with appropriate args)
b) Upon button clicks, gui functions may modify fields from gameState and 
Player classes. These fields determine which gui screen is to be called next
loop
"""
#returns 0 if user did not atttempt to join game, 1 if yes
#ie open socket if return value is 1
def print_menu(root, num_players, state):
    res = 0
    _screen_set_up(root, "Main Menu", "Verdana", "light yellow")
    menu_font = tkFont.Font(family="Verdana", size=24, weight=tk.NORMAL)
    frame = tk.Frame(root, bg="light yellow")
    frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  

    join_game = tk.Button(frame, text="Join Game", font=menu_font, command=lambda: _curr_state(state, "wait"))
    join_game.grid(row = 0, column = 0, sticky = W, pady = 5)
    instructions = tk.Button(frame, text="Instructions", font=menu_font, command=lambda: _print_instructions(root, num_players))
    instructions.grid(row = 1, column = 0, sticky = W, pady = 5)
    credits = tk.Button(frame, text="Credits", font=menu_font, command=lambda: _print_credits(root, num_players))
    credits.grid(row = 2, column = 0, sticky = W, pady = 5)

    if (state.waitingRoom == True):
        res = 1 
    return res

#This is the screen players see while waiting for others to join ganme
#Need at least two players to manually start game
#Game automatically starts when fourth player joins
def waiting_room(root, state):
    _screen_set_up(root, "Waiting Room", "Verdana", "tan1")
    wait_font = tkFont.Font(family="Verdana", size=24, weight=tk.NORMAL)
    frame = tk.Frame(root, bg="tan1")
    frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER) 

    msg = "Waiting for more players to join..."
    label = tk.Label(frame, text=msg, font=wait_font, bg='tan1', fg='white', justify='left')
    label.grid(row = 0, column = 0, sticky = "ew", pady = 2)
    if state.numOfPlayers == 4:
        state.isGameRunning = True
    else: 
        msg2 = f"\nThere is currently {state.numOfPlayers} enrolled."
        label = tk.Label(frame, text=msg2, font=wait_font, bg='tan1', fg='white', justify='left')
        label.grid(row = 1, column = 0, sticky = "ew", pady = 2)
        if state.numOfPlayers > 1:     
            start = tk.Button(frame, text="Start!", font=wait_font, command=lambda: _curr_state(state, "start"))
            start.grid(row=2, column=0, sticky = "ew", pady = 40)

    return

#player: int from [0, 3]
#hand: list of up to 7 elements
#the last three cards played
def print_board(root, player, state, lastCard, card_nums):
    screen_col = "deep sky blue"
    main_font = tk.font.Font(family="Arial", size=24, weight=tk.NORMAL)
    _screen_set_up(root, "Main Game", main_font, screen_col)
    _turn_info(root, state, screen_col)

    #print "face down deck" in centre
    frameCentre = tk.Frame(root, bg=screen_col)
    frameCentre.place(relx=0.5, rely=0.4, anchor="center")  
    deck = tk.Label(frameCentre, text="Deck", font=("Helvetica", 14), bg="grey50", fg='white', justify='left', width=5, height=5)
    deck.grid(row = 0, column = 1, sticky = "", pady = 2, padx=8)
    #print last card played
    prevCard = tk.Label(frameCentre, bg=lastCard.color, text=lastCard.type, font=("Helvetica", 34), fg='grey69', width=2, height=2)
    prevCard.grid(row = 0, column = 0, sticky = "", pady = 10, padx=8)
    #print draw card button:
    drawCardBtn = tk.Button(frameCentre, text="Draw\n card", font=("Helvetica", 20), command=lambda: _draw_card(player))
    drawCardBtn.grid(row=0, column=2, sticky = "", padx=8)
    
    _print_hands(root, state, player, card_nums, screen_col)

    return

#Displays winner/loser screen when game concludes
#@: root --> screen to display, state -->game state (to be changed upon 
#button click), player-->info on if player wins
def game_res(root, player, state):
    if player.win == True:
        _you_win(root)
    else:
        _you_lose(root)
    btn = tk.Button(root, text="Play Again", font=("Helvetica", 32), command=lambda: _curr_state(state, "restart"))
    btn.grid(row = 2, column = 1)

#displays error when disconnection occurs suddenly
#@: root --> screen to display, state -->game state (to be changed upon 
#button click)
def disconnection(root, state):
    _clear_screen(root)
    root.title("ERROR")
    root.configure(bg="red")
    root.geometry("600x600")
    msg = "Someone has disconnected so\n the game is now over :("
    err = tk.Label(root, text=msg, font=("Helvetica", 32), bg="red", fg="white")
    err.grid(row = 1, column = 1, sticky = "ew", pady = 100, padx = 90)
    btn = tk.Button(root, text="Play Again", font=("Helvetica", 32), command=lambda: _curr_state(state, "restart"))
    btn.grid(row = 2, column = 1)

"""
Private Helper Functions
"""

def _curr_state(currState, stateStr):
    if stateStr == "wait":
        currState.waitingRoom = True
    if stateStr == "start":
        currState.isGameRunning = True
    if stateStr == "restart":
        currState.waitingRoom = False
        currState.isGameRunning = False
        currState.menu = True
        currState.numOfPlayers = 0
    return 

def _play_card(p, index, prevCard):
    if p.turn == True:
        if p.cards[index].color == prevCard.color or p.cards[index].type == prevCard.type:
            #now there is a new prevCard
            prevCard.color = p.cards[index].color
            prevCard.type = p.cards[index].type
            p.playCard(index)
    p.turn = False

def _draw_card(p):
    if p.turn == True:
        newCard = Card()
        #could not find vars for these values so they are hardcoded
        #how do they correspond to colour strings? ie card.type
        newCard.val = random.randint(0,8)
        newCard.color = random.randint(1, 4)
        p.addCard()
    p.turn = False

def _clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

def _screen_set_up(root, heading, font, colour):
    _clear_screen(root)
    root.title(heading)
    root.geometry('600x600')
    root.configure(bg=colour)
    menu_font = tkFont.Font(family=font, size=24, weight=tk.NORMAL)

def _you_win(root):
    root.title("Winner!")
    root.configure(bg="green2")
    root.geometry("600x600")
    win = tk.Label(root, text="YOU WIN!!!!!!", font=("Helvetica", 64), bg="green2", fg="white")
    win.grid(row = 1, column = 1, sticky = "ew", pady = 100, padx = 80)
    return 

def _you_lose(root):
    root.title("Loser!")
    root.configure(bg="orange red")
    root.geometry("600x600")
    lose = tk.Label(root, text="YOU LOSE!!!!!", font=("Helvetica", 64), bg="orange red", fg="white")
    lose.grid(row = 1, column = 1, sticky = "ew", pady = 100, padx = 80)
    return 

##credits found from main menu
def _print_credits(root, num_players):
    _screen_set_up(root, "Credits", "Verdana", "purple")
    frame = tk.Frame(root, bg="purple")
    frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  
    creds_font = tkFont.Font(family="Arial", size=14)
    creds = (
        "GAME CREATED BY:\n\n"
        "-- Serena Dhillon\n\n"
        "-- Jennifer Grinberg\n\n"
        "-- Paul Colonia \n\n"
        "-- Amir Nur Saidy\n\n"
    )

    label = tk.Label(frame, text=creds, font=creds_font, bg='purple', fg='white', justify='left')
    label.grid(row = 0, column = 0, sticky = W, pady = 2)

    back_button = tk.Button(frame, text="Back", font=creds_font, command=lambda: print_menu(root, num_players, state))
    back_button.grid(row = 1, column = 0, sticky = W, pady = 2)
    return 0

##credits found from main menu
def _print_credits(root, num_players):
    _screen_set_up(root, "Credits", "Verdana", "purple")
    frame = tk.Frame(root, bg="purple")
    frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  
    creds_font = tkFont.Font(family="Arial", size=14)
    creds = (
        "GAME CREATED BY:\n\n"
        "-- Serena Dhillon\n\n"
        "-- Jennifer Grinberg\n\n"
        "-- Paul Colonia \n\n"
        "-- Amir Nur Saidy\n\n"
    )

    label = tk.Label(frame, text=creds, font=creds_font, bg='purple', fg='white', justify='left')
    label.grid(row = 0, column = 0, sticky = W, pady = 2)

    back_button = tk.Button(frame, text="Back", font=creds_font, command=lambda: print_menu(root, num_players, state))
    back_button.grid(row = 1, column = 0, sticky = W, pady = 2)
    return 0

#game instrcutions found at main menu
def _print_instructions(root, num_players):
    _screen_set_up(root, "How to Play", "Verdana", "sky blue")

    instr_font = tkFont.Font(family="arial", size=14)
    frame = tk.Frame(root, bg="sky blue")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  
    instructions = (
        "HOW TO PLAY:\n\n"
        "-- Designed for 2-4 players\n\n"
        "-- Initially dealt 7 cards\n\n"
        "-- Each card has a colour or number\n\n"
        "-- You will take turns playing a card\n\n"
        "-- The card you play must be either the same number\n"
        "or colour...\n\n"
        "-- If you cannot or willnot play, then you mist draw \n"
        "a card...\n\n"
        " OBJECTIVE: \n\n"
        "Be the first to run out of cards!\n\n"
        "-- Special Rules:\n\n"
        "-- If you or someone has one card remained, press UNO!\n"
    )

    label = tk.Label(frame, text=instructions, font=instr_font, bg='sky blue', fg='white', justify='left')
    label.grid(row = 0, column = 0, sticky = W, pady = 2)

    back_button = tk.Button(frame, text="Back", font=instr_font, command=lambda: print_menu(root, num_players, state))
    back_button.grid(row = 1, column = 0, sticky = W, pady = 2)
    return 0

#print all cards at bottom of screen
#pself -- players own hand, face up
#p2-p4: other players, cards printed face down
#card_nums is a list where gelements are how much cards other 
#index corresponds to playerID
#players currently have in their hands
#prev_card: last cardf played
def _print_hands(root, state, player, card_nums, col):
    hand_font = tkFont.Font(family="Helvetica", size=45)
    #print user's own cards
    frameSelf = tk.Frame(root, bg=col)
    frameSelf.place(relx=0.5, rely=0.9, anchor="s")  
    for index, currCard in enumerate(player.cards):
        pseudoBtn = tk.Label(
            frameSelf,
            text=str(currCard.type),
            font=hand_font,
            bg=currCard.color.lower(), 
            fg="gray48",
            width=2,
            height=2,
            relief="ridge",
            bd=4,
            cursor="hand2",
            padx=4,
        )

        pseudoBtn.bind(
            "<Button-3>",
            lambda e, i=index: _play_card(player, i, state.lastPlayedCard)
        )

        pseudoBtn.bind("<Enter>", lambda e, btn=pseudoBtn: btn.config(bg="purple"))
        pseudoBtn.bind("<Leave>", lambda e, btn=pseudoBtn, col=currCard.color.lower(): btn.config(bg=col))
        pseudoBtn.grid(row = 0, column = index, padx=4)


    ##print number of cards across screen of opponents
    if state.numOfPlayers == 2:
        fontCol = _if_turn(state, 0)
        otherCards1 = tk.Frame(root, bg=col)
        otherCards1.place(relx=0.5, rely=0.1, anchor="n")
        label1 = tk.Label(otherCards1, font=hand_font, text=str(card_nums[0]), bg=col, fg=fontCol, justify='left')
        label1.grid(row = 0, column = 0, sticky = "", pady = 2)
    else:
        fontCol1 = _if_turn(state, 0)
        otherCards1 = tk.Frame(root, bg=col)
        otherCards1.place(relx=0.1, rely=0.5, anchor="w")
        label1 = tk.Label(otherCards1,font=hand_font, text=str(card_nums[0]), bg=col, fg=fontCol1, justify='left')
        label1.grid(row = 0, column = 0, sticky = "", pady = 2)

        fontCol2 = _if_turn(state, 1)
        otherCards2 = tk.Frame(root, bg=col)
        otherCards2.place(relx=0.5, rely=0.1, anchor="n")
        label1 = tk.Label(otherCards2,font=hand_font, text=str(card_nums[1]), bg=col, fg=fontCol2, justify='left')
        label1.grid(row = 0, column = 0, sticky = "", pady = 2)

        if state.numOfPlayers == 4:
            fontCol3 = _if_turn(state, 2)
            otherCards3 = tk.Frame(root, bg=col)
            otherCards3.place(relx=0.9, rely=0.5, anchor="e")
            label1 = tk.Label(otherCards3,font=hand_font, text=str(card_nums[2]), bg=col, fg=fontCol3, justify='left')
            label1.grid(row = 0, column = 0, sticky = "", pady = 2)
      
    return 0

#Tells players whose turn it is currently
def _turn_info(root, state, colour):
    if state.currentPlayerTurn == state.playerID:
        msg = "It's your turn!"
    else:
        msg = f"It is now Player {state.currentPlayerTurn}'s turn."
    turn_font = tk.font.Font(family="Arial", size=24, weight=tk.NORMAL)
    label = tk.Label(root, text=msg, font=turn_font, bg=colour, fg='white', justify='left')
    label.place(relx=0.5, rely=0.6, anchor='n') 
    return

def _if_turn(state, pid):
    if state.currentPlayerTurn == pid:
        fontCol = "red"
    else:
        fontCol = "white"
    return fontCol

##DEMO RUN#
#DELETE FOR FINAL VERSION#
"""
card1 = Card(color="red", val=0, cType="1")
card2 = Card(color="blue", val=1, cType="4")
card3 = Card(color="red", val=0, cType="7")
card4 = Card(color="yellow", val=2, cType="8")
card5 = Card(color="green", val=3, cType="1")
lastCard = Card(color="yellow", val=2, cType="2")

hand = [card1, card2, card3, card4, card5]
cardNums = [5, 6, 7]    
player = Player(playerNum=1, cards=hand)
player.turn = False
player.win = False
#player.win = True
state = ClientState()
state.numOfPlayers = 4
state.lastPlayedCard =lastCard
root = tk.Tk()
#print_menu(root, 3, state)
#waiting_room(root, state)
#game_res(root, player, state)
#disconnection(root, state)
#_turn_info(root, 3, state)

print_board(root, player, state, lastCard, cardNums)

root.mainloop()

"""