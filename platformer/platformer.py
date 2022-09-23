import pygame
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
SHIFT = 4

playaccel = 0
leftness = True
maxspeed = 0
#player variables
xpos = 500 #xpos of player
ypos = 200 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
keys = [False, False, False, False, False] #this list holds whether each key has been pressed
isOnGround = False #this variable stops gravity from pulling you down more when on a platform


def makeplatform(colorr, colorg, colorb, recx, recy, rech, recv):
    global xpos
    global ypos
    global isOnGround
    global vy
    pygame.draw.rect(screen, (colorr, colorg, colorb), (recx, recy, rech, recv))
    if xpos>(recx-20) and xpos<(recx+rech) and ypos+40 >recy and ypos+40 <(recy+recv):
        if vy > 0:
            ypos = recy-40
            isOnGround = True
            vy = 0
fancymovey=[200,0,0,0]
fancything=[True,True,True,True]
def makemovingvert(movenum, colorr, colorg, colorb, recx, recy, rech, recv, newy):
    global fancymovey
    global fancything
    makeplatform(colorr, colorg, colorb, recx, fancymovey[movenum], rech, recv)
    if fancymovey[movenum] == recy:
        fancything[movenum] = False
    if fancymovey[movenum] == newy:
        fancything[movenum] = True
    if fancything[movenum] == False:
        fancymovey[movenum] += 2
    if fancything[movenum] == True:
        fancymovey[movenum] -= 2





winning = False

pygame.display.set_caption('adding images')

dog = pygame.image.load("tre.png")

thesky = pygame.image.load("more_orange.jpg")

uwin = pygame.image.load("you_win.png")

dirt = pygame.image.load("dirt.jpg")



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
            elif event.key == pygame.K_LSHIFT:
                keys[SHIFT]=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False

            elif event.key == pygame.K_UP:
                keys[UP]=False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
            elif event.key == pygame.K_LSHIFT:
                keys[SHIFT]=False
            elif event.key == pygame.K_DOWN:
                keys[DOWN]=False
        
          
    #physics section--------------------------------------------------------------------
    #MOVEMENT
    vx=playaccel
    if keys[SHIFT]==True and keys[DOWN]==False:
        maxspeed = 6
    else:
        maxspeed = 3
    if keys[LEFT]==True:
        if (maxspeed * -1) < playaccel:
            playaccel -= 0.5
        elif (maxspeed * -1) > playaccel:
            playaccel += 0.5
        if vx < 0:
            leftness = True
        direction = LEFT
    elif keys[RIGHT]==True:
        if maxspeed > playaccel:
            playaccel += 0.5
        elif maxspeed < playaccel:
            playaccel -= 0.5
        if vx > 0:
            leftness = False
        direction = RIGHT

    #turn off velocity
    else:
        if vx != 0:
            if leftness == True:
                playaccel += 0.5
            else:
                playaccel -= 0.5
        
        #JUMPING
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        direction = UP
    
    

    
    #COLLISION
    if xpos>130 and xpos<250 and ypos+40 >600 and ypos+40 <620:
        ypos = 600-40
        isOnGround = True
        vy = 0
    elif xpos>130 and xpos<250 and ypos+40 >600 and ypos+40 <620:
        ypos = 600-40
        isOnGround = True
        vy = 0
    else:
        isOnGround = False
    
    if xpos>80 and xpos<164 and ypos+40 >100 and ypos <164:
        winning = True

    
    #stop falling if on bottom of game screen
    if ypos > 760:
        isOnGround = True
        vy = 0
        ypos = 760
    
    #gravity
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
    

    #update player position
    xpos+=vx 
    ypos+=vy
    
  
    # RENDER Section--------------------------------------------------------------------------------
    
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    
    screen.blit(thesky, (0, 0))
    
    screen.blit(dog, (100, 100))
    
    if winning == True:
        screen.blit(uwin, (200, 200))
    if keys[DOWN]==True:
        pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos+20, 20, 20))
    else:
        pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos, 20, 40))
    
    
    #platforms
    makeplatform(200, 0, 100, 100, 750, 100, 20)
    
    makeplatform(100, 0, 200, 200, 650, 100, 20)
    
    makeplatform(100, 200, 50, 150, 600, 100, 20)
    
    makeplatform(200, 100, 0, 700, 600, 100, 20)
    
    pygame.draw.line(screen, (0, 0, 0,), (700, 600),(800, 600), width=5)
    
    makemovingvert(0, 0, 50, 200, 800, 200, 100, 20, 500)
    
    makeplatform(0, 200, 150, 300, 300, 100, 20)
    
    makeplatform(200, 0, 0, 100, 164, 64, 10)
    
    screen.blit(dirt, (0, 800))
    
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()