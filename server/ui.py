import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from clientState import *
from entities import *
from tkinter import PhotoImage

"""
Main GUI Functions

--How to use:
a) import this file (ui.py) in file where graphic are called
b) At each iteration of game loop, call the appropriate public gui function
(ie print_menu(), print_board(), print_result(), waiting_room(), 
disconnection(), print_credits(), print_instrcutions() etc with appropriate args)
c) Upon button clicks, Click class is modified so that server can interpret
the button click and change gameState/playerState information and resend
so that ui can continuously be updated
"""

##prints menu
##args: root --> root screen
## clk: tracks button clicks
def print_menu(root, clk):
    _screen_set_up(root, "Main Menu", "Verdana", "light yellow")
    menu_font = tkFont.Font(family="Verdana", size=32, weight=tk.NORMAL)

    msg = "__uno__ "
    title = tk.Label(root, text=msg, font=("Helvetica", 100, "bold", "italic"), bg='tan1', fg='red3')
    title.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    #frame for menu
    frame = tk.Frame(root, bg="light yellow")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 

    join_game = tk.Button(frame, text="Join Game", font=menu_font, command=lambda: clk.clicked('joinedWaitingRoom'))
    join_game.grid(row = 0, column = 0, sticky = W, pady = 5)
    instructions = tk.Button(frame, text="Instructions", font=menu_font, command=lambda: clk.clicked('instructions'))
    instructions.grid(row = 1, column = 0, sticky = W, pady = 5)
    credits = tk.Button(frame, text="Credits", font=menu_font, command=lambda: clk.clicked('credits'))
    credits.grid(row = 2, column = 0, sticky = W, pady = 5)

    return 

#This is the screen players see while waiting for others to join ganme
#Need at least two players to manually start game
def waiting_room(root, numPlayers, clk):
    _screen_set_up(root, "Waiting Room", "Verdana", "tan1")
    wait_font = tkFont.Font(family="Verdana", size=24, weight=tk.NORMAL)
    frame = tk.Frame(root, bg="tan1")
    frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER) 

    msg = f"\nThere is currently {numPlayers} enrolled."
    label = tk.Label(frame, text=msg, font=wait_font, bg='tan1', fg='white', justify='left')
    label.grid(row = 0, column = 0, sticky = "", pady = 2)
    if numPlayers > 1:     
        start = tk.Button(frame, text="Start!", font=wait_font, command=lambda: clk.clicked('startGame'))
        start.grid(row=2, column=0, sticky = "", pady = 40)
    return

#player: instance of player class
#state: current state of game from players
# lastCard -- last card played, passed separately for clarity
# card_nums: a list of 1,2, 0r 3 elements where card_nums[i] 
# corresponds to the number of cards player(i) has 
#clk: tracks user clicks

def print_board(root, player, currTurn, lastCard, card_nums, numPlayers, clk):
    screen_col = "deep sky blue"
    main_font = tk.font.Font(family="Arial", size=24, weight=tk.NORMAL)
    _screen_set_up(root, "Main Game", main_font, screen_col)
    _turn_info(root, currTurn, player.playerNum, screen_col)

    #print "face down deck" in centre
    frameCentre = tk.Frame(root, bg=screen_col)
    frameCentre.place(relx=0.5, rely=0.4, anchor="center")  
    deck = tk.Label(frameCentre, text="Deck", font=("Helvetica", 14), bg="grey50", fg='white', justify='left', width=5, height=5)
    deck.grid(row = 0, column = 1, sticky = "", pady = 2, padx=8)
    #print last card played
    prevCard = tk.Label(frameCentre, bg=lastCard.color, text=lastCard.type, font=("Helvetica", 34), fg='grey69', width=2, height=2)
    prevCard.grid(row = 0, column = 0, sticky = "", pady = 10, padx=8)
    #print draw card button:
    drawCardBtn = tk.Button(frameCentre, text="Draw\n card", font=("Helvetica", 20), command=lambda: clk.clicked('drawCard'))
    drawCardBtn.grid(row=0, column=2, sticky = "", padx=8)
    drawUnoBtn = tk.Button(frameCentre, text="UNO!", font=("Helvetica", 20), command=lambda: clk.clicked('uno'))
    drawUnoBtn.grid(row=1, column=2, sticky = "", padx=8)
    
    _print_hands(root, numPlayers, player,card_nums, currTurn, screen_col, clk)

    return

