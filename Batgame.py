import pygame, random, sys, time
from pygame.locals import *

#setting up variables
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
TEXTCOLOR = (218, 231, 218)
BACKGROUNDCOLOR = (151,159,234)
FPS = 30
BADDIEMINSIZE = 50
BADDIEMAXSIZE = 90
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 12
PLAYERMOVERATE = 10
wormsize = 40
clock = pygame.time.Clock()
bat = 0 #default black , 0 for black , 1 for white

flies_hunt = 0
total = 0
#Colors
White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Green = (0,155,0)
Blue = (0,0,255)
Grey = (182,183,174)
Navy = (128,128,254)
Parrot = (121,242,236)
Silver = (218,231,218)
LBlack = (21,21,21)
Tb = (0,0,0)
Tw = (218,231,218)


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                if event.key == pygame.K_q:
                       terminate()
                if event.key == pygame.K_b:
                    pygame.mouse.set_visible(True)

                    gameOverSound.stop()
                    gameBeginSound.play(-1)
                    bcscreen()
                if event.key == pygame.K_r:
                    gameOverSound.stop()
                    global bat
                    if bat == 1:
                        [playerRect,playerImage,bg] = Load_BATandBG('batsilver.png','bgforwhite.jpg')
                        gameloop(playerRect,playerImage,bg)
                    else:
                        #global TEXTCOLOR
                        #TEXTCOLOR = (0,0,0)
                        [playerRect,playerImage,bg] = Load_BATandBG('bat.png','bg.jpg')
                        gameloop(playerRect,playerImage,bg)

                            

    
def playerHasHitWorm(playerRect,wormRect):
    if playerRect.colliderect(wormRect):
        #print("crossed")
        global flies_hunt
        flies_hunt += 1
        return True
    return False
    
    

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False



def drawText(text, font, surface, x, y):
    global bat
    if bat == 1:
        TEXTCOLOR = Tw
    else:
        TEXTCOLOR = Tb
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def drawTextforWhitebat(text, font, surface, x, y):
    textobj = font.render(text, 1, Tw)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawTextforRed(text, font, surface, x, y):
    textobj = font.render(text, 1, Red)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def drawTextforBlue(text, font, surface, x, y):
    textobj = font.render(text, 1, Navy)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def text_objects(text,font,color):
    textSurface = font.render(text,True,color)
    return textSurface, textSurface.get_rect()



# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


pygame.display.set_caption("Bat's Hunt")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon) 


# set up fonts
hfont = pygame.font.SysFont('timesnewroman', 25)
font = pygame.font.SysFont('ardestineopentype', 20)

lfont = pygame.font.SysFont('ardestineopentype', 40)
largeText = pygame.font.SysFont('chiller', 90)
smallText = pygame.font.SysFont('chiller', 40)
midText = pygame.font.SysFont('chiller', 50)
smallTextS = pygame.font.SysFont('chiller', 25)
# set up ScoreFonts
fontScore = pygame.font.SysFont('ardestineopentype', 20)
fontScoreL = pygame.font.SysFont('ardestineopentype', 50)

# set up sounds
gameBeginSound = pygame.mixer.Sound('start.wav')
gameOverSound = pygame.mixer.Sound('end.wav')
pygame.mixer.music.load('bgm.wav')

# set up constant images
bg_help = pygame.image.load('bghelp.jpg')
baddieImage = pygame.image.load('perfecto.gif')
bg_start = pygame.image.load('bgstart.jpg')

worm1Image = pygame.image.load('fly.gif')
flyImage = pygame.image.load('fly.gif')


wormRect = worm1Image.get_rect()
flyRect =  flyImage.get_rect()


bg_start = pygame.transform.scale(bg_start,(WINDOWWIDTH, WINDOWHEIGHT))


def randomapple():
    randwx = round(random.randrange(50, 1100))
    
    randwy = round(random.randrange(25,500))
    return randwx, randwy
    
def Load_BATandBG(batim,bgim):

    
    playerImage = pygame.image.load(batim)
    playerRect = playerImage.get_rect()

    
    bg = pygame.image.load(bgim)
    bg = pygame.transform.scale(bg,(WINDOWWIDTH, WINDOWHEIGHT))

    return playerRect,playerImage,bg
  



    

