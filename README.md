# Instructions

## Requirements

There are no required libraries to install and the required modules (i.e. Tkinter, Pickle, Sockets) have already been implemented within Python's prebuilt module. It is suggested to use the latest version of Python to work.

### Launch Server & Client

The server must be first opened running the command `py game_server.py` Which is then followed for the other clients running `ui_client.py` 

### How To Start

The game requires at least 2 people for the game to start. When clicking join game you will be left within a waiting room

Upon joining the game, depending on how many players are in the server the game can or can't be started
If the server recognizes that there are two players right now, it will present the option to all of the users that they can start the game

### The Game State

As soon as the button is clicked all players are put into the current game room which presents the current clients deck and how many cards the other players have where the black box indicates whos current turn it is for the other clients, the last card played and the actions a client can take

There are three screens that can pop up after the game, either a force disconnect from a user, the win or lose screen
