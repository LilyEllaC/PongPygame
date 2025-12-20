import pygame
import random
import math
pygame.init()

#get fonts
font15=pygame.font.Font('freesansbold.ttf', 15)
font20=pygame.font.Font('freesansbold.ttf', 20)
font25=pygame.font.Font('freesansbold.ttf', 25)
font30=pygame.font.Font('freesansbold.ttf', 30)
font40=pygame.font.Font('freesansbold.ttf', 40)
font200=pygame.font.Font('freesansbold.ttf', 200)

#setting colours
RED=(255,0,0)
ORANGE=(255,137,0)
YELLOW=(247,255,0)
GREEN=(0,255,0)
LIGHT_GREEN=(125,255,125)
LIGHT_BLUE=(0,230,255)
BLUE=(0,0,255)
PURPLE=(179,0,255)
MAGENTA=(255,0,255)
WHITE=(255,255,255)
BLACK=(0,0,0)
GRAY=(177,177,177)

#screen
WIDTH,HEIGHT= 900, 600
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

#clock framerate
clock=pygame.time.Clock()
#please only set FPS to multiples of 30 for the visual of the trailing balls (nothing will actually break, it will just look different)
FPS=60
FPSScaling = 30/FPS

#showing text
def toScreen(words, font, colour, x, y):
    text=font.render(words, True, colour)
    textRect=text.get_rect()
    textRect.center=(x, y)
    screen.blit(text, textRect)

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
        if self.posY>HEIGHT+10 or self.posY<-10:
            self.posY=HEIGHT//2
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

#having an intro screen
def intro(screenSurface):
    playing=False
    colour=RED
    while not playing:
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
        toScreen("Use the w and s keys for the left paddle, and the up and down keys for the right paddle", font25, GRAY, WIDTH//2, 277)
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
                playing=True
            if event.type==pygame.MOUSEBUTTONDOWN and rightSpot:
                playing=True

        #updating the board image
        pygame.display.flip()

#having an ending scene
def outro(screenSurface, p1Points, p2Points, running, reloadSign):
    replaying=False
    colour=BLACK
    rightSpot=False
    while not replaying and running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        screenSurface.fill(RED)

        #showing score
        toScreen("Player 1: "+str(p1Points), font20, GREEN, 100, 20)
        toScreen("Player 2: "+str(p2Points), font20, GREEN, 250, 20)
        #toScreen("Player 3: "+str(p3Points), font20, GREEN, WIDTH-250, 20)
        #toScreen("Player 4: "+str(p4Points), font20, GREEN, WIDTH-100, 20)

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
        toScreen("Press to replay: ", font20, BLACK, WIDTH//2, HEIGHT//2-75)

        #get mouse coords
        mouseX, mouseY=pygame.mouse.get_pos()
        #see if it is in the right spot
        if (mouseX<WIDTH//2+55 and mouseX>WIDTH//2-55) and (mouseY<HEIGHT//2+55 and mouseY>HEIGHT//2-55):
            rightSpot=True
            colour=LIGHT_BLUE
        else:
            rightSpot=False
            colour=BLUE
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN and (rightSpot or colour==LIGHT_BLUE):
                replaying=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                print("Mouse clicked")
        #button
        rect=(WIDTH//2-55, HEIGHT//2-55, 110,110)
        pygame.draw.rect(screenSurface, colour, rect, 0, 0)
        #getting the reload sign
        for sign in reloadSign:
            sign.rect.x=WIDTH//2-50
            sign.rect.y=HEIGHT//2-50
        reloadSign.update()
        reloadSign.draw(screen)

        pygame.display.flip()
    return replaying

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

#typing!
def getNumFollowers():
    numFollowers=""
    running=True
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
    while running:
        #displaying
        screen.fill("YELLOW")
        time+=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                numFollowers="75"
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
        if numFollowers!="":
            createTrails(ball, int(numFollowers)*4//5, pastLocationsX, pastLocationsY, colours, balls, time)

        #checking whether it is a number
        if isNumber(numFollowers):
            colour=GREEN
        else:
            colour=RED

        #get mouse coords
        mouseX, mouseY=pygame.mouse.get_pos()
        #see if it is in the right spot
        if (mouseX<WIDTH//2+50 and mouseX>WIDTH//2-50) and (mouseY<HEIGHT-120 and mouseY>HEIGHT-220) and (colour==GREEN or colour==LIGHT_GREEN):
            rightSpot=True
            colour=LIGHT_GREEN
        elif colour==GREEN or colour==LIGHT_GREEN:
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
        toScreen("It can be any number, but it looks the best between 30 and 70. (upwards of 200 is weird, but still fun)", font15, MAGENTA, WIDTH//2, HEIGHT//2-50)

        toScreen(numFollowers, font25, RED, WIDTH//2, HEIGHT//2)
        pygame.display.flip()
        clock.tick(FPS)

    #continuing (deleting to save memory)
    balls.clear()
    return int(numFollowers)

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

#actual game part
def main():
    #Having the game actually play
    running=True

    #running intro
    intro(screen)

    paddleWidth  =10
    #actually creating the sprites
    player1=Paddle(20,HEIGHT//2,paddleWidth,100,10,BLUE)
    player2=Paddle(WIDTH-30,HEIGHT//2,paddleWidth,100,10,BLUE)
    player3=Paddle(WIDTH//2, HEIGHT-60, 100,paddleWidth,10,BLUE)
    player4=Paddle(WIDTH//2, 47,100,paddleWidth,10,BLUE)
    ball=Ball(WIDTH//2, HEIGHT//2, 9, 7, BLACK)

    #sprite group
    sprites=pygame.sprite.Group()
    button=Reload(100,100,WIDTH//2-50, 475)
    sprites.add(button)

    #having a small trail of balls behind to look cool
    colours=[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, MAGENTA]
    #seeing the past locations
    numFollowers=getNumFollowers()
    pastLocationsX=[]
    pastLocationsY=[]
    for i in range(0, numFollowers):
        pastLocationsX.append(0)
        pastLocationsY.append(0)
    #creating the followers
    balls=[]
    for i in range(1,numFollowers+1):
        balls.append(Ball(WIDTH//2, HEIGHT//2, 7-i/(numFollowers//7), 7, colours[i%7]))

    #More variable stuff
    allowedNumbers={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29}
    time=0
    timesHit=[]
    coolDownTime=FPS//5
    for i in range(0, coolDownTime):
        timesHit.append(0)

    #list of players
    playerList=[player1, player2, player3, player4]
    #parameters for the players
    player1Score, player2Score, player3Score, player4Score=0,0,0,0
    player1YDirect, player2YDirect, player3XDirect, player4XDirect=0,0,0,0

    #having it loop until it stops
    while running:
        time+=1
        #drawing background
        screen.fill(LIGHT_BLUE)

        #handling events (such as a buton or closing)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
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

            #powers
            #if timesHit.count(1)>3:
                #timesHit=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                #power(ball, player, playerList)

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

        #displaying time
        toScreen("Time left: "+str(120-(time//FPS)), font20, RED, 450, 20)

        #updating the screen
        pygame.display.update()
        pygame.display.flip()

        #frame rate
        clock.tick(FPS)
        #stopping at the end of the time
        if time==FPS*60*2:
            running=outro(screen, player1Score, player2Score, running, sprites)
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




#stuff?
if __name__=="__main__":
    main()
    pygame.quit()