def gameloop(playerRect,playerImage,bg):
    
    while True:

            # set up the start of the game
            apples = []
            baddies = []
            randwx1, randwy1 = randomapple()
            randwx2, randwy2 = randomapple()
            score = 0
            playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
            moveLeft = moveRight = moveUp = moveDown = False
            reverseCheat = slowCheat = False
            appleAddCounter = 0
            baddieAddCounter = 0
            pygame.mixer.music.play(-1, 0.0)

            while True: # the game loop runs while the game part is playing

                score += 1 # increase score
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()

                    if event.type == KEYDOWN:
                        if event.key == ord('z'):
                            reverseCheat = True
                        if event.key == ord('x'):
                            slowCheat = True
                        if event.key == K_LEFT or event.key == ord('a'):
                            moveRight = False
                            moveLeft = True
                        if event.key == K_RIGHT or event.key == ord('d'):
                            moveLeft = False
                            moveRight = True
                        if event.key == K_UP or event.key == ord('w'):
                            moveDown = False
                            moveUp = True
                        if event.key == K_DOWN or event.key == ord('s'):
                            moveUp = False
                            moveDown = True

                    if event.type == KEYUP:
                        if event.key == ord('z'):
                            reverseCheat = False
                            score = 0
                        if event.key == ord('x'):
                            slowCheat = False
                            score = 0
                        if event.key == K_ESCAPE:
                                terminate()

                        if event.key == K_LEFT or event.key == ord('a'):
                            moveLeft = False
                        if event.key == K_RIGHT or event.key == ord('d'):
                            moveRight = False
                        if event.key == K_UP or event.key == ord('w'):
                            moveUp = False
                        if event.key == K_DOWN or event.key == ord('s'):
                            moveDown = False

                    if event.type == MOUSEMOTION:
                        # If the mouse moves, move the player where the cursor is.
                        playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
                    
                    
                    
                # Add new baddies at the top of the screen, if needed.
                if not reverseCheat and not slowCheat:
                    baddieAddCounter += 1
                if baddieAddCounter == ADDNEWBADDIERATE:
                    baddieAddCounter = 0
                    baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                    newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                                }

                    baddies.append(newBaddie)


                # Move the player around.
                if moveLeft and playerRect.left > 0:
                    playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
                if moveRight and playerRect.right < WINDOWWIDTH:
                    playerRect.move_ip(PLAYERMOVERATE, 0)
                if moveUp and playerRect.top > 0:
                    playerRect.move_ip(0, -1 * PLAYERMOVERATE)
                if moveDown and playerRect.bottom < WINDOWHEIGHT:

                    
                    playerRect.move_ip(0, PLAYERMOVERATE)

                # Move the mouse cursor to match the player.
                pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

                # Move the baddies down.
                for b in baddies:
                    if not reverseCheat and not slowCheat:
                        b['rect'].move_ip(0, b['speed'])
                    elif reverseCheat:
                        b['rect'].move_ip(0, -5)
                    elif slowCheat:
                        b['rect'].move_ip(0, 1)

                # Delete baddies that have fallen past the bottom.
                for b in baddies[:]:
                    if b['rect'].top > WINDOWHEIGHT:
                        baddies.remove(b)
                        


                # Draw the game world on the window.
                                
                wormRect.topleft = (randwx1,randwy1)
                flyRect.topleft = (randwx2,randwy2)

                windowSurface.fill(Black)
                windowSurface.blit(bg,(0,0))
                
                wormRect.topleft = (randwx1,randwy1)
                
                flyRect.topleft = (randwx2,randwy2)
                
                



                # Draw the score and top score.
                drawText('Survival Points: %s' % (score), fontScore, windowSurface, 8, 0)
                drawText('Flies Hunt: %s' % (flies_hunt), fontScore, windowSurface, 1060, 0)

                # Draw the player's rectangle
                windowSurface.blit(playerImage, playerRect)
                windowSurface.blit(worm1Image,  wormRect)
                
                windowSurface.blit(flyImage,  flyRect)

                # Draw each baddie
                for b in baddies:
                    windowSurface.blit(b['surface'], b['rect'])

                pygame.display.update()
                #checkif player touched worm

                if playerHasHitWorm(playerRect, wormRect):
                    randwx1, randwy1 = randomapple()
                    
                if playerHasHitWorm(playerRect, flyRect):
                    randwx2, randwy2 = randomapple()
                    

                    

                # Check if any of the baddies have hit the player.
                if playerHasHitBaddie(playerRect, baddies):
                    #if score > topScore:
                        #topScore = score # set new top score
                    break

                mainClock.tick(FPS)

            # Stop the game and show the "Game Over" screen.
            pygame.mixer.music.stop()
            gameOverSound.play(-1)

            drawText('GAME OVER', smallText, windowSurface, (WINDOWWIDTH / 2.4), (WINDOWHEIGHT / 3.5))
            drawText('Press R to Restart', smallText, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 2.5))
            drawText('Press B to Go Back', smallText, windowSurface, (WINDOWWIDTH / 2.55), (WINDOWHEIGHT / 1.9))
            drawText('Press Q to Quit', smallText, windowSurface, (WINDOWWIDTH / 1.8), (WINDOWHEIGHT / 2.5))

            global total
            global files_hunt

            total = int(score/4) + (flies_hunt * 25)
            

            drawText('SCORE: %s' % (total),fontScoreL, windowSurface, 480,450)
            pygame.display.update()
            waitForPlayerToPressKey()

