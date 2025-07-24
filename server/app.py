# Example file showing a basic pygame "game loop"
import pygame
import pygame_widgets
from pygame_widgets.button import Button,ButtonArray
from gameState import GameState
from entities import Card
from operator import attrgetter

currGame = GameState(4)

def getCardCalled(card: int):
    print(card)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
cardX = 0
cardY = 0
offsetX = 120
offsetY = 120
cards = []
cardFunc = []
cardText = []
numOfPlayers = 3
for i in range(7):
    cardIter = pygame.Rect(cardX,cardY,100,200)
    cardX += offsetX
    cards.append(cardIter)
    currCard = currGame.players[0].cards[i]
    cardFunc.append(lambda: getCardCalled(currCard.val))
    cardText.append(str(currCard.val))

print(cardFunc)

buttonArr = ButtonArray(win=screen,x=0,y=0,width=500,height=500,shape=(7,1),texts=tuple(cardText),onClicks=cardFunc)

# button = pygame_widgets.button.Button(screen,100,100,300,150,text = "Test", fontSize = 50,onClick = lambda: print('HELLLOOO'))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    
    for i in range(len(cards)):
        pygame.draw.rect(screen,currGame.players[0].cards[i].color,cards[i])

    # RENDER YOUR GAME HERE

    clock.tick(100)  # limits FPS to 60
    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()

pygame.quit()