#Displays winner/loser screen when game concludes
#@: root --> screen to display, 
#@: win: true if player won
def game_res(root, win, clk):
    if win == True:
        _you_win(root)
    else:
        _you_lose(root)
    btn = tk.Button(root, text="Play Again", font=("Helvetica", 32), command=lambda: clk.clicked('joinWaitingRoom'))
    btn.grid(row = 2, column = 1)

#displays error when disconnection occurs suddenly
#@: root --> screen to display
#@ clk -->tracks user button clicks
def disconnection(root, clk):
    _clear_screen(root)
    root.title("ERROR")
    root.configure(bg="red")
    root.geometry("600x600")
    msg = "Someone has disconnected so\n the game is now over :("
    err = tk.Label(root, text=msg, font=("Helvetica", 32), bg="red", fg="white")
    err.grid(row = 1, column = 1, sticky = "ew", pady = 100, padx = 90)
    btn = tk.Button(root, text="Play Again", font=("Helvetica", 32), command=lambda: clk.clicked('joinWaitingRoom'))
    btn.grid(row = 2, column = 1)

    ##credits found from main menu
def print_credits(root, num_players, clk):
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

    back_button = tk.Button(frame, text="Back", font=creds_font, command=lambda: clk.clicked('menu'))
    back_button.grid(row = 1, column = 0, sticky = W, pady = 2)
    return 0

#game instrcutions found at main menu
def print_instructions(root, num_players, clk):
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

    back_button = tk.Button(frame, text="Back", font=instr_font, command=lambda: clk.clicked('menu'))
    back_button.grid(row = 1, column = 0, sticky = W, pady = 2)
    return 0

"""
Private Helper Functions
"""

def _clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

def _screen_set_up(root, heading, font, colour):
    _clear_screen(root)
    root.title(heading)
    root.geometry('600x600')
    root.configure(bg=colour)
    menu_font = tkFont.Font(family=font, size=24, weight=tk.NORMAL)

#screen user sees upon winning
def _you_win(root):
    root.title("Winner!")
    root.configure(bg="green2")
    root.geometry("600x600")
    win = tk.Label(root, text="YOU WIN!!!!!!", font=("Helvetica", 64), bg="green2", fg="white")
    win.grid(row = 1, column = 1, sticky = "ew", pady = 100, padx = 80)
    return 

#screen user sees upon losing
def _you_lose(root):
    root.title("Loser!")
    root.configure(bg="orange red")
    root.geometry("600x600")
    lose = tk.Label(root, text="YOU LOSE!!!!!", font=("Helvetica", 64), bg="orange red", fg="white")
    lose.grid(row = 1, column = 1, sticky = "ew", pady = 100, padx = 80)
    return 

