#INITIAL STUFF (Variables, Pygame, ect)
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
ducking = False



#enemy variables
expos = [150,700,200]
eypos = [550,750,200]
evx = [0,0,0]
evy = [0,0,0]
enaccel = [0,0,0]
exsize = [20, 40, 30]
eysize = [20, 30, 40]
eleftn = [False,False,False]
eground = [False,False,False]
ewell = ["goomb","goomb","goomb"]

#Level variables
level = 0
fancymovey=[200,0,0,0]
fancything=[True,True,True,True]


#win?
winning = False

#Images
pygame.display.set_caption('adding images')

dog = pygame.image.load("tre.png")

thesky = pygame.image.load("more_orange.jpg")

uwin = pygame.image.load("you_win.png")

dirt = pygame.image.load("dirt.jpg")

#Sounds
jump = pygame.mixer.Sound('jump.ogg')#load in sound effect
music = pygame.mixer.music.load('music.ogg')#load in background music

#FUNCTION DEFINING-------------------------------------------------------------------

#Ez ifs
def echeck(irecx,irech,irecy,irecv,enumb,prtype):
    global expos
    global eypos
    global evy
    global eleftn
    global ewell
    global exsize
    global eysize
    if prtype == "platform":
        if expos[enumb]>(irecx-exsize[enumb]) and expos[enumb]<(irecx+irech) and eypos[enumb]+eysize[enumb] >irecy and eypos[enumb]+eysize[enumb] <(irecy+irecv):
            if evy[enumb] > 0:
                eypos[enumb] = irecy-eysize[enumb]
                eground[enumb] = True
                evy[enumb] = 0
            if ewell[enumb] == "smart":
                if expos[enumb] < irecx:
                    eleftn[enumb] = False
                elif expos[enumb] > (irecx+irech)-exsize[enumb]:
                    eleftn[enumb] = True
    elif prtype == "wall":
        if eypos[enumb]+eysize[enumb] >irecy and eypos[enumb] <(irecy+irecv) and expos[enumb]+exsize[enumb] >= irecx and expos[enumb] <= (irecx+irech):
            if eleftn[enumb] == True:
                eleftn[enumb] = False
            else:
                eleftn[enumb] = True
    elif prtype == "roof":
        if expos[enumb]>(irecx-exsize[enumb]) and expos[enumb]<(irecx+irech) and eypos[enumb] >irecy and eypos[enumb] <(irecy+irecv) and evy[enumb] < 0:
            eypos[enumb] = (irecy+irecv)
            evy[enumb] = 0


def levelreload(): #reload the level
    global xpos
    global ypos
    global expos
    global eypos
    global fancymovey
    global fancything
    if level == 0:
        xpos = 350
        ypos = 770
        expos = [150,700,200]
        eypos = [550,750,200]
        fancymovey=[200,0,0,0]
        fancything=[True,True,True,True]
        exsize = [20, 40, 30]
        eysize = [20, 30, 40]
    elif level == 1:
        xpos = 100
        ypos = 760
        expos = [1080, 700, 0]
        eypos = [760, 500, 0]
        exsize = [20, 20, 20]
        eysize = [20, 20, 20]


#Level parts
def makeplatform(colorr, colorg, colorb, recx, recy, rech, recv): #Makes platforms that you can stand on
    global xpos
    global ypos
    global isOnGround
    global vy
    global expos
    global eypos
    global evy
    global eleftn
    global ewell
    pygame.draw.rect(screen, (colorr, colorg, colorb), (recx, recy, rech, recv))
    if xpos>(recx-20) and xpos<(recx+rech) and ypos+40 >recy and ypos+40 <(recy+recv):
        if vy > 0:
            ypos = recy-40
            isOnGround = True
            vy = 0
    for i in range(len(ewell)):
        echeck(recx,rech,recy,recv,i,"platform")
        
                
def makemovingvert(movenum, colorr, colorg, colorb, recx, recy, rech, recv, newy): #Makes vertical moving platforms that you can stand on
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


def makewall(colorr, colorg, colorb, recx, recy, rech, recv): #Makes walls that you can't pass through
    global xpos
    global ypos
    global vx
    global keys
    global playaccel
    global expos
    global eypos
    pygame.draw.rect(screen, (colorr, colorg, colorb), (recx, recy, rech, recv))
    if ypos+40 >recy and ypos+vloss <(recy+recv) and xpos+20 >= recx and xpos <= (recx+rech): #making sure to account for ducking
        playaccel = 0
        if xpos < recx:
            xpos = recx-20
            if keys[LEFT] == False:
                vx = 0
        else:
            xpos = recx+rech
            if keys[RIGHT] == False:
                vx = 0
    for i in range(len(ewell)):
        echeck(recx,rech,recy,recv,i,"wall")
        
def makeroof(colorr, colorg, colorb, recx, recy, rech, recv): #Makes roofs that you can't jump through
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
        if recy+recv > ypos and ypos > recy:
            ducking = True
    for i in range(len(ewell)):
        echeck(recx,rech,recy,recv,i,"roof")
#Enemy stuff
def ephysic(ienum): #because yes
    global expos
    global eypos
    global eleftn
    global enaccel
    global evx
    global evy
    global ewell
    global exsize
    global eysize
    if expos[ienum] < 0 or expos[ienum] > (1200-exsize[ienum]):
        if expos[ienum] < 0:
            eleftn[ienum] = False
        else:
            eleftn[ienum] = True
        if ewell[ienum] == "clone":
            enaccel[ienum] = 0
    if eypos[ienum] > (800-eysize[ienum]):
        eground[ienum] = True
        evy[ienum] = 0
        eypos[ienum] = (800-eysize[ienum])
    if eground[ienum] == False:
        evy[ienum]+=.2

