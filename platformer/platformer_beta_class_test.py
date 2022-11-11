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
SHIFT = 4
REST = 5

#player variables
xpos = 300 #xpos of player
ypos = 770 #ypos of player
vx = 0 #x velocity of player
vy = 0 #y velocity of player
playaccel = 0 #umm... amogus?
leftness = True #Are you going left or right?
maxspeed = 0 #The speed limit
vloss = 0 #the height lost from the player
keys = [False, False, False, False, False, False] #this list holds whether each key has been pressed
isOnGround = False #this variable stops gravity from pulling you down more when on a platform
ducking = False
phurt = 0
dying = False
php = 3

#Level variables
level = 0
fancymovey=[200,0,0,0]
fancything=[True,True,True,True]

ewell = []

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
hurt = pygame.mixer.Sound('ouch.mp3')
die = pygame.mixer.Sound('dust.mp3')
music = pygame.mixer.music.load('music.ogg')#load in background music

#FUNCTION DEFINING-------------------------------------------------------------------

#Level parts
def makeplatform(colorr, colorg, colorb, recx, recy, rech, recv): #Makes platforms that you can stand on
    global xpos
    global ypos
    global isOnGround
    global vy
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
    global ewell
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

def echeck(irecx,irech,irecy,irecv,enumb,prtype):
    global expos
    global eypos
    global evy
    global eleftn
    global ewell
    global exsize
    global eysize
    if prtype == "platform":
        if ewell[enumb].xpos>(irecx-ewell[enumb].xsize) and ewell[enumb].xpos<(irecx+irech) and ewell[enumb].ypos +ewell[enumb].ysize >irecy and ewell[enumb].ypos+ewell[enumb].ysize <(irecy+irecv):
            if ewell[enumb].vy > 0:
                ewell[enumb].ypos = irecy-ewell[enumb].ysize
                ewell[enumb].grounded = True
                ewell[enumb].vy = 0
            if ewell[enumb].type == "smart":
                if ewell[enumb].xpos < irecx:
                    ewell[enumb].left = False
                elif ewell[enumb].xpos > (irecx+irech)-ewell[enumb].xsize:
                    ewell[enumb].left = True
    elif prtype == "wall":
        if ewell[enumb].ypos+ewell[enumb].ysize >irecy and ewell[enumb].ypos <(irecy+irecv) and ewell[enumb].xpos+exsize[enumb] >= irecx and ewell[enumb].xpos <= (irecx+irech):
            if ewell[enumb].left == True:
                ewell[enumb].left = False
            else:
                ewell[enumb].left = True
    elif prtype == "roof":
        if ewell[enumb].xpos>(irecx-exsize[enumb]) and ewell[enumb].xpos<(irecx+irech) and ewell[enumb].ypos >irecy and ewell[enumb].ypos <(irecy+irecv) and ewell[enumb].vy < 0:
            ewell[enumb].ypos = (irecy+irecv)
            ewell[enumb].vy = 0

class enemy:
    def __init__(self,type,fren = False,hurt = "none",xpos = 100,ypos = 100,xsize = 20,ysize = 20):
        self.type = type
        self.fren = fren
        self.hurt = hurt
        self.live = True
        self.xpos = xpos
        self.ypos = ypos
        self.xsize = xsize
        self.ysize = ysize
        self.left = False
        self.grounded = False
        self.vx = 0
        self.vy = 0
        if random.randrange(0, 2) == 1:
            self.left = True
    def movement(self,speed = 2):
        global xpos
        global ypos
        global vloss
        global phurt
        global php
        if self.live == True:
            if self.type == "goomb" or self.type == "smart" or self.type == "jumpy":
                if self.xpos < 0:
                    self.left = False
                elif self.xpos > (1200-self.xsize):
                    self.left = True
                if self.left == False:
                    self.xpos += speed
                else:
                    self.xpos -= speed
                if self.ypos > (800-self.ysize):
                    self.grounded = True
                    self.vy = 0
                    self.ypos = (800-self.ysize)
                if self.grounded == False:
                    self.vy+=.2
                if self.grounded == True and self.type == "jumpy":
                    self.vy = -4
                self.ypos += self.vy
            #The part where they kill you (or you kill it)
            if self.fren == False:
                if xpos>(self.xpos-20) and xpos<(self.xpos+self.xsize):
                    if ypos+40 >self.ypos and ypos+40 <(self.ypos+10) and self.hurt != "spike":
                        vy = -8
                        pygame.mixer.Sound.play(hurt)
                        if self.hurt == "multistomp" and self.ysize > 20:
                            self.ysize -= 20
                        else:
                            self.live = False
                            self.xpos = 10000
                            self.ypos = 10000
                            pygame.mixer.Sound.play(hurt)
                    elif (ypos+40 >self.ypos and ypos+(40-vloss) <=(self.ypos+self.ysize)) and phurt <= 0:
                        phurt = 100
                        php -= 1
                        if php <= 0:
                            pygame.mixer.Sound.play(die)
                        pygame.mixer.Sound.play(hurt)
    def erender(self):
        if etype == "goomb":
            pygame.draw.rect(screen, (100, 50, 0), (self.xpos, self.ypos, self.xsize, self.ysize))
        elif etype == "smart":
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, self.xsize, self.ysize))
        elif etype == "jumpy":
            pygame.draw.rect(screen, (200, 20, 2), (self.xpos, self.ypos, self.xsize, self.ysize))
        else:
            pygame.draw.rect(screen, (0, 255, 255), (self.xpos, self.ypos, self.xsize, self.ysize))
    if self.fren == False:
            pygame.draw.rect(screen, (250, 0, 0), (self.xpos, self.ypos, 10, 10))
            if ehurt == "spike":
                pygame.draw.rect(screen, (250, 0, 0), ((self.xpos+self.xsize)-10, (self.ypos+self.ysize)-10, 10, 10))
            elif ehurt == "multistomp":
                pygame.draw.rect(screen, (250, 200, 0), ((self.xpos+self.xsize)-10, (self.ypos+self.ysize)-10, 10, 10))
    else:
            pygame.draw.rect(screen, (0, 250, 0), (self.xpos, self.ypos, 10, 10))
    


