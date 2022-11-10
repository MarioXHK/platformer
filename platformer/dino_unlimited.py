import pygame
import random
print("Hello, Moon")
print("This takes place in the same universe as platformer")
amongst = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Dino Jumper")
doExit=False
clock = pygame.time.Clock()
#game var stufffffffffffffffffffffffffffffffffffffffffffff

isOnGround = True
vy = 0
ypos = 340
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
keys = [False, False, False, False]
pcolor = (0, 0, 0)
dead = False

#iamg
tree = pygame.image.load("tre.png")

thesky = pygame.image.load("more_orange.jpg")

dirt = pygame.image.load("dirt.jpg")

jump = pygame.mixer.Sound('jump.ogg')#load in sound effect

die = pygame.mixer.Sound('ouch.mp3')

#Scroll factors
scroll = 0
dirtpos = 0
skypos = 0
sunpos = 550
cactpos = 0
cactsize = 0
score = 0


cactrng = 0
cactonscreen = False

#gaem loop
while not doExit:
    
    for event in pygame.event.get(): #2b- i mean event queue
        if event.type == pygame.QUIT:
            doExit = True;
    
    if cactpos <= -50:
        cactonscreen = False
        cactrng = 0
    
    for i in range(round(scroll)):
        if cactrng != 100:
            cactrng = random.randrange(0, 201)
        else:
            cactonscreen = True
    
    
    
    if cactonscreen == True:
        if cactpos == -50:
            cactpos = 640
        else:
            cactpos -= scroll
    else:
        cactpos = -50
        cactsize = random.randrange(20, 100)
    
    
    #timerrrrrrrrrr
    clock.tick(60)
    dirtpos -= scroll
    skypos -= scroll/4
    #inputt5ttttttttt
    if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_UP:
                keys[UP]=True
            elif event.key == pygame.K_DOWN:
                keys[DOWN]=True
            elif event.key == pygame.K_LEFT:
                keys[LEFT]=True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
    elif event.type == pygame.KEYUP: #learn
            if event.key == pygame.K_UP:
                keys[UP]=False
            elif event.key == pygame.K_DOWN:
                keys[DOWN]=False
            elif event.key == pygame.K_LEFT:
                keys[LEFT]=False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
    
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        pygame.mixer.Sound.play(jump)
    
    if keys[RIGHT] == True:
        scroll+=0.1
    if keys[LEFT] == True:
        scroll-=0.1
    print(scroll)
    
    if ypos > 340:
        isOnGround = True
        vy = 0
        ypos = 340
    
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
    

    #collision maybe
    if ypos+60 > 400-cactsize and (cactpos < 110 and cactpos > 50):
        if dead != True:
            pygame.mixer.Sound.play(die)
        dead = True
    
    if dead != True:
        ypos+=vy
    else:
        scroll = 0
        pcolor = (255, 255, 255)
    
    
    #rendererrererer
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    
    screen.blit(thesky, (skypos, 0))
    if skypos <= -(3840-640):
        screen.blit(thesky, (skypos+3840, 0))
    if skypos+3840 <= 0:
        skypos = 0
    sunpos -= scroll/100
    pygame.draw.circle(screen, (255, 230, 50), (sunpos, 100), 50)
    
    score += round(scroll/10)
    #print(score)
    screen.blit(dirt, (dirtpos, 400))
    if dirtpos <= -(3008-640):
        screen.blit(dirt, (dirtpos+3008, 400))
    if dirtpos+3008 <= 0:
        dirtpos = 0
    if keys[DOWN] == True and dead != True:
        pygame.draw.rect(screen, pcolor, (80, ypos+30, 30, 30))
    else:
        pygame.draw.rect(screen, pcolor, (80, ypos, 30, 60))
    pygame.draw.rect(screen, (0, 120, 0), (cactpos, 400-cactsize, 30, cactsize))
    pygame.display.flip()#this actually puts the pixel on the screen
#end
pygame.quit()