def buttonsforbc(msg1,x1,y1,w1,h1,inact1,act1,text_color1,text_size,action1=None):
        mouse1 = pygame.mouse.get_pos()
        click1 = pygame.mouse.get_pressed()
        
     
        if x1+w1 > mouse1[0] > x1 and y1+h1 > mouse1[1] > y1:
            pygame.draw.rect(windowSurface,act1,(x1,y1,w1,h1))
            
            
            if click1[2]==1 and action1 != None:
                if action1 == "PLAY_WHITE":
                    global bat
                    bat = 1
                    
                    [playerRect,playerImage,bg] = Load_BATandBG('batsilver.png','bgforwhite.jpg')
                    
                    gameBeginSound.stop()
                    gameloop(playerRect,playerImage,bg)
                if action1 == "PLAY_BLACK":

                    global bat
                    bat = 0
                    [playerRect,playerImage,bg] = Load_BATandBG('bat.png','bg.jpg')
                    gameBeginSound.stop()
                    gameloop(playerRect,playerImage,bg)
                if action1 == "QUIT":
                    terminate()
                if action1 == "BACK":
                    gameBeginSound.stop()
                    startscreen() 
                    
                

        else:
            pass


        
        textSurf1, textRect1 = text_objects(msg1,text_size,text_color1)
        textRect1.center = ((x1+(w1/2)),(y1+(h1/2)))
        windowSurface.blit(textSurf1,textRect1)
        

def buttonsforhelp(msg1,x1,y1,w1,h1,inact1,act1,text_color1,text_size,action1=None):
        mouse1 = pygame.mouse.get_pos()
        click1 = pygame.mouse.get_pressed()
        

        if x1+w1 > mouse1[0] > x1 and y1+h1 > mouse1[1] > y1:
            pygame.draw.rect(windowSurface,act1,(x1,y1,w1,h1))
            
        
            if click1[1]==1 and action1 != None:
                if action1 == "PLAY_WHITE":
                    global bat
                    bat = 1
                    
                    [playerRect,playerImage,bg] = Load_BATandBG('batsilver.png','bgforwhite.jpg')
                    
                    gameBeginSound.stop()
                    gameloop(playerRect,playerImage,bg)
                if action1 == "PLAY_BLACK":
                    global bat
                    bat = 0


                    [playerRect,playerImage,bg] = Load_BATandBG('bat.png','bg.jpg')
                    gameBeginSound.stop()
                    gameloop(playerRect,playerImage,bg)
                if action1 == "QUIT":
                    terminate()
                if action1 == "BACK":
                    gameBeginSound.stop()
                    startscreen() 
                    
                

        else:
            pass


        
        textSurf1, textRect1 = text_objects(msg1,text_size,text_color1)
        textRect1.center = ((x1+(w1/2)),(y1+(h1/2)))
        windowSurface.blit(textSurf1,textRect1)
        




def bcscreen():
    
    
    #start bcscreen display
    bcScreenDisplay = True


    #bat choose screen loop
    while bcScreenDisplay ==  True:
        #bc screen running
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            terminate()
                         

        
        # show the "bcStart" screen
        windowSurface.blit(bg_start,(0,0))
        buttonsforbc("WHITE",640,460,130,80,White,LBlack,Silver,midText,"PLAY_WHITE")
        drawTextforWhitebat('<<', midText, windowSurface,57, 510)
        buttonsforbc("BACK",100,520,100,50,White,LBlack,Silver,smallText,"BACK")
        buttonsforbc("BLACK",640,375,130,80,White,LBlack,Silver,midText,"PLAY_BLACK")
        buttonsforbc("QUIT",1045,520,100,50,White,LBlack,Silver,smallText,"QUIT")
        drawTextforWhitebat('Right click on the buttons to proceed.', font, windowSurface,430, 570)
        drawTextforWhitebat('.', largeText, windowSurface,608, 425)
        drawTextforWhitebat('.', largeText, windowSurface,608, 340)
                 
        drawTextforWhitebat('choose the BAT color:', smallText, windowSurface,310, 390)
        pygame.display.update()
        
        