#print all cards at bottom of screen
#root: main screen
#numPlayers: number of players in game
#player class
#card_nums: list containing number of cards each player has
#card_num[i] stores the number of cards player(i) has
#currTurn: corresponds to the playerid of whose turn it is
#col: background colour for screen
#clk: stores user button clicks
def _print_hands(root, numPlayers, player, card_nums, currTurn, col, clk):
    hand_font = tkFont.Font(family="Helvetica", size=45)
    opponent_font = tkFont.Font(family="Helvetica", size=52)
    #print user's own cards
    frameSelf = tk.Frame(root, bg=col)
    frameSelf.place(relx=0.5, rely=0.9, anchor="s")  
    for idx, currCard in enumerate(player.cards):
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
            lambda: clk.clicked(('hand', idx))
        )

        pseudoBtn.bind("<Enter>", lambda e, btn=pseudoBtn: btn.config(bg="white", fg="black"))
        pseudoBtn.bind("<Leave>", lambda e, btn=pseudoBtn, col=currCard.color.lower(): btn.config(bg=col, fg="gray48"))
        pseudoBtn.grid(row = 0, column = idx, padx=4)

    ##print number of cards across screen of opponents
    nextPlayer = (player.playerNum + 1)% numPlayers
    if numPlayers == 2:
        cols = _if_turn(currTurn, nextPlayer)
        otherCards1 = tk.Frame(root, bg=col)
        otherCards1.place(relx=0.5, rely=0.1, anchor="n")
        label1 = tk.Label(otherCards1, font=opponent_font, text=str(card_nums[nextPlayer]), bg=cols[1], fg=cols[0], justify='left')
        label1.grid(row = 0, column = 0, sticky = "", pady = 2)
    else:
        cols1 = _if_turn(currTurn, nextPlayer)
        otherCards1 = tk.Frame(root, bg=col)
        otherCards1.place(relx=0.1, rely=0.5, anchor="w")
        label1 = tk.Label(otherCards1,font=opponent_font, text=str(card_nums[nextPlayer]), bg=cols1[1], fg=cols1[0], justify='left')
        label1.grid(row = 0, column = 0, sticky = "", pady = 2)

        nextPlayerx2 = (player.playerNum + 2)% numPlayers
        cols2 = _if_turn(currTurn, nextPlayerx2)
        otherCards2 = tk.Frame(root, bg=col)
        otherCards2.place(relx=0.5, rely=0.1, anchor="n")
        label1 = tk.Label(otherCards2,font=opponent_font, text=str(card_nums[nextPlayerx2]), bg=cols2[1], fg=cols2[0], justify='left')
        label1.grid(row = 0, column = 0, sticky = "", pady = 2)

        if numPlayers == 4:
            nextPlayerx3 = (player.playerNum + 3)% numPlayers
            cols3 = _if_turn(currTurn, nextPlayerx3 )
            otherCards3 = tk.Frame(root, bg=col)
            otherCards3.place(relx=0.9, rely=0.5, anchor="e")
            label1 = tk.Label(otherCards3,font=opponent_font, text=str(card_nums[nextPlayerx3 ]), bg=cols3[1], fg=cols3[0], justify='left')
            label1.grid(row = 0, column = 0, sticky = "", pady = 2)
    return 0

#Tells players whose turn it is currently
#currPlayerTurn: the player id of the player whose turn it is currently
#playID: the playerID of the player seeing the screen
def _turn_info(root, currPlayerTurn, playID, colour):
    if currPlayerTurn == playID:
        msg = "It's your turn!"
    else:
        msg = f"It is now Player {currPlayerTurn}'s turn."
    turn_font = tk.font.Font(family="Arial", size=24, weight=tk.NORMAL)
    label = tk.Label(root, text=msg, font=turn_font, bg=colour, fg='white', justify='left')
    label.place(relx=0.5, rely=0.6, anchor='n') 
    return

#If it is an opponent's turn, (currTurn == pid) the number of cards 
# they have lights up red
#Otherwise, it is white
def _if_turn(currTurn, pid):
    if currTurn == pid:
        fontCol = "red"
        cardCol = "black"
    else:
        fontCol = "white"
        cardCol = "grey69"
    return (fontCol, cardCol)

##DEMO RUN#
#DELETE FOR FINAL VERSION#

"""

clk = Click()
root = tk.Tk()

#waiting_room(root, 6, clk)
#game_res(root, False, clk)
#print_menu(root, clk)

card1 = Card(color="red", val=0, cType="1")
card2 = Card(color="blue", val=1, cType="4")
card3 = Card(color="red", val=0, cType="7")
card4 = Card(color="yellow", val=2, cType="8")
card5 = Card(color="green", val=3, cType="1")
lastCard = Card(color="yellow", val=2, cType="2")

hand = [card1, card2, card3, card4, card5]
cardNums = [5, 1, 4, 9]    
player = Player(playerNum=2, cards=hand)
player.turn = False
player.win = False

currTurn = 0
numOfPlayers = 4
lastPlayedCard =lastCard

print_board(root, player, currTurn, lastPlayedCard, cardNums, numOfPlayers, clk)
root.mainloop()

"""