#Important level things        

def treedog(xwin, ywin):
    global xpos
    global ypos
    global vx
    global vy
    global level
    screen.blit(dog, (xwin, ywin))
    if xpos>(xwin-20) and xpos<164 and ypos+40 >ywin and ypos <164 and dying == False:
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

        treedog(100, 100)
    if level == 1:
        
        makeplatform(0, 200, 100, 600, 700, 20, 20)
        
        makewall(200, 0, 0, 700, 600, 100, 100)
        
        makeplatform(0, 200, 100, 700, 590, 100, 10)
        
        makeroof(100, 50, 150, 705, 695, 90, 10)
        
        makewall(200, 0, 0, 900, 670, 100, 100)
        
        makeplatform(0, 200, 100, 900, 660, 100, 10)
        
        makeplatform(0, 200, 100, 400, 460, 200, 30)
        
        makeplatform(random.randrange(1, 20), 200, 125, 400, 400, 50, 20)
        makeroof(100, 50, 150, 905, 725, 90, 50)

        treedog(550, 100)

def levelreload(): #reload the level
    global xpos
    global ypos
    global expos
    global eypos
    global exsize
    global eysize
    global fancymovey
    global fancything
    global php
    global dying
    global vloss
    global phurt
    global elive
    phurt = 0
    php = 3
    dying = False
    vloss = 0
    if level == 0:
        xpos = 300
        ypos = 770
        fancymovey=[200,0,0,0]
        fancything=[True,True,True,True]
        ewell = [enemy("smart", True,150,550,20,20),enemy("goomb", False, "na",700,750,40,30),enemy("jumpy", True, "na",200,200,30,40),enemy("smart", False, "na", 200, 100, 30, 30),enemy("smart", True)]
    elif level == 1:
        xpos = 100
        ypos = 760
        ewell = [enemy("smart", False, "na",1080,760,20,20),enemy("smart", False, "spike",700,500,20,40),enemy("smart", False, "multistomp",20,20,20,60),enemy("smart", False, "multistomp")]

#pygame.mixer.music.play(-1)#start background music



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
            elif event.key == pygame.K_r:
                keys[REST] = True
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
            elif event.key == pygame.K_r:
                keys[REST] = False
    if dying == True:
        keys[UP] = False
        keys[DOWN] = False
        keys[LEFT] = False
        keys[RIGHT] = False
        keys[SHIFT] = False
          
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
    for eg in range(len(ewell)):
        ewell[eg].grounded = False

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
    if vy > 10:
        vy = 10
    if leftness == True:
        vx=(playaccel * -1)
    else:
        vx=playaccel
    if keys[REST] == True:
        pygame.mixer.Sound.play(die)
    
    phurt -= 2
    if phurt < -100:
        phurt = -100 #so the game doesn't overflow :D
    if php <= 0 or keys[REST] == True:
        dying = True
    if dying == True:
        vloss += 1
    if vloss >= 40:
        levelreload()
    
    for em in range(len(ewell)):
        ewell[em].movement()
    
    # RENDER Section--------------------------------------------------------------------------------
    
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    
    screen.blit(thesky, (0, 0))
    
    if winning == True:
        screen.blit(uwin, (200, 200))
    
    
    #objects
    levelmake()
    for er in range(len(ewell)):
        ewell[er].erender()
    screen.blit(dirt, (0, 800))
    
    if ducking==True:
        if vloss != 20:
            vloss += 5
    elif dying == False:
        if vloss != 0:
            vloss -= 5
    #update player position
    xpos+=vx
    ypos+=vy
    if phurt > 0:
        pygame.draw.rect(screen, (155+phurt, 0, 0), (xpos, ypos+vloss, 20, 40-vloss))
    else:
        pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos+vloss, 20, 40-vloss))
        
    pygame.display.flip()#this actually puts the pixel on the screen
    print(php)
#end game loop------------------------------------------------------------------------------
pygame.quit()