def helpscreen():
    
    #start screen display
    helpScreenDisplay = True

    #help screen loop
    while helpScreenDisplay ==  True:
        #help screen running
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            terminate()
                         

        
        # show the "help" screen
        windowSurface.blit(bg_help,(0,0))
        drawTextforRed('<<', midText, windowSurface,57, 540)
        buttonsforhelp("BACK",100,550,100,50,White,LBlack,Red,smallText,"BACK")
        
        buttonsforhelp("QUIT",1045,550,100,50,White,LBlack,Red,smallText,"QUIT")

        drawTextforWhitebat('Middle click on the buttons to proceed.', font, windowSurface,430, 570)

        drawTextforRed('INSTRUCTIONS', lfont, windowSurface,500, 10)


        drawTextforBlue('Navigation', lfont, windowSurface,880, 50)
        drawTextforBlue('Objectives', lfont, windowSurface,150, 50)
        drawTextforBlue('Cheat Codes', lfont, windowSurface,140, 300)
        drawTextforBlue('Score Calculation', lfont, windowSurface,820, 300)

        #for objectives
        drawTextforWhitebat('* Help the BAT to Hunt the Flies.', font, windowSurface,30, 120)
        drawTextforWhitebat('* Dodge the fire balls thrown.', font, windowSurface,30, 160)
        drawTextforWhitebat('* Hunt as many flies as possible.', font, windowSurface,30, 200)
        drawTextforWhitebat('* Points for Survival too.', font, windowSurface,30, 240)

        #for cheat codes        
        drawTextforWhitebat('* Use key X for Slowing the speed of fire balls.', font, windowSurface,30, 410)
        drawTextforWhitebat('* Use key Z for reversing the speed of fire balls.', font, windowSurface,30, 450)
        drawTextforWhitebat('* NOTE: Score resets to 0 after each cheat code used.', font, windowSurface,30, 490)
        drawTextforWhitebat('* Slow & Reverse cheats are available', font, windowSurface,30, 370)

        #for navigation        
        drawTextforWhitebat('* Use Arrow Keys to move the Bat.', font, windowSurface,725, 120)
        drawTextforWhitebat('* Use mouse to move to the desired position.', font, windowSurface,725, 160)
        drawTextforWhitebat('* Use keys A for left & D for right.', font, windowSurface,725, 200)
        drawTextforWhitebat('* Use keys W for up & S for down.', font, windowSurface,725, 240)


        #for score
        drawTextforWhitebat('* Score is based on the SurvivalPoints &', font, windowSurface,725, 370)
        drawTextforWhitebat('* Number of Preys Hunt.', font, windowSurface,725, 410)
        drawTextforWhitebat('* 25 points for each fly.', font, windowSurface,725, 450)
        drawTextforWhitebat('* Total Score = SurvivalPoints/4 + PointsForPrey.', font, windowSurface,725, 490)


        pygame.display.update()
        

    

            
            
def buttons(msg,x,y,w,h,inact,act,text_color,text_size,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(windowSurface,act,(x,y,w,h))
            
            

            if click[0]==1 and action != None:
                if action == "PLAY":

                    
                    bcscreen()
                if action == "QUIT":
                    terminate()
                if action == "HELP":
                    helpscreen()
                
        else:
            pass


        
        textSurf, textRect = text_objects(msg,text_size,text_color)
        textRect.center = ((x+(w/2)),(y+(h/2)))
        windowSurface.blit(textSurf,textRect)
        
        







def startscreen():
    
    #start screen display
    StartScreenDisplay = True
    gameBeginSound.play(-1)

    #start screen loop
    while StartScreenDisplay ==  True:
        #start screen running
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            terminate()
                         

        
        # show the "Start" screen
        windowSurface.blit(bg_start,(0,0))

        buttons("PLAY",520,420,160,90,White,LBlack,Silver,largeText,"PLAY")
        buttons("HELP",100,500,100,50,White,LBlack,Silver,smallText,"HELP")
        buttons("QUIT",1000,500,100,50,White,LBlack,Silver,smallText,"QUIT")
        
        global TEXTCOLOR
        TEXTCOLOR = (218, 231, 218)
        drawTextforWhitebat('rAhulSyed', smallTextS, windowSurface,10, 570)
        drawTextforWhitebat('SyedSaqib', smallTextS, windowSurface,1120, 570)

        drawTextforWhitebat('Left click on the buttons to proceed.', font, windowSurface,430, 570)
        pygame.display.update()
        
        

startscreen()    