def enemy(enum,etype): #Makes something to fight
    global expos
    global eypos
    global eleftn
    global enaccel
    global evx
    global evy
    global ewell
    global exsize
    global eysize
    global vx
    global vy
    global vloss
    global maxspeed
    ewell[enum] = etype
    if etype == "goomb" or etype == "smart" or etype == "jumpy":
        if eleftn[enum] == False:
            expos[enum] += 2
        else:
            expos[enum] -= 2
        ephysic(enum)
        if eground[enum] == True and etype == "jumpy":
            evy[enum] = -4
        eypos[enum] += evy[enum]
        if etype == "goomb":
            pygame.draw.rect(screen, (100, 50, 0), (expos[enum], eypos[enum], exsize[enum], eysize[enum]))
        elif etype == "smart":
            pygame.draw.rect(screen, (250, 250, 250), (expos[enum], eypos[enum], exsize[enum], eysize[enum]))
        elif etype == "jumpy":
            pygame.draw.rect(screen, (200, 20, 2), (expos[enum], eypos[enum], exsize[enum], eysize[enum]))
        else:
            pygame.draw.rect(screen, (0, 255, 255), (expos[enum], eypos[enum], exsize[enum], eysize[enum]))
    elif etype == "clone": #challenge to make an enemy clone
        exsize[enum] = 20
        eysize[enum] = 40-vloss
        if keys[LEFT]==True:
            if evx[enum] > 0:
                enaccel[enum] -= 0.5
            else:
                enaccel[enum] += 0.5
                eleftn[enum] = True
        elif keys[RIGHT]==True:
            if evx[enum] < 0:
                enaccel[enum] -= 0.5
            else:
                enaccel[enum] += 0.5
                eleftn[enum] = False
        else:
            enaccel[enum] -= 0.5
        #turn off velocity
        if enaccel[enum] < 0:
            enaccel[enum] = 0
        if enaccel[enum] > maxspeed:
            enaccel[enum] = maxspeed
            #JUMPING
        ephysic(enum)
        if keys[UP] == True and eground[enum] == True: #only jump when on the ground
            evy[enum] = -8
            eground[enum] = False
            pygame.mixer.Sound.play(jump)
        if keys[UP] == False and evy[enum] < -2: #Jump cancel
            evy[enum] = -2
        if eleftn[enum] == True:
            evx[enum]=(enaccel[enum] * -1)
        else:
            evx[enum]=enaccel[enum]
        expos[enum] += evx[enum]
        eypos[enum] += evy[enum]
        pygame.draw.rect(screen, (50, 100, 50), (expos[enum], eypos[enum]+vloss, 20, 40-vloss))
        
#Important level things        

def treedog(xwin, ywin):
    global xpos
    global ypos
    global vx
    global vy
    global level
    screen.blit(dog, (xwin, ywin))
    if xpos>(xwin-20) and xpos<164 and ypos+40 >ywin and ypos <164:
        level =+ 1
        vx = 0
        vy = 0
        levelreload()
        print(level)

def levelmake(): #Makes the level
    global level
    if level == 0:
        makeplatform(200, 0, 100, 100, 750, 100, 20)
    
        makeplatform(100, 0, 200, 200, 650, 100, 20)
        
        makeplatform(100, 200, 50, 150, 600, 100, 20)
        
        makeplatform(200, 100, 0, 700, 600, 100, 20)
        
        pygame.draw.line(screen, (0, 0, 0,), (700, 600),(800, 600), width=5)
        
        makemovingvert(0, 0, 50, 200, 800, 200, 100, 20, 500)
        
        makeplatform(0, 200, 150, 300, 300, 100, 20)
        
        makeplatform(200, 0, 0, 100, 164, 64, 10)
        
        makewall(200, 0, 0, 700, 670, 20, 100)
        
        makewall(200, 0, 0, 1000, 750, 10, 50)
        
        makeroof(100, 0, 200, 500, 660, 50, 50)
        
        makeroof(100, 50, 150, 300, 725, 100, 50)

        enemy(0, "smart")
        enemy(1, "goomb")
        enemy(2, "jumpy")
        treedog(100, 100)
    if level == 1:
        
        makeplatform(0, 200, 100, 600, 700, 20, 20)
        
        makewall(200, 0, 0, 700, 600, 100, 100)
        
        makeplatform(0, 200, 100, 700, 590, 100, 10)
        
        makeroof(100, 50, 150, 705, 695, 90, 10)
        
        makewall(200, 0, 0, 900, 670, 100, 100)
        
        makeplatform(0, 200, 100, 900, 660, 100, 10)
        
        makeroof(100, 50, 150, 905, 725, 90, 50)
        enemy(0, "smart")
        enemy(1, "smart")
        enemy(2, "smart")
        treedog(550, 100)
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
    
    if keys[UP] == False and vy < -2: #Jump cancel
        vy = -2
    
    
    #COLLISION

    isOnGround = False
    eground = [False,False,False]

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
    
    if winning == True:
        screen.blit(uwin, (200, 200))
    
    
    #objects
    levelmake()
    
    
    screen.blit(dirt, (0, 800))
    
    if ducking==True:
        if vloss != 20:
            vloss += 5
    else:
        if vloss != 0:
            vloss -= 5
    #update player position
    xpos+=vx
    ypos+=vy
    pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos+vloss, 20, 40-vloss))
    pygame.display.flip()#this actually puts the pixel on the screen
#end game loop------------------------------------------------------------------------------
pygame.quit()