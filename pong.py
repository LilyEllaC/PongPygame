import random
import pygame
import asyncio
# pylint: disable=no-member

pygame.init()
#get fonts
fontType='freesansbold.ttf'
font15=pygame.font.Font(fontType, 15)
font20=pygame.font.Font(fontType, 20)
font25=pygame.font.Font(fontType, 25)
font30=pygame.font.Font(fontType, 30)
font37=pygame.font.Font(fontType, 37)
font40=pygame.font.Font(fontType, 40)
font200=pygame.font.Font(fontType, 200)

#setting colours
RED=(255,0,0)
DARK_RED=(137,0,0)
ORANGE=(255,137,0)
DARK_ORANGE=(137,68,0)
YELLOW=(255,255,0)
DARK_YELLOW=(137,137,0)
GREEN=(0,230,15)
LIGHT_GREEN=(125,255,125)
DARK_GREEN=(0, 150, 0)
TEAL=(55,225,250)
DARK_TEAL=(0, 137, 137)
BLUE=(0,0,255)
DARK_BLUE=(0,0,170)
LIGHT_BLUE=(0,230,255)
PURPLE=(179,0,255)
DARK_PURPLE=(100, 0, 150)
MAGENTA=(255,0,255)
DARK_MAGENTA=(137,0,137)
WHITE=(255,255,255)
BLACK=(0,0,0)
GRAY=(177,177,177)
DARK_GRAY=(100,100,100)

#screen
WIDTH,HEIGHT= 900, 600
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

#clock framerate
clock=pygame.time.Clock()
#please only set FPS to multiples of 30 for the visual of the trailing balls (nothing will actually break, it will just look different)
FPS=30
FPSScaling = 30/FPS
gameRunning=True

#showing text
def toScreen(words, font, colour, x, y):
    text=font.render(words, True, colour)
    textRect=text.get_rect()
    textRect.center=(x, y)
    screen.blit(text, textRect)

