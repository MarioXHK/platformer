#INITIAL STUFF (Variables, Pygame, ect)
import pygame
import random
pygame.init()  
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((1200, 900))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

#CONSTANTS
LEFT=0
RIGHT=1
UP = 2
DOWN = 3

xpos = 600 #xpos of player
ypos = 450 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
keys = [False, False, False, False] #this list holds whether each key has been pressed


player = pygame.image.load("player_rpg.png")
player.set_colorkey((255,0,255))

#animation doo doo fard
frameWidth = 16*2
frameHeight = 32*2
RowNum = 0
frameNum = 0
ticker = 0

#ignore dis rainbiw

rainred = 255
raingreen = 0
rainblue = 0
incred = False
incgreen = False
incblue = False
decred = False
decgreen = False
decblue = False
allcolors = False

RAINBOW = (rainred,raingreen,rainblue)




while not gameover: #GAME LOOP############################################################
    clock.tick(60) #FPS
    
    #Input Section------------------------------------------------------------
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
        
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True
            elif event.key == pygame.K_DOWN:
                keys[DOWN]=True
            elif event.key == pygame.K_UP:
                keys[UP]=True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False
            elif event.key == pygame.K_UP:
                keys[UP]=False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
            elif event.key == pygame.K_DOWN:
                keys[DOWN]=False
    #movement:bangbang:
    if keys[LEFT] == True:
        vx = -3
        direction = LEFT
    elif keys[RIGHT] == True:
        vx = 3
        direction = RIGHT
    else:
        vx = 0
    
    if keys[UP] == True:
        vy = -3
        direction = UP
    elif keys[DOWN] == True:
        vy = 3
        direction = DOWN
    else:
        vy = 0
    xpos+=vx
    ypos+=vy
    
    
    #render maybe?
    
    if vx < 0:
        RowNum = 1
        ticker += 1
        if ticker%2==0:
            frameNum += 1
        if frameNum>13:
            frameNum = 2
    elif vx > 0:
        RowNum = 0
        ticker += 1
        if ticker%2==0:
            frameNum += 1
        if frameNum>13:
            frameNum = 2
    elif vy < 0:
        RowNum = 3
        ticker += 1
        if ticker%2==0:
            frameNum += 1
        if frameNum>11:
            frameNum = 0
    elif vy > 0:
        RowNum = 2
        ticker += 1
        if ticker%2==0:
            frameNum += 1
        if frameNum>11:
            frameNum = 0
    if abs(vx)+abs(vy) == 0:
        frameNum = 0
        ticker = 0
    #RAINBOW CODE!!!
    if rainred == 255 and raingreen == 0 and rainblue == 0:
        decblue = False
        incgreen = True
    if rainred == 255 and raingreen == 255 and rainblue == 0:
        decred = True
        incgreen = False
    if rainred == 0 and raingreen == 255 and rainblue == 0:
        decred = False
        incblue = True
    if rainred == 0 and raingreen == 255 and rainblue == 255:
        decgreen = True
        incblue = False
    if rainred == 0 and raingreen == 0 and rainblue == 255:
        decgreen = False
        incred = True
    if rainred == 255 and raingreen == 0 and rainblue == 255:
        decblue = True
        incred = False
    if incred == True:
        rainred += 1
    if decred == True:
        rainred -= 1
    if incgreen == True:
        raingreen += 1
    if decgreen == True:
        raingreen -= 1
    if incblue == True:
        rainblue += 1
    if decblue == True:
        rainblue -= 1
    RAINBOW = (rainred,raingreen,rainblue)
    
    #Nah, this is the rendering!
    
    screen.fill((RAINBOW))
    screen.blit(player, (xpos, ypos), (frameWidth*frameNum, RowNum*frameHeight, frameWidth, frameHeight))
    pygame.display.flip()
pygame.quit()