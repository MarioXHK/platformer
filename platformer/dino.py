import pygame

print("Hello, Moon")
print("This takes place in the same universe as platformer")
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
keys = [False, False]

#iamg
tree = pygame.image.load("tre.png")

thesky = pygame.image.load("more_orange.jpg")

dirt = pygame.image.load("dirt.jpg")

jump = pygame.mixer.Sound('jump.ogg')#load in sound effect

scroll = 10
dirtpos = 0
skypos = 0
#gaem loop
while not doExit:
    
    for event in pygame.event.get(): #2b- i mean event queue
        if event.type == pygame.QUIT:
            doExit = True;
    
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
    elif event.type == pygame.KEYUP: #learn
            if event.key == pygame.K_UP:
                keys[UP]=False
            elif event.key == pygame.K_DOWN:
                keys[DOWN]=False
    
    if keys[UP] == True and isOnGround == True: #only jump when on the ground
        vy = -8
        isOnGround = False
        pygame.mixer.Sound.play(jump)
    
    
    if ypos > 340:
        isOnGround = True
        vy = 0
        ypos = 340
    
    if isOnGround == False:
        vy+=.2 #notice this grows over time, aka ACCELERATION
    
    ypos+=vy
    #rendererrererer
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
    
    screen.blit(thesky, (skypos, 0))
    if skypos <= -(3840-640):
        screen.blit(thesky, (skypos+3840, 0))
    if skypos+3840 <= 0:
        skypos = 0
    
    screen.blit(dirt, (dirtpos, 400))
    if dirtpos <= -(3008-640):
        screen.blit(dirt, (dirtpos+3008, 400))
    if dirtpos+3008 <= 0:
        dirtpos = 0
    if keys[DOWN] == True:
        pygame.draw.rect(screen, (0, 0, 0), (80, ypos+30, 30, 30))
    else:
        pygame.draw.rect(screen, (0, 0, 0), (80, ypos, 30, 60))
    
    pygame.display.flip()#this actually puts the pixel on the screen
#end
pygame.quit()