#showing 2 lines of text
def toScreen2(words1, words2, font, colour, x, y):
    #first line
    toScreen(words1, font, colour, x, y-font.get_height()//2)
    #next line
    toScreen(words2, font, colour, x, y+font.get_height()//2)
 
#three lines
def toScreen3(words1, words2, words3, font, colour, x, y):
    #first line
    toScreen(words1, font, colour, x, y-font.get_height())
    #next line
    toScreen(words2, font, colour, x, y)
    #third line
    toScreen(words3, font, colour, x, y+font.get_height())

#getting the paddle class
class Paddle:
    #getting the position, dimensions, speed and colour
    def __init__(self, posX, posY, width, height, speed, colour):
        self.posX=posX
        self.posY=posY
        self.width=width
        self.height=height
        self.speed=speed*FPSScaling
        self.colour=colour
        self.playerRect=pygame.Rect(posX, posY, width, height)
        self.isHorizontal =width>50

        #object actually on the screen
        self.player=pygame.draw.rect(screen, self.colour, self.playerRect)
        
        #hitbox
        self.playerRect=pygame.Rect(posX, posY, width, height)

    # displaying on screen
    def display(self):
        self.playerRect=pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.player=pygame.draw.rect(screen, self.colour, self.playerRect)

    #updating state of object
    def updateY(self, yDirect):
        self.posY=self.posY+self.speed*yDirect

        #stopping it from going too high
        if self.posY<0:
            self.posY=0
        #going too low
        elif self.posY+self.height>HEIGHT:
            self.posY=HEIGHT-self.height
        
        #updating with new values
        self.playerRect=(self.posX, self.posY, self.width, self.height)

    def updateX(self, xDirect):
        self.posX=self.posX+self.speed*xDirect

        #far left
        if self.posX<0:
            self.posX=0
        #far right
        elif self.posX+self.width>WIDTH:
            self.posX=WIDTH-self.width

        #updating with new values
        self.playerRect=(self.posX, self.posY, self.width, self.height)

    #score images
    def displayScore(self, text, score, x, y, colour):
        #text=font20.render(text+str(score), True, colour)
        #textRect=text.get_rect()
        #textRect.center=(x,y)
        #screen.blit(text, textRect)
        toScreen(text+str(score), font20, colour, x, y)

        
    #returning the player
    def getRect(self):
        return self.playerRect

#ball class
class Ball:
    def __init__(self, posX, posY, radius, speed, colour):
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.speed = speed*FPSScaling
        self.colour = colour
        self.xDirect=1
        self.yDirect=-1
        self.ball=pygame.draw.circle(screen, self.colour, (self.posX, self.posY), self.radius)
        self.ballRect=pygame.Rect(self.posX, self.posY, 14, 14)
        self.firstTime=1

    #visual
    def display(self):
        self.ball=pygame.draw.circle(screen, self.colour, (self.posX, self.posY), self.radius)

    #updating
    def update(self):
        self.posX+=self.speed*self.xDirect
        self.posY+=self.speed*self.yDirect
        self.ballRect.x=self.posX-7
        self.ballRect.y=self.posY-7

        #touching left wall for the first time
        if self.posX<=0 and self.firstTime:
            self.firstTime=0
            return 1
        elif self.posX>=WIDTH and self.firstTime:
            self.firstTime=0
            return -1
        else:
            return 0
        
    #reset position
    def reset (self):
        self.posX=WIDTH//2
        self.posY=HEIGHT//2
        self.firstTime=1
        self.speed=7*FPSScaling
        #having the y and x direction be 1, but swap directions
        #x
        if self.xDirect<0:
            self.xDirect=1
        else:
            self.xDirect=-1
        #y
        if self.yDirect<0:
            self.yDirect=1
        else:
            self.yDirect=-1

    #hitting the paddles
    def hitH(self):
        self.xDirect*=-1+random.randint(-5,5)/40
        self.yDirect+=random.randint(-5,5)/40
        self.speed+=0.15*FPSScaling

    #hitting vertically
    def hitV(self):
        #hitting top or bottom and bouncing
        self.yDirect*=-1+random.randint(-5,5)/40
        self.xDirect+=random.randint(-5,5)/40
        if self.posY<0:
            self.posY=0
        elif self.posY>HEIGHT:
            self.posY=HEIGHT

    #getting the ball shown?
    def getRect(self):
        return self.ball

#reload button
class Reload(pygame.sprite.Sprite):
    def __init__(self, width, height, posX, posY):
        #self.width=width
        #self.height=height
        super().__init__()
        self.posX=posX
        self.posY=posY
        image=pygame.image.load("reload.png")
        self.image=pygame.transform.scale(image, (width, height))
        self.rect=self.image.get_rect()
    def update(self):
        self.posX=WIDTH//2-50
        self.posY=450

#celebration confetti
class Confetti(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, angle):
        super().__init__()
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.angle=angle
        image=pygame.image.load("confetti.png")
        self.image=pygame.transform.scale(image, (width, height))
        self.image=pygame.transform.rotate(self.image, self.angle)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
    def update(self):
        #moving down slowly and drifting a little
        self.rect.y+=10*FPSScaling
        self.rect.x+=random.randint(-2,2)*FPSScaling
        self.angle+=random.randint(-15,15)*FPSScaling
        image=pygame.image.load("confetti.png")
        image=pygame.transform.scale(image, (self.width, self.height))
        self.image=pygame.transform.rotate(image, self.angle) 
        #resetting if too low
        if self.rect.y>HEIGHT:
            self.rect.y=random.randint(-60,-30)
            self.rect.x=random.randint(0,WIDTH)
        self.y=self.rect.y
        self.x=self.rect.x

#having fun with a glitch that hopefully doesn't even happen anymore
def power(ball, player, playerList):
    #checks which paddle it is
    if player==playerList[0]:
        ball.xDirect=1
        ball.yDirect=0
        ball.posX=player.posX+player.width+ball.radius+1
    elif player==playerList[1]:
        ball.xDirect=-1
        ball.yDirect=0
        ball.posX=player.posX-ball.radius-1
    elif player==playerList[2]:
        ball.xDirect=0
        ball.yDirect=-1
        ball.posY=player.posY-ball.radius-1
    elif player==playerList[3]:
        ball.xDirect=0
        ball.yDirect=1
        ball.posY=player.posY+player.height+ball.radius+1

#checking that it is only numbers
def isNumber(number):
    numbers=[0,1,2,3,4,5,6,7,8,9]
    numAreDigits=0
    for i in range(0, len(number)):
        for j in range(0,10):
            if str(number[i])==str(numbers[j]):
                numAreDigits+=1
    if numAreDigits==len(number) and len(number)!=0:
        return True
    else:
        return False

#creating the balls for the demo
def createTrails(ball, numFollowers, pastLocationsX, pastLocationsY, colours, balls, time):
    #allowed number list
    #allowedNumbers={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29}
    allowedNumbers={0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58}
    
    #having the amount change when the number changes
    if (isNumber(numFollowers)):
        length=len(balls)
        #recreating when the number changes
        if int(numFollowers)!=length:
            pastLocationsX.clear()
            pastLocationsY.clear()
            balls.clear()
            for i in range(0, int(numFollowers)):
                pastLocationsX.append(-10)
                pastLocationsY.append(-10)
                balls.append(Ball(WIDTH//2, HEIGHT//2, 7-i/(int(numFollowers)/7), 7, colours[i%7]))
        
    #having the ball move around
    #top right
    if ball.posX>WIDTH-20 and ball.posY<20:
        #ball.posX=WIDTH-10
        ball.xDirect=0
        ball.yDirect=1
    #bottom left
    if ball.posX<20 and ball.posY>HEIGHT-20:
        ball.xDirect=0
        ball.yDirect=-1
        #ball.posX=10
    #bottom right
    if ball.posY>HEIGHT-20 and ball.posX>WIDTH-20:
        ball.xDirect=-1
        ball.yDirect=0
        #ball.posY=HEIGHT-10
    #top left
    if ball.posY<20 and ball.posX<20:
        ball.xDirect=1
        ball.yDirect=0
        #ball.posY=10
    
    #saving the past locations
    if inList((time%(FPS)*FPSScaling), allowedNumbers):
        pastLocationsX.append(ball.posX)
        pastLocationsY.append(ball.posY)
        pastLocationsX.pop(0)
        pastLocationsY.pop(0)

    #having the balls actually follow
    for i in range(0,len(balls)):
        balls[i].posX=pastLocationsX[len(balls)-i-1]
        balls[i].posY=pastLocationsY[len(balls)-i-1]
        balls[i].display()

    ball.update()
    ball.display()

#seeing if a number is in a list
def inList(number, numList):
    #going through
    for num in numList:
        #returning answer
        if num==number:
            return True
    return False

#checking that the ball has the right x/y coords
def rightPosition(personPos, ballPos, ballDirect):
    #Between the top and bottom of the paddle
    if ballPos+4>personPos and ballPos-4<personPos+100:
        return True
    else:
        if (ballPos>personPos+50 and ballDirect>0) or (ballPos<personPos+50 and ballDirect<0):
            return True
        else:
            return False

#drawing the outline for the buttons
def drawOutlines(xPos, yPos, width, height):
    rect=(xPos, yPos, width, height)
    pygame.draw.rect(screen, BLACK, rect, 3)

#checking if they are in the right spot
def checkSpot(xPos, yPos, width, height, colour):
    #getting mouse positions
    mouseX, mouseY=pygame.mouse.get_pos()
    if (mouseX>xPos and mouseX<xPos+width) and (mouseY>yPos and mouseY<yPos+height):
        if colour%2==0:
            colour+=1
    elif colour%2==1:
        colour-=1
    #returning the colour
    return colour

#check clicks
def checkClicks(boxes):
    global gameRunning
    endingScenario=[]
    _, mouseY=pygame.mouse.get_pos()

    #checking if it got clicked
    for event in pygame.event.get():
        #stopping
        if event.type==pygame.QUIT:
            gameRunning=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            for box in boxes:
                if box%2==1:
                    #having it remember whether it is time or points based
                    if mouseY<300:
                        endingScenario.append(0)
                    else:
                        endingScenario.append(1)
                    #Remembering the time/points to win
                    if box==boxes[0]:
                        endingScenario.append(60)
                    elif box==boxes[1]:
                        endingScenario.append(120)
                    elif box==boxes[2]:
                        endingScenario.append(180)
                    #points
                    elif box==boxes[3]:
                        endingScenario.append(3)
                    elif box==boxes[4]:
                        endingScenario.append(5)
                    elif box==boxes[5]:
                        endingScenario.append(10)
    return endingScenario

#double checking that they are sure of their answer
async def doubleCheck(endScenario):
    global gameRunning
    running=True
    box=(WIDTH//2-300, HEIGHT//2-200, 600, 400)
    width, height=75,50
    yesBox=(WIDTH//2-100-width, HEIGHT//2+50, width, height)
    noBox=(WIDTH//2+100, HEIGHT//2+50, width, height)
    colours=[RED, DARK_RED, GREEN, DARK_GREEN]
    yesColour, noColour=2,0
    keep=False

    #having it say the right thing
    if endScenario[0]==1:
        word=str(endScenario[1])+" points"
    else:
        word=str(endScenario//60)+" minutes"
    
    while running and gameRunning:
        #box
        pygame.draw.rect(screen, GRAY, box)
        drawOutlines(WIDTH//2-300, HEIGHT//2-200, 600, 400)

        #text
        toScreen3("Are you sure you want the game", "to go to "+word+"?", "That would be a really long game.", font30, BLACK, WIDTH//2, HEIGHT//2-30)
        
        #yes and no buttons
        yesColour=drawTextSqauare(colours, yesColour,"Yes", yesBox)
        noColour=drawTextSqauare(colours, noColour,"No", noBox)

        #checking stuff
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRunning=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if yesColour==3:
                    keep=True
                    running=False
                elif noColour==1:
                    keep=False
                    running=False

        #loading
        clock.tick(FPS)
        pygame.display.flip()
        await asyncio.sleep(0)  # Very important, and keep it 0

    return keep

#drawing the yes and no buttons
def drawTextSqauare(colours, colour, text, location):
    colour=checkSpot(location[0], location[1], location[2], location[3], colour)    
    pygame.draw.rect(screen, colours[colour], location)
    drawOutlines(location[0], location[1], location[2], location[3])
    toScreen(text, font25, BLACK, location[0]+location[2]//2, location[1]+location[3]/2)
    return colour

#other end parameter
async def findOther(endingScenario):
    global gameRunning
    running=True
    rect=(WIDTH//2-50, HEIGHT-110, 100, 100)
    trianglePoints=[(WIDTH//2-35, HEIGHT-100), (WIDTH//2-35, HEIGHT-20), (WIDTH//2+40, HEIGHT-60)]
    colour=RED
    endGoal=""
    question="Why don't I have a question?"
    clicked=False

    #seeing what to ask
    if endingScenario[0]==1:
        question="What score do you want the maximum to be?"
    elif endingScenario[0]==0:
        question="How many minutes do you want the game to run?"

    #running this
    while running and gameRunning:
        screen.fill(MAGENTA)

        #stuff
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRunning=False
            if event.type==pygame.KEYDOWN:
                #continuing by clicking enter
                if event.key==pygame.K_RETURN and isNumber(endGoal):
                    running=False
                #actually typing
                if event.key==pygame.K_BACKSPACE:
                    endGoal=endGoal[:-1]
                else:
                    endGoal+=event.unicode
            #checking clicking
            if event.type==pygame.MOUSEBUTTONDOWN and colour==DARK_GREEN:
                clicked=True
                if endingScenario[0]==1:
                    endingScenario.append(int(endGoal))
                else: 
                    endingScenario.append(int(endGoal)*60)
        
        #getting the button to change colour
        if isNumber(endGoal):
            colour=GREEN
        #get mouse coords
        mouseX, mouseY=pygame.mouse.get_pos()
        #see if it is in the right spot
        if (mouseX<WIDTH//2+50 and mouseX>WIDTH//2-50) and (mouseY<HEIGHT-10 and mouseY>HEIGHT-110) and (colour==GREEN or colour==DARK_GREEN):
            colour=DARK_GREEN
        elif colour==GREEN or colour==DARK_GREEN:
            colour=GREEN
        if  not isNumber(endGoal):
            colour=RED

        #having the button exist
        pygame.draw.rect(screen, colour, rect, 0, 0)
        drawOutlines(WIDTH//2-50, HEIGHT-110, 100, 100)
        #triangle
        pygame.draw.polygon(screen, BLACK, trianglePoints)

        #text
        toScreen(question, font30, BLACK, WIDTH//2, HEIGHT//2-200)
        toScreen(endGoal, font30, BLACK, WIDTH//2, HEIGHT//2)

        #checking if they are sure for weird answers
        if len(endingScenario)==2:
            if ((endingScenario[0]==1 and endingScenario[1]>20) or (endingScenario[0]==0 and int(endGoal)>10)) and clicked:
                if await doubleCheck(endingScenario):
                    running=False
                else:
                    endingScenario.pop(1)
                    endGoal=""
            else:
                running=False

        #displaying
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)  # Very important, and keep it 0
    
    return endingScenario

#having an intro screen
async def intro(screenSurface):
    global gameRunning
    playing=False
    colour=RED
    while not playing and gameRunning:
        screenSurface.fill(BLUE)
        #drawing play button
        #rectangle
        rect=(WIDTH//2-50, 490, 100,100)
        pygame.draw.rect(screenSurface, colour, rect, 0, 0)
        #triangle
        trianglePoints=[(WIDTH//2-35, 500), (WIDTH//2-35, 580), (WIDTH//2+40, 540)]
        pygame.draw.polygon(screenSurface, BLACK, trianglePoints)


        #showing title
        toScreen("PONG", font200, RED, WIDTH//2, 100)

        #Instructions
        toScreen("This is a 2 player game of pong where the ball gets faster everytime",font25,GRAY,WIDTH//2, 200)
        toScreen("it gets hit until a point is scored. A point gets scored when the ball ", font25, GRAY, WIDTH//2, 226)
        toScreen("hits either the left or right wall.", font25, GRAY, WIDTH//2, 251)
        toScreen("W and S keys move the left one, and up and down keys move the right one", font25, GRAY, WIDTH//2, 277)
        toScreen("The top and bottom paddles are just for helping score points.", font25, GRAY, WIDTH//2, 303)
        toScreen("Use the a and d keys for the top paddle (left player)", font25, GRAY, WIDTH//2, 328)
        toScreen("and the left and right keys for the bottom paddle (right player)", font25, GRAY, WIDTH//2, 354)
        toScreen("Have fun!", font25, GREEN, WIDTH//2, 380)


        #showing text
        toScreen("Press to play: ", font20, BLACK, WIDTH//2, 475)

        #get mouse coords
        mouseX, mouseY=pygame.mouse.get_pos()
        #see if it is in the right spot
        if (mouseX<WIDTH//2+50 and mouseX>WIDTH//2-50) and (mouseY<590 and mouseY>490):
            rightSpot=True
            colour=ORANGE
        else:
            rightSpot=False
            colour=RED
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRunning=False
            if event.type==pygame.MOUSEBUTTONDOWN and rightSpot:
                playing=True

        #updating the board image
        pygame.display.flip()
        await asyncio.sleep(0)  # Very important, and keep it 0

#typing!
async def getNumFollowers():
    numFollowers=""
    running=True
    global gameRunning
    colour=RED
    rightSpot=False
    time=0
    #showing the demo of the balls
    #creating the main ball
    ball=Ball(10, 10, 9, 7, BLACK)
    #seeing the past locations
    pastLocationsX=[]
    pastLocationsY=[]
    #creating the followers
    balls=[]
    #having the balls follow it just for fun
    #colours missing yellow because the background is yellow
    colours=[RED, ORANGE, GREEN, LIGHT_BLUE, BLUE, PURPLE, MAGENTA]

    #so it can stop
    while running and gameRunning:
        #displaying
        screen.fill("YELLOW")
        time+=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRunning=False
            if event.type==pygame.MOUSEBUTTONDOWN and rightSpot:
                running=False
            if event.type==pygame.KEYDOWN:
                #continuing by clicking enter
                if event.key==pygame.K_RETURN and isNumber(numFollowers):
                    running=False
                #actually typing
                if event.key==pygame.K_BACKSPACE:
                    numFollowers=numFollowers[:-1]
                else:
                    numFollowers+=event.unicode
        
        #creating the balls
        createTrails(ball, numFollowers, pastLocationsX, pastLocationsY, colours, balls, time)

        #checking whether it is a number
        if isNumber(numFollowers):
            colour=GREEN
        else:
            colour=RED

        #get mouse coords
        mouseX, mouseY=pygame.mouse.get_pos()
        #see if it is in the right spot
        if (mouseX<WIDTH//2+50 and mouseX>WIDTH//2-50) and (mouseY<HEIGHT-120 and mouseY>HEIGHT-220) and (colour==GREEN or colour==DARK_GREEN):
            rightSpot=True
            colour=DARK_GREEN
        elif colour==GREEN or colour==DARK_GREEN:
            rightSpot=False
            colour=GREEN
        else:
            colour=RED

        #having the button exist
        rect=(WIDTH//2-50, HEIGHT-220, 100,100)
        pygame.draw.rect(screen, colour, rect, 0, 0)
        #triangle
        trianglePoints=[(WIDTH//2-35, 390), (WIDTH//2-35, 470), (WIDTH//2+40, 430)]
        pygame.draw.polygon(screen, BLACK, trianglePoints)

        #showing the text
        toScreen("Fun patterns", font40, BLUE, WIDTH//2-90, 50)
        toScreen("(Optional)", font25, BLUE, WIDTH//2+110,50)
        toScreen("Please enter the number of mini balls you want following the main ball.", font25, MAGENTA, WIDTH//2, HEIGHT//2-100)
        toScreen("These balls don't do anything, they just look really cool.", font25, MAGENTA, WIDTH//2, HEIGHT//2-70)
        toScreen("It can be any number, but it looks the best between 30 and 70. (upwards of 200 is weird, but still fun)", font15, MAGENTA, WIDTH//2, HEIGHT//2-47)

        toScreen(numFollowers, font25, RED, WIDTH//2, HEIGHT//2)
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)  # Very important, and keep it 0


    #continuing (deleting to save memory)
    balls.clear()
    #if already closed
    if numFollowers=="":
        numFollowers="75"
    return int(numFollowers)

#getting the way the game ends
async def getEndVariables():
    running=True
    global gameRunning
    endingScenario=[]
    check=[]
    #colours
    colours=[RED, DARK_RED, ORANGE, DARK_ORANGE, YELLOW, DARK_YELLOW, GREEN, DARK_GREEN, BLUE, DARK_BLUE, PURPLE, DARK_PURPLE, TEAL, DARK_TEAL]
    box1=0
    box2=2
    box3=4
    box4=6
    box5=8
    box6=10
    boxOther1=12
    boxOther2=12
    boxes=[box1, box2, box3, box4, box5, box6, boxOther1, boxOther2]

    #creating variables for the x and y coords
    xPos1And4=25
    xPos2And5=WIDTH//2-195
    xPos3And6=WIDTH-415
    xPosOthers=WIDTH-185
    yPos123=150
    yPos456=400

    #height and width
    height, width=150, 200
    otherWidth=165

    #running the code
    while running and gameRunning:
        screen.fill(DARK_MAGENTA)

        #showing the boxes
        #box1 (1 minute)
        rect=(xPos1And4, yPos123, width, height)
        pygame.draw.rect(screen, colours[box1], rect, 0, 0)
        #box2 (2 minutes)
        rect=(xPos2And5, yPos123, width, height)
        pygame.draw.rect(screen, colours[box2], rect, 0, 0)
        #box3 (3 minutes?)
        rect=(xPos3And6, yPos123, width, height)
        pygame.draw.rect(screen, colours[box3], rect, 0, 0)
        #box4 (3 points?)
        rect=(xPos1And4, yPos456, width, height)
        pygame.draw.rect(screen, colours[box4], rect, 0, 0)
        #box5 (5 points?)
        rect=(xPos2And5, yPos456, width, height)
        pygame.draw.rect(screen, colours[box5], rect, 0, 0)
        #box6 (10 points?)
        rect=(xPos3And6, yPos456, width, height)
        pygame.draw.rect(screen, colours[box6], rect, 0, 0)
        #others
        #box7 (10 points?)
        rect=(xPosOthers, yPos123, otherWidth, height)
        pygame.draw.rect(screen, colours[boxOther1], rect, 0, 0)
        #box8 (10 points?)
        rect=(xPosOthers, yPos456, otherWidth, height)
        pygame.draw.rect(screen, colours[boxOther2], rect, 0, 0)

        #outlines
        drawOutlines(xPos1And4, yPos123, width, height)
        drawOutlines(xPos2And5, yPos123, width, height)
        drawOutlines(xPos3And6, yPos123, width, height)
        drawOutlines(xPos1And4, yPos456, width, height)
        drawOutlines(xPos2And5, yPos456, width, height)
        drawOutlines(xPos3And6, yPos456, width, height)
        drawOutlines(xPosOthers, yPos123, otherWidth, height)
        drawOutlines(xPosOthers, yPos456, otherWidth, height)

        #seeing if it is in the right spot
        box1=checkSpot(xPos1And4, yPos123, width, height, box1)
        box2=checkSpot(xPos2And5, yPos123, width, height, box2)
        box3=checkSpot(xPos3And6, yPos123, width, height, box3)
        box4=checkSpot(xPos1And4, yPos456, width, height, box4)
        box5=checkSpot(xPos2And5, yPos456, width, height, box5)
        box6=checkSpot(xPos3And6, yPos456, width, height, box6)
        boxOther1=checkSpot(xPosOthers, yPos123, xPosOthers, height, boxOther1)
        boxOther2=checkSpot(xPosOthers, yPos456, xPosOthers, height, boxOther2)
        boxes=[box1, box2, box3, box4, box5, box6, boxOther1, boxOther2]

        #seeing if it got clicked and setting what the ending goal is
        check=checkClicks(boxes)
        if len(check)==2:
            endingScenario=check
            running=False
        elif len(check)==1:
            endingScenario=await findOther(check)
            running=False

        #displaying the text
        toScreen("Please choose when you want the game to end", font37, BLACK, WIDTH//2, 30)
        toScreen("After a certain length of time:", font30, BLACK, WIDTH//2, 110)
        toScreen("After someone reaches a certain number of points:", font30, BLACK, WIDTH//2, 360)
        
        #each button
        textColour=BLACK
        toScreen("1 Minute", font30, textColour, xPos1And4+width//2, yPos123+height//2)
        toScreen("2 Minutes", font30, textColour, xPos2And5+width//2, yPos123+height//2)
        toScreen("3 Minutes", font30, textColour, xPos3And6+width//2, yPos123+height//2)
        toScreen("3 Points", font30, textColour, xPos1And4+width//2, yPos456+height//2)
        toScreen("5 Points", font30, textColour, xPos2And5+width//2, yPos456+height//2)
        toScreen("10 points", font30, textColour, xPos3And6+width//2, yPos456+height//2)
        toScreen2("Other", "time", font30, textColour, xPosOthers+otherWidth//2, yPos123+height//2)
        toScreen2("Other", "points", font30, textColour, xPosOthers+otherWidth//2, yPos456+height//2)

        #displaying
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)  # Very important, and keep it 0


    #returning answer
    return endingScenario

#having an ending scene
async def outro(screenSurface, p1Points, p2Points):
    global gameRunning
    replaying=False
    #stuff ofr the buttons
    restartRect=(WIDTH//2-55, HEIGHT//2-55, 110,110)
    rectX, rectY, rectWidth, rectHeight=WIDTH-133,10,120,50
    quitRect=(rectX, rectY, rectWidth, rectHeight)
    colours=[BLUE, DARK_BLUE, RED, DARK_RED]
    restartColour=0
    quitColour=2

    #sprite stuff
    sprites=pygame.sprite.Group()
    #restarting button
    button=Reload(100,100,WIDTH//2-50, 475)
    sprites.add(button)
    confettis=[]
    #confetti
    for i in range(0,15):
        confettis.append(Confetti(100,100,random.randint(0, WIDTH), random.randint(-300,300),random.randint(0,360)))
        sprites.add(confettis[i])

    #actually running
    while not replaying and gameRunning:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRunning=False
            elif event.type==pygame.MOUSEBUTTONDOWN and restartColour==1:
                replaying=True
            elif event.type==pygame.MOUSEBUTTONDOWN and quitColour==3:
                gameRunning=False
        screenSurface.fill(LIGHT_GREEN)

        #showing score
        toScreen("Player 1: "+str(p1Points), font20, PURPLE, 100, 20)
        toScreen("Player 2: "+str(p2Points), font20, PURPLE, 250, 20)

        #showing who won
        if p1Points>p2Points:
            text=font30.render("Player 1 won!", True, BLACK)
        elif p2Points>p1Points:
            text=font30.render("Player 2 won!", True, BLACK)
        else:
            text=font30.render("It's a tie!", True, BLACK)
        textRect=text.get_rect()
        textRect.center=(WIDTH//2-15,100)
        screen.blit(text, textRect)

        #showing text
        toScreen("Press to replay:", font20, BLACK, WIDTH//2, HEIGHT//2-75)

        #see if it is in the right spot
        restartColour=checkSpot(WIDTH//2-55, HEIGHT//2-55, 110, 110, restartColour)
        quitColour=checkSpot(rectX, rectY, rectWidth, rectHeight, quitColour)
            
        #button
        pygame.draw.rect(screenSurface, colours[restartColour], restartRect, 0, 0)
        drawOutlines(WIDTH//2-55, HEIGHT//2-55, 110, 110)
        #getting the reload sign
        button.rect.x=WIDTH//2-50
        button.rect.y=HEIGHT//2-50
        #Quit button
        pygame.draw.rect(screenSurface, colours[quitColour], quitRect)
        drawOutlines(rectX, rectY, rectWidth, rectHeight)
        toScreen("QUIT", font40, BLACK, WIDTH-75, 38)

        #having the confetti move
        for confetti in confettis:
            confetti.update()
        
        #sprites
        sprites.draw(screen)

        pygame.display.flip()
        await asyncio.sleep(0)  # Very important, and keep it 0

        clock.tick(FPS)
    return replaying

#actual game part
async def main():
    #Having the game actually play
    running=True
    global gameRunning

    #running intro
    #findOther([0])
    await intro(screen)
    #getting the number of followers
    numFollowers= await getNumFollowers()
    #getting the ending scenario
    endingScenario= await getEndVariables()

    paddleWidth=10
    #actually creating the sprites
    player1=Paddle(20,HEIGHT//2,paddleWidth,100,10,BLUE)
    player2=Paddle(WIDTH-30,HEIGHT//2,paddleWidth,100,10,BLUE)
    player3=Paddle(WIDTH//2, HEIGHT-60, 100,paddleWidth,10,BLUE)
    player4=Paddle(WIDTH//2, 47,100,paddleWidth,10,BLUE)
    ball=Ball(WIDTH//2, HEIGHT//2, 9, 7, BLACK)

    #having a small trail of balls behind to look cool
    colours=[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, MAGENTA]

    #seeing the past locations
    pastLocationsX=[]
    pastLocationsY=[]
    for i in range(0, numFollowers):
        pastLocationsX.append(0)
        pastLocationsY.append(0)
    #creating the followers
    balls=[]
    if numFollowers>=7:
        for i in range(1,numFollowers+1):
            balls.append(Ball(WIDTH//2, HEIGHT//2, 7-i/(numFollowers//7), 7, colours[i%7]))
    else:
        for i in range(1,numFollowers+1):
            balls.append(Ball(WIDTH//2, HEIGHT//2, 7-i*(numFollowers/7), 7, colours[i%7]))

    #More variable stuff for having a cooldown and the following balls
    allowedNumbers={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29}
    time=0
    timesHit=[]
    coolDownTime=FPS//5
    for i in range(0, coolDownTime):
        timesHit.append(0)

    #list of players
    playerList=[player1, player2, player3, player4]
    #settings for the players
    player1Score, player2Score, player3Score, player4Score=0,0,0,0
    player1YDirect, player2YDirect, player3XDirect, player4XDirect=0,0,0,0


    #having it loop until it stops
    #PLAYING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    while running and gameRunning:
        time+=1
        #drawing background
        screen.fill(LIGHT_BLUE)

        #handling events (such as a buton or closing)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRunning=False
            if event.type==pygame.KEYDOWN:
                #changing direction when a key is pressed
                #p2
                if event.key==pygame.K_UP:
                    player2YDirect=-1
                if event.key==pygame.K_DOWN:
                    player2YDirect=1
                #p1
                if event.key==pygame.K_w:
                    player1YDirect=-1
                if event.key==pygame.K_s:
                    player1YDirect=1
                #p3
                if event.key==pygame.K_LEFT:
                    player3XDirect=-1
                if event.key==pygame.K_RIGHT:
                    player3XDirect=1
                #p4
                if event.key==pygame.K_a:
                    player4XDirect=-1
                if event.key==pygame.K_d:
                    player4XDirect=1


            #stopping
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    player2YDirect=0
                if event.key==pygame.K_w or event.key==pygame.K_s:
                    player1YDirect=0
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    player3XDirect=0
                if event.key==pygame.K_a or event.key==pygame.K_d:
                    player4XDirect=0

        #checking for ball-player collisions
        timesHit[time%coolDownTime]=0
        #goint through all the players
        for player in playerList:
            #seeing if the touched
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                #horizontal paddles edge hits
                if (player.isHorizontal):
                    if rightPosition(player.posX, ball.posX, ball.xDirect) and not inList(1, timesHit):
                        ball.hitV()
                    elif not inList(1, timesHit):
                        ball.hitH()
                #vertical paddles
                else:
                    if rightPosition(player.posY, ball.posY, ball.yDirect) and not inList(1, timesHit):
                        ball.hitH()
                    elif not inList(1, timesHit):
                        ball.hitV()
                #stopping it from getting stuck and doing something fun
                timesHit[time%coolDownTime]=1

        #checking ball for bouncing on top or bottom
        if ball.posY<=0 or ball.posY>=HEIGHT:
            ball.hitV()

        #updating sprites
        player1.updateY(player1YDirect)
        player2.updateY(player2YDirect)
        player3.updateX(player3XDirect)
        player4.updateX(player4XDirect)

        #having the balls actually follow
        for i in range(0,len(balls)):
            balls[i].posX=pastLocationsX[len(balls)-i-1]
            balls[i].posY=pastLocationsY[len(balls)-i-1]

        point=ball.update()
        #updating the list
        if inList(time%FPS*FPSScaling, allowedNumbers):
            pastLocationsX.append(ball.posX)
            pastLocationsY.append(ball.posY)
            pastLocationsX.pop(0)
            pastLocationsY.pop(0)

        #checking score
        if point==-1:
            player1Score+=1
        elif point==1:
            player2Score+=1
        elif point==2:
            player3Score+=1
        elif point==-2:
            player4Score+=1
        
        #resetting ball because there was a point
        if point!=0:
            ball.reset()

        #displaying the sprites
        player1.display()
        player2.display()
        player3.display()
        player4.display()
        for follower in balls:
            follower.display()
        ball.display()

        #showing scores
        player1.displayScore("Player 1: ", player1Score, 100, 20, ORANGE)
        player2.displayScore("Player 2: ", player2Score, 250, 20, ORANGE)
        #player3.displayScore("Player 3: ", player3Score, WIDTH-250, 20, ORANGE)
        #player4.displayScore("Player 4: ", player4Score, WIDTH-100, 20, ORANGE)

        #showing hitboxes (giving them an outline :) )
        pygame.draw.rect(screen, BLACK, player1.playerRect, 3)
        pygame.draw.rect(screen, BLACK, player2.playerRect, 3)
        pygame.draw.rect(screen, BLACK, player3.playerRect, 3)
        pygame.draw.rect(screen, BLACK, player4.playerRect, 3)
        
        #getting it to end when they want it to
        #time
        ending=False
        if endingScenario[0]==0:
            #displaying time
            toScreen("Time left: "+str(endingScenario[1]-(time//FPS)), font20, RED, 450, 20)
            #checking
            if time==FPS*endingScenario[1]:
                ending=True
        elif endingScenario[0]==1:
            #displaying time
            toScreen("Time: "+str(time//FPS), font20, RED, 450, 20)
            #checking
            if player1Score==endingScenario[1] or player2Score==endingScenario[1]:
                ending=True

        #updating the screen
        pygame.display.update()
        pygame.display.flip()
        await asyncio.sleep(0)  # Very important, and keep it 0


        #frame rate
        clock.tick(FPS)

        #stopping 
        if ending:
            running= await outro(screen, player1Score, player2Score)
            #resetting variables
            if running:
                for i in range(0, numFollowers):
                    pastLocationsX.append(0)
                    pastLocationsY.append(0)
                ball.reset()
                time=0
                player1.posY=HEIGHT//2
                player2.posY=HEIGHT//2
                player3.posX=WIDTH//2
                player4.posX=WIDTH//2
                player1Score, player2Score, player3Score, player4Score=0,0,0,0
                player1YDirect, player2YDirect, player3XDirect, player4XDirect=0,0,0,0
                pastLocationsX.clear()
                pastLocationsY.clear()
                for i in range(0, numFollowers):
                    pastLocationsX.append(0)
                    pastLocationsY.append(0)
        await asyncio.sleep(0)  # probably important, and keep it 0

#stuff?
if __name__=="__main__":
    asyncio.run(main())

    pygame.quit()
    