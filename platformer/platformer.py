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

ducking = False

#player variables
xpos = 350 #xpos of player
ypos = 770 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
playaccel = 0 #umm... amogus?
leftness = True #Are you going left or right?
maxspeed = 0 #The speed limit
vloss = 0 #the height lost from the player
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


def makewall(colorr, colorg, colorb, recx, recy, rech, recv):
    global xpos
    global ypos
    global vx
    global keys
    global playaccel
    pygame.draw.rect(screen, (colorr, colorg, colorb), (recx, recy, rech, recv))
    if ypos+40 >recy and ypos+vloss <(recy+recv) and xpos+20 >= recx and xpos <= (recx+rech):
        playaccel = 0
        if xpos < recx:
            xpos = recx-20
            if keys[LEFT] == False:
                vx = 0
        else:
            xpos = recx+rech
            if keys[RIGHT] == False:
                vx = 0
        
def makeroof(colorr, colorg, colorb, recx, recy, rech, recv):
    global xpos
    global ypos
    global isOnGround
    global vy
    global vloss
    global ducking
    pygame.draw.rect(screen, (colorr, colorg, colorb), (recx, recy, rech, recv))
    if xpos>(recx-20) and xpos<(recx+rech):
        if ypos+vloss >recy and ypos+vloss <(recy+recv):
            if vy < 0:
                ypos = (recy+recv)-vloss
                vy = 0
        if recy+recv > ypos and isOnGround == True:
            ducking = True
        
            


winning = False

pygame.display.set_caption('adding images')

dog = pygame.image.load("tre.png")

thesky = pygame.image.load("more_orange.jpg")

uwin = pygame.image.load("you_win.png")

dirt = pygame.image.load("dirt.jpg")


#SOUND--------------------------------------------------------------------
jump = pygame.mixer.Sound('jump.ogg')#load in sound effect
music = pygame.mixer.music.load('music.ogg')#load in background music
pygame.mixer.music.play(-1)#start background music
#-------------------------------------------------------------------------


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
    ducking = False
                
    if keys[SHIFT]==True and vloss < 10:
        maxspeed = 6
    else:
        maxspeed = 3
    if keys[LEFT]==True:
        if vx > 0:
            playaccel -= 0.5
        else:
            playaccel += 0.5
            leftness = True
        direction = LEFT
    elif keys[RIGHT]==True:
        if vx < 0:
            playaccel -= 0.5
        else:
            playaccel += 0.5
            leftness = False
        direction = RIGHT
    else:
        playaccel -= 0.5
    #turn off velocity
    if playaccel < 0:
        playaccel = 0
    if playaccel > maxspeed:
        playaccel = maxspeed
        #JUMPING
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        direction = UP
        pygame.mixer.Sound.play(jump)
    if keys[DOWN]==True:
        ducking=True
    
    
    
    
    #COLLISION

    isOnGround = False
    
    
    if xpos>80 and xpos<164 and ypos+40 >100 and ypos <164:
        winning = True

    if xpos < 0:
        xpos = 0
        playaccel = 0
    elif xpos > 1180:
        xpos = 1180
        playaccel = 0
    #stop falling if on bottom of game screen
    if ypos > 760:
        isOnGround = True
        vy = 0
        ypos = 760
    
    #gravity
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
    
    if leftness == True:
        vx=(playaccel * -1)
    else:
        vx=playaccel
    
    
  
    # RENDER Section--------------------------------------------------------------------------------
    
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    
    screen.blit(thesky, (0, 0))
    
    screen.blit(dog, (100, 100))
    
    if winning == True:
        screen.blit(uwin, (200, 200))
    
    
    #objects
    makeplatform(200, 0, 100, 100, 750, 100, 20)
    
    makeplatform(100, 0, 200, 200, 650, 100, 20)
    
    makeplatform(100, 200, 50, 150, 600, 100, 20)
    
    makeplatform(200, 100, 0, 700, 600, 100, 20)
    
    pygame.draw.line(screen, (0, 0, 0,), (700, 600),(800, 600), width=5)
    
    makemovingvert(0, 0, 50, 200, 800, 200, 100, 20, 500)
    
    makeplatform(0, 200, 150, 300, 300, 100, 20)
    
    makeplatform(200, 0, 0, 100, 164, 64, 10)
    
    makewall(200, 0, 0, 700, 670, 20, 100)
    
    makeroof(100, 0, 200, 500, 660, 50, 50)
    
    makeroof(100, 50, 150, 300, 725, 100, 50)
    
    screen.blit(dirt, (0, 800))
    
    if ducking==True:
        vloss = 20
    else:
        vloss = 0
    #update player position
    xpos+=vx
    ypos+=vy
    pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos+vloss, 20, 40-vloss))
    pygame.display.flip()#this actually puts the pixel on the screen
    print (isOnGround)
#end game loop------------------------------------------------------------------------------
pygame.quit()