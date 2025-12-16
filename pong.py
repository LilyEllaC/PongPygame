import pygame
import math
pygame.init()

#get font
font20=pygame.font.Font('freesansbold.ttf', 20)
font25=pygame.font.Font('freesansbold.ttf', 25)
font30=pygame.font.Font('freesansbold.ttf', 30)
font40=pygame.font.Font('freesansbold.ttf', 40)

#setting colours
RED=(255,0,0)
ORANGE=(255,137,0)
YELLOW=(247,255,0)
GREEN=(0,255,0)
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
FPS=30

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
        self.speed=speed
        self.colour=colour

        #hitbox
        self.playerRect=pygame.Rect(posX, posY, width, height)
        
        #object actually on the screen
        self.player=pygame.draw.rect(screen, self.colour, self.playerRect)

    # displaying on screen
    def display(self):
        self.playerRect=pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.player=pygame.draw.rect(screen, self.colour, self.playerRect)

    #updating state of object
    def update(self, yDirect):
        self.posY=self.posY+self.speed*yDirect

        #stopping it from going too high
        if self.posY<0:
            self.posY=0
        #going too low
        elif self.posY+self.height>HEIGHT:
            self.posY=HEIGHT-self.height

        #updating with new values
        self.playerRect=(self.posX, self.posX, self.width, self.height)

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
        self.speed = speed
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

        #hitting top or bottom and bouncing
        if self.posY<=0 or self.posY>=HEIGHT:
            self.yDirect*=-1

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
        self.xDirect*=-1
        self.firstTime=1
        self.speed=7
        self.yDirect=-1

    #hitting the paddles
    def hit(self):
        self.xDirect*=-1
        self.speed+=0.2

    #getting the ball shown?
    def getRect(self):
        return self.ball

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
        toScreen("PONG", font40, RED, WIDTH//2, 25)

        #Instructions
        toScreen("This is a 2 player game of pong where the ball gets faster everytime",font25,GRAY,WIDTH//2, 200)
        toScreen("it ges hit until a point is scored. If you hit the ball with the edge", font25, GRAY, WIDTH//2, 226)
        toScreen("of the paddle it will do something secret.", font25, GRAY, WIDTH//2, 251)

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
            if event.type==pygame.MOUSEBUTTONDOWN and rightSpot:
                playing=True

        #updating the board image
        pygame.display.flip()

#having an ending scene
def outro(screenSurface, p1Points, p2Points, running):
    replaying=False
    colour=BLACK
    while not replaying and running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        screenSurface.fill(RED)
        rect=(WIDTH//2-50, HEIGHT//2-50, 100,100)
        pygame.draw.rect(screenSurface, colour, rect, 0, 0)

        #showing who won
        if p1Points>p2Points:
            text=font20.render("Player 1 won!", True, BLACK)
        elif p2Points>p1Points:
            text=font20.render("Player 2 won!", True, BLACK)
        else:
            text=font20.render("It's a tie!", True, BLACK)
        textRect=text.get_rect()
        textRect.center=(WIDTH//2-15,100)
        screen.blit(text, textRect)


        #showing text
        toScreen("Press to replay: ", font20, BLACK, WIDTH//2, HEIGHT//2-75)

        #get mouse coords
        mouseX, mouseY=pygame.mouse.get_pos()
        #see if it is in the right spot
        if (mouseX<WIDTH//2+50 and mouseX>WIDTH//2-50) and (mouseY<HEIGHT//2+50 and mouseY>HEIGHT//2-50):
            rightSpot=True
            colour=GRAY
        else:
            rightSpot=False
            colour=BLACK
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN and rightSpot:
                replaying=True
        pygame.display.flip()
    return replaying

#having fun with the hitting with the edge glitch
def power(ball):
    ball.speed=35
    ball.xDirect*=-1
    ball.yDirect*=3
    ball.x=WIDTH//2


#actual game part
def main():
    #Having the game actually play
    running=True

    #running intro
    #intro(screen)

    #actually creating the sprites
    player1=Paddle(20,HEIGHT//2,10,100,10,BLUE)
    player2=Paddle(WIDTH-30,HEIGHT//2,10,100,10,BLUE)
    ball=Ball(WIDTH//2, HEIGHT//2, 7, 7, RED)
    colours=[RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, MAGENTA]
    #having a small trail of ball behind to look cool
    #seeing the past locations
    pastLocationsX=[]
    pastLocationsY=[]
    for i in range(0, 14):
        pastLocationsX.append(0)
        pastLocationsY.append(0)
    #creating the followers
    balls=[]
    for i in range(0,14):
        balls.append(Ball(WIDTH//2, HEIGHT//2, 7-i/2, 7, colours[i%7]))
    

    time=0
    timesHit=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    #list of players
    playerList=[player1, player2]
    #parameters for the players
    player1Score, player2Score=0,0
    player1YDirect, player2YDirect=0,0

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
                if event.key==pygame.K_UP:
                    player2YDirect=-1
                if event.key==pygame.K_DOWN:
                    player2YDirect=1
                if event.key==pygame.K_w:
                    player1YDirect=-1
                if event.key==pygame.K_s:
                    player1YDirect=1

            #stopping
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    player2YDirect=0
                if event.key==pygame.K_w or event.key==pygame.K_s:
                    player1YDirect=0

        #checking for ball-player collisions
        for player in playerList:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()
                timesHit[time%60]="1"
            else:
                timesHit[time%60+1]="0"

            #powers
            if timesHit.count("1")>3:
                timesHit=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                power(ball)
            
            #checking the following balls
            for follower in balls:
                if pygame.Rect.colliderect(follower.getRect(), player.getRect()):
                    follower.hit()


        #updating sprites
        player1.update(player1YDirect)
        player2.update(player2YDirect)
        #having the balls actually follow
        for i in range(0,len(balls)):
            balls[i].posX=pastLocationsX[len(balls)-i-1]
            balls[i].posY=pastLocationsY[len(balls)-i-1]
        point=ball.update()
        #updating the list
        pastLocationsX.append(ball.posX)
        pastLocationsY.append(ball.posY)
        pastLocationsX.pop(0)
        pastLocationsY.pop(0)

        #checking score
        if point==-1:
            player1Score+=1
        elif point==1:
            player2Score+=1
        
        #resetting ball because there was a point
        if point:
            ball.reset()

        #displaying the sprites
        player1.display()
        player2.display()
        for follower in balls:
            follower.display()
        ball.display()

        #showing scores
        player1.displayScore("Player 1: ", player1Score, 100, 20, MAGENTA)
        player2.displayScore("Player 2: ", player2Score, 250, 20, ORANGE)

        #showing hitboxes
        #pygame.draw.rect(screen, BLACK, ball.ballRect, 2)

        #displaying time
        toScreen("Time left: "+str(120-(time//30)), font20, RED, 450, 20)

        #updating the screen
        pygame.display.update()
        pygame.display.flip()

    
        #frame rate
        clock.tick(FPS)
        #stopping at the end of the time
        if time==30*60*2:
            running=outro(screen, player1Score, player2Score, running)



#stuff?
if __name__=="__main__":
    main()
    pygame.quit()
        
