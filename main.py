import pygame
import random
import math
import time
pygame.init()

class PygameGame(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=55, title="Hill climb racing"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0,0,0)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self._keys = dict()
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()

class Game(PygameGame):
    def init(self):
        self.mode="splashScreen"
        pygame.key.set_repeat(50, 80)
        self.tealColor=(0,153,153)
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.gameLength=30
        self.difficulty=.5
        self.pathLength =self.width*self.gameLength
        self.gameInit()

    def gameInit(self):
        self.imagesInit()
        self.playerInit()
        self.gamePlay()
        #create the hills
        self.hillStartY=600
        self.pixelStep=25
        self.numHills=30
        self.hills=[]
        self.randomHeights=self.getRandomHeights(self.numHills)
        self.createHills()

        self.numCoins=50
        self.coins=[]
        self.drawCoins=False
        self.coinCount=0
        self.createCoins()

        self.fuelGauge= FuelGauge(20,20)
        self.fuelTanks=[]
        self.placeFuel()

        self.boulders=[]

        self.plane=Plane(150,50)
    def gamePlay(self):
        self.gameOver=False
        self.display=False
        self.count=0
        self.lives=3
        self.score=0
        self.paused=False
        self.gameWon=False
        self.invincible=False
        self.flashingCount=0
        self.drawInstructions=False
        self.destroyed=False
        self.lift=False
        self.displayWarning=False
    def playerInit(self):
        self.scrollX = 0
        self.scrollMargin = 700
        self.r=7
        self.x1=self.scrollMargin
        self.x2=self.scrollMargin+50
        self.y1=0
        self.y2=0

        self.speed=18
        self.angle=0
        self.rotationAngle=0
        self.maxSpeed=20
        self.slope=0
    def imagesInit(self):
        self.homeCar=pygame.image.load('D:\game\car.jpg').convert_alpha()
        homeCarW,homeCarH = self.homeCar.get_size()
        pygame.transform.scale(self.homeCar, (int(homeCarW), int(homeCarH)))
        self.homeFinish=pygame.image.load('D:/game/finish.jpg').convert_alpha()
        homeFinishW,homeFinishH=self.homeFinish.get_size()
        self.homeFinish=pygame.transform.scale(self.homeFinish,
                                (int(homeFinishW*.2), int(homeFinishH*.5)))
        self.gameScreen()
        self.instructionsScreen()
    def gameScreen(self):
        self.gameBackground = pygame.image.load('D:\game\sky.JFIF').convert_alpha()
        gameBackgroundW,gameBackgroundH = self.gameBackground.get_size()
        self.gameBackground = pygame.transform.scale(self.gameBackground,
                        (int(gameBackgroundW*3.2), int(gameBackgroundH*3.9)))
        self.car = pygame.image.load(r'D:\game\gif.gif').convert_alpha()
        self.w,self.h = self.car.get_size()
        self.w*=.14
        self.h*=.2
        self.car = pygame.transform.scale(self.car,
                            (int(self.w), int(self.h)))
        self.invincibleCar=pygame.image.load('D:/game/gif.gif').convert_alpha()
        invincibleCarW,invincibleCarH=self.invincibleCar.get_size()
        invincibleCarW*=.09
        invincibleCarH*=0.1
        self.invincibleCar=pygame.transform.scale(self.invincibleCar,
                          (int(invincibleCarW), int(invincibleCarH)))
        self.finish=pygame.image.load('D:/game/finish.jpg').convert_alpha()
        finishW,finishH=self.finish.get_size()
        self.finish= pygame.transform.scale(self.finish,
                                     (int(finishW*.5), int(finishH*.5)))
    def instructionsScreen(self):
        self.howToPlay=pygame.image.load('D:\game\instruction.jpg').convert_alpha()
        instructW,instructH=self.howToPlay.get_size()
        self.howToPlay = pygame.transform.scale(self.howToPlay,
                                        (int(instructW*1), int(instructH*1)))
    def mousePressed(self,x,y):
        if (self.mode == "splashScreen"):
            self.splashScreenMousePressed(x,y)
        elif (self.mode == "game"):
            self.gameMousePressed(x,y)
        elif (self.mode == "menu"):
            self.menuMousePressed(x,y)
    def keyPressed(self,keyCode, modifier):
        if (self.mode == "splashScreen"):
            self.splashScreenKeyPressed(keyCode, modifier)
        elif (self.mode == "game"):
            self.gameKeyPressed(keyCode, modifier)
        elif (self.mode == "menu"):
            self.menuKeyPressed(keyCode, modifier)
    def timerFired(self,dt):
        if (self.mode == "splashScreen"):
            self.splashScreenTimerFired(dt)
        elif (self.mode == "game"):
            self.gameTimerFired(dt)
        elif (self.mode == "menu"):
            self.menuTimerFired(dt)
    def redrawAll(self,screen):
        if (self.mode == "splashScreen"):
            self.splashScreenRedrawAll(screen)
        elif (self.mode == "game"):
            self.gameRedrawAll(screen)
        elif (self.mode == "menu"):
            self.menuRedrawAll(screen)
    def splashScreenMousePressed(self,x,y):
        if (x>=150 and x<=300) and (y>=520 and y<=620):
            self.mode="game"
            self.difficulty=.1
        if (x>=320 and x<=470) and (y>=520 and y<=620):
            self.mode="game"
            self.difficulty=.5
        if (x>=500 and x<=650) and (y>=520 and y<=620):
            self.mode="game"
            self.difficulty=1
        elif (x>=150 and x<=650) and (y>=640 and y<=740):
            self.mode="menu"
    def splashScreenKeyPressed(self,keyCode, modifier):
        pass
    def splashScreenTimerFired(self,dt):
        pass
    def splashScreenRedrawAll(self,screen):

        pygame.draw.rect(screen,self.tealColor,(0,0,self.width,self.height))
        pygame.draw.rect(screen,self.white,(140,500,150,100),4)
        pygame.draw.rect(screen, self.white, (310,500,150,100),4)
        pygame.draw.rect(screen, self.white,(490,500,150,100),4)
        pygame.draw.rect(screen,self.white,(150,640,400,100),4)
        screen.blit(self.homeFinish, (0,80))
        screen.blit(self.homeFinish, (640,80))
        screen.blit(self.homeCar, (200,200))
        font=pygame.font.SysFont("euphemiaucas",40)
        start=font.render("EASY",True,self.white)
        screen.blit(start,(180,540))
        start=font.render(" MEDIUM",True,self.white)
        screen.blit(start,(320,540))
        start=font.render("HARD",True,self.white)
        screen.blit(start,(520,540))
        fontInstructions=pygame.font.SysFont("euphemiaucas",55)
        instructions=fontInstructions.render("  INSTRUCTIONS",True,self.white)
        screen.blit(instructions,(180,650))
        font=pygame.font.SysFont("euphemiaucas",75)
        hillRacer=font.render("HILL CLIMB RACING 3", True,self.white)
        screen.blit(hillRacer,(80,80))

    def menuRedrawAll(self,screen):
        pygame.draw.rect(screen,self.tealColor,(0,0,self.width, self.height))
        screen.blit(self.howToPlay,(5,5))#image with instructions
        pygame.draw.rect(screen,self.white,(300,670,230,70),2)
        font=pygame.font.SysFont("euphemiaucas",55)
        back=font.render("BACK", True,self.white)
        screen.blit(back,(348,670))
    def menuMousePressed(self,x,y):
        if ((x>=300 and x<=530) and (y<=740 and y>=670)):
            self.mode="splashScreen"
    def menuKeyPressed(self,keyCode, modifier):
        pass
    def menuTimerFired(self,dt):
        pass
    def gameMousePressed(self,x,y):
        if self.gameOver==True or self.gameWon==True:
            if (x>=350 and x<=550) and (y<=400 and y>=350):
                self.init()
            if (x>=350 and x<=550) and (y<=480 and y>=430):
                pygame.quit()
        else:
            if ((x>=720 and x<=780) and (y<=42 and y>=12)):
                self.init()
    def gameKeyPressed(self,keyCode, modifier):
        if keyCode== pygame.K_RIGHT:
            if self.speed<self.maxSpeed:
                self.speed+=10
        if keyCode==pygame.K_LEFT:
            self.speed-=2
        if keyCode==pygame.K_r:
            self.gameInit()
        if keyCode==pygame.K_p:
            self.paused= not self.paused

    def gameTimerFired(self, dt):

        sx=self.scrollX
        self.count+=1

        if self.gameOver==False and self.paused==False and self.gameWon==False:
            self.h=47.6
            if self.fuelGauge.width>0:
                self.fuelGauge.width-=self.difficulty
            else:
                self.gameOver= True
            if self.fuelGauge.width<=50:
                self.displayWarning=True
                self.startWarning=time.time()
            if self.displayWarning:
                self.endWarning=time.time()
                if (((self.endWarning-self.startWarning)>2) or
                    (self.fuelGauge.width>50)):
                    self.displayWarning=False
            self.y1=self.getY(self.x1)-self.r-5
            self.y2=self.getY(self.x2)-self.r-5
            self.x1+=self.speed
            self.x2+=self.speed

            self.moveCar()

            self.gravity()
            if self.speed >0:
                self.speed -=.2

            self.plane.move(self.x1)
            if self.speed<=self.maxSpeed:
                if self.slope<0:
                    if self.slope<-.5:
                        self.speed+=5
                    else:
                        self.speed+=.5

            if self.slope>0:
                if self.slope>.5:
                    self.speed-=.7
                else:
                    self.speed-=.5
            if self.speed>=20 and abs(self.slope)>=.3:
                self.lift=True
                self.y1-=15
                self.y2-=15

            if self.count%30==0 and self.plane.speed>=5:
                self.boulders.append(Boulder(self.plane.x+100,self.plane.y+100))

            self.boundsA= self.getPlayerBounds()
            for coin in self.coins:
                self.boundsB=coin.getBounds()

                if self.boundsIntersect(self.boundsA,self.boundsB):
                    self.score+=50
                    self.coinCount+=1
                    self.coins.remove(coin)
                    pass
            if self.coinCount%40==0 and self.coinCount!=0:
                self.invincible=True
                self.startTime=time.time()
                self.display=True
            if self.invincible:
                self.endTime= time.time()
                if self.endTime-self.startTime>=5:
                    self.invincible=False
                if self.endTime-self.startTime>=1:
                    self.display=False
            for tank in self.fuelTanks:
                self.boundsB=tank.getBounds()
                if self.boundsIntersect(self.boundsA,self.boundsB):
                    self.fuelTanks.remove(tank)
                    self.fuelGauge.width = self.fuelGauge.fullTank
                    pass
            self.handleBoulders()

            if self.lives<0:
                self.gameOver=True
            if self.destroyed:
                self.endDeadTime=time.time()
                if self.endDeadTime-self.startDeadTime>=2:
                    self.destroyed=False

            for boulder in self.boulders:
                if boulder.hit==False:
                    boulder.fall()
                boulder.checkHit(self.boulders)

            if self.x2>=self.pathLength-100:
                self.gameWon=True

            self.sideScroll()
    def handleBoulders(self):
        for boulder in self.boulders:
                self.boundsB=boulder.getBounds()
                if not self.invincible:
                    if self.boundsIntersect(self.boundsA,self.boundsB):
                        if self.lives>=0:
                           self.lives-=1
                        boulder.y=self.getY(boulder.x)-boulder.h

                        self.score-=100
                        boulder.hit=True
                        self.startDeadTime=time.time()
                        self.destroyed =True
                        self.speed=0
                        self.boulders.remove(boulder)
                        pass
                if boulder.y+boulder.h>=self.getY(boulder.x):
                    boulder.hit =True
                    boulder.hitCount+=1
                    self.rotateBoulder(boulder)
                    self.fallingBoulder(boulder)

    def sideScroll(self):
        if (self.x1< self.scrollX + self.scrollMargin):
            self.scrollX = self.x1 - self.scrollMargin

        if (self.x1 > self.scrollX + self.width - self.scrollMargin):
            self.scrollX = self.x1 - self.width + self.scrollMargin

    def moveCar(self):
        adjacent1=-(self.y2-self.y1)
        adjacent2=self.x2-self.x1
        self.slope=adjacent1/adjacent2
        self.angle= math.atan2(adjacent1,adjacent2)
        self.rotationAngle=math.degrees(self.angle)
        self.scale_x=math.cos(self.angle)
        self.scale_y=math.sin(self.angle)
        if self.lift!=True:
           self.checkForIntersection()
        self.velocity_x=self.speed*self.scale_x
        self.velocity_y=self.speed*self.scale_y
        self.speed=self.velocity_x
    def gravity(self):
        gravity=.2
        self.yCheck1=self.getY(self.x1)
        self.yCheck2=self.getY(self.x2)
        if self.y1<=self.yCheck1:
            self.y1+=gravity
        if self.y2<= self.yCheck2:
            self.y2+=gravity
    def rotateBoulder(self,boulder):
        boulder.y1=self.getY(boulder.x)
        boulder.y2=self.getY(boulder.x+boulder.w)
        boulder.x1=boulder.x
        boulder.x2=boulder.x+boulder.w
        boulder.adjacent1=-(boulder.y2-boulder.y1)
        boulder.adjacent2=boulder.x2-boulder.x1
        boulder.slope=boulder.adjacent1/boulder.adjacent2
        angle= math.atan2(boulder.adjacent1,boulder.adjacent2)
        boulder.rotationAngle=math.degrees(angle)
    def fallingBoulder(self,boulder):
        if  boulder.stopMoving==False:
            if boulder.slope<0:
                boulder.x+=4
            if boulder.slope>0:
                boulder.x-=4
        if boulder.slope<=.1 and boulder.slope>=-.1:
            boulder.stopMoving=True
        boulder.y=self.getY(boulder.x)-boulder.h

    def getRandomHeights(self,numHills):
        randomHeights=[]
        for i in range(0,numHills):
            randomHeight= random.random()*150
            randomHeights.append(randomHeight)
        return randomHeights

    def checkForIntersection(self):
        self.yCheck1=self.getY(self.x1)
        self.yCheck2=self.getY(self.x2)
        if self.y1+10>=self.yCheck1 or self.y2>=self.yCheck2:
            self.lift=False

    def createCoins(self):
        for x in range(self.pathLength):
            if x%500==0:
                if x%60==0:
                    for j in range(5):
                      y= self.getY(x+(j*30))-35
                      self.coins.append(Coins(x+(j*30),y))
                else:
                     for j in range(5):
                         y= self.getY(x+(j*30))-65
                         self.coins.append(Coins(x+(j*30),y))

    def placeFuel(self):
        for x in range(self.pathLength):
            if x%2450==0:
                y=self.getY(x)
                self.fuelTanks.append(FuelTank(x,y))

    def createHills(self):
        sx=self.scrollX
        numHills=self.numHills
        pixelStep=self.pixelStep
        pointList=[]

        hillWidth=(self.pathLength)/numHills
        hillSlices=hillWidth//pixelStep
        closed=True
        i=0
        for i in range(0,numHills):
            randomHeight= self.randomHeights[i]
            self.hills.append(Hills(randomHeight,i*hillWidth,(i+1)*hillWidth))

    def drawHills(self,screen,numHills,pixelStep):
        sx=self.scrollX
        hillStartY=self.hillStartY
        pointList=[]
        hillWidth=(self.pathLength)/numHills
        hillSlices=hillWidth//pixelStep
        closed=True
        brown=(139,69,19)
        green=(76,153,0)
        for i in range(0,numHills):
            randomHeight= self.randomHeights[i]
            self.hills.append(Hills(randomHeight,i*hillWidth,(i+1)*hillWidth))#create new instance of hill class
            if (i!=0):
                hillStartY-=randomHeight
            for j in range(0,int(hillSlices)+1):
                hillPoint= (int((j*pixelStep+hillWidth*i)-sx),
                   int(hillStartY+randomHeight*math.cos(2*math.pi/hillSlices*j)))
                previousHillPointx=int((j+1)*pixelStep+hillWidth*i-sx)

                previousHillPointy=int(hillStartY+randomHeight*math.cos(2*math.pi/hillSlices*(j+1)))

                screen.set_at((hillPoint),self.black)
                hillPointx=j*pixelStep+hillWidth*i-sx
                hillPointy=hillStartY+randomHeight*math.cos(2*math.pi/hillSlices*j)
                pointList.append(hillPoint)
                pygame.draw.polygon(screen,green,[(hillPointx,hillPointy),
                                    (hillPointx,800),
                                    ((j+1)*pixelStep+hillWidth*i-sx,800),
                                   (previousHillPointx,previousHillPointy)],0)
            if (i!=0):
                hillStartY+=randomHeight
            pygame.draw.lines(screen,brown,closed,pointList,6)
            pointList=[]
        pygame.draw.line(screen,green,(0,hillStartY),
                          (self.pathLength,hillStartY),5)

    def getY(self,x):
        hillStartY=self.hillStartY
        hillWidth=(self.pathLength)/self.numHills
        hillSlices=int(hillWidth/self.pixelStep)
        j=(x)/self.pixelStep
        for hill in self.hills:
            hillStartY-=hill.height
            height=hill.height
            if (x==hill.end):
                y=int(hillStartY+height*math.cos(2*math.pi/hillSlices*j))
            if (x>hill.start and x< hill.end):
                x=hill.start
                y=int(hillStartY+height*math.cos(2*math.pi/hillSlices*j))
                return y
            if (x==hill.start):
                 y=int(hillStartY+height*math.cos(2*math.pi/hillSlices*j))
            hillStartY=600
        return 600

    def getPlayerBounds(self):
        (x0, y1) =(self.x1, self.y1)
        (x1, y0) = (x0+self.w , y1-self.h)
        return (x0, y0, x1, y1)

    def boundsIntersect(self,boundsA, boundsB):
        (ax0, ay0, ax1, ay1) = boundsA
        (bx0, by0, bx1, by1) = boundsB
        return ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0))

    def rot_center(self,image,angle):
        rot_image = pygame.transform.rotate(image, angle)
        return rot_image

    def stats(self,screen):
        font=pygame.font.SysFont("euphemiaucas",40)
        if self.lives>=0:
            lives= font.render("LIVES:"+str(self.lives), True,(128,0,0))
            screen.blit(lives,(20,700))
        score=font.render("SCORE:"+str(self.score),True,(128,0,0))
        screen.blit(score,(520,700))
        speed=font.render("SPEED:"+str(abs(int((self.speed)))),True,(128,0,0))
        screen.blit(speed,(250,700))

    def drawWon(self,screen):
        purple=(153,0,153)
        pygame.draw.rect(screen,purple,(160,200,500,500))
        pygame.draw.rect(screen, self.white, (310,350,200,50),2)
        pygame.draw.rect(screen,self.white, (310,430,200,50),2)
        pygame.draw.rect(screen,self.black,(160,200,500,500),2)
        font=pygame.font.SysFont("euphemiaucas",50)
        over=font.render("YOU WON!", True,self.white)
        screen.blit(over,(270,270))
        font=pygame.font.SysFont("euphemiaucas",35)
        restart=font.render(" RESTART",True,self.white)
        screen.blit(restart,(340,350))
        quit1=font.render("QUIT",True,self.white)
        screen.blit(quit1,(375,430))
        font=pygame.font.SysFont("euphemiaucas",35)
        score=font.render("TOTAL SCORE: "+str(self.score),True,self.white)
        screen.blit(score,(260,540))

    def drawGameOver(self,screen):
        pygame.draw.rect(screen,self.tealColor,(160,200,500,500))
        pygame.draw.rect(screen, self.white, (310,350,200,50),2)
        pygame.draw.rect(screen,self.white, (310,430,200,50),2)
        pygame.draw.rect(screen,self.black,(160,200,500,500),2)
        font=pygame.font.SysFont("euphemiaucas",50)
        over=font.render("GAME OVER!", True,self.white)
        screen.blit(over,(270,270))
        font=pygame.font.SysFont("euphemiaucas",35)
        restart=font.render(" RESTART",True,self.white)
        screen.blit(restart,(340,350))
        quit1=font.render("QUIT",True,self.white)
        screen.blit(quit1,(375,430))
        font=pygame.font.SysFont("euphemiaucas",35)
        score=font.render("TOTAL SCORE: "+str(self.score),True,self.white)
        screen.blit(score,(260,540))

    def gameRedrawAll(self, screen):
        self.h=47.6
        self.flashingCount+=1
        color=(150,150,150)
        purple=(100,0,100)
        sx=self.scrollX
        screen.blit(self.gameBackground, (0,0))
        self.plane.draw(screen,self.scrollX)
        self.fuelGauge.draw(screen)
        rotatedImage=self.rot_center(self.car,self.rotationAngle)
        self.drawHills(screen,self.numHills,self.pixelStep)
        if self.invincible:
            truck=self.rot_center(self.invincibleCar,self.rotationAngle)
            screen.blit(truck, (int(self.x1-self.scrollX), self.y2-(self.h)))
            if self.display:
                font=pygame.font.SysFont("euphemiaucas",100)
                over=font.render("POWER UP", True,(0,204,0))
                screen.blit(over,(170,350))
        elif self.destroyed:
            if self.flashingCount%5==0:
                screen.blit(rotatedImage, (int(self.x1-self.scrollX),
                                           self.y2-(self.h)+12))

        else:
            screen.blit(rotatedImage, (int(self.x1-self.scrollX),
                                       self.y2-(self.h)+12))
        self.placeObjects(screen)

    def placeObjects(self,screen):
        for coin in self.coins:
            coin.draw(screen,self.scrollX)
        for tank in self.fuelTanks:
            tank.draw(screen,self.scrollX)
        for boulder in self.boulders:
            boulder.draw(screen,self.scrollX)

        w,h = self.finish.get_size()
        pygame.draw.rect(screen,(76,153,0),(0,self.hillStartY,self.width,800))
        screen.blit(self.finish, (self.pathLength-self.scrollX-50,
                                  self.hillStartY-h+100))
        self.stats(screen)
        if self.displayWarning:
            if self.flashingCount%10!=0:
                font=pygame.font.SysFont("euphemiaucas",100)

                warning=font.render("LOW FUEL",True,(255,0,0))
                screen.blit(warning,(170,350))
        font=pygame.font.SysFont("euphemiaucas",20)
        home=font.render(" HOME", True,self.tealColor)
        screen.blit(home,(720,20))
        pygame.draw.rect(screen,self.tealColor,(710,12,60,30),2)
        if self.gameOver:
           self.drawGameOver(screen)
        if self.gameWon:
           self.drawWon(screen)

class FuelGauge(Game):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.fullTank=200
        self.red=(255,0,0)
        self.height=12
        self.width=200
        self.fuel =pygame.image.load('D:/game/petrol.png').convert_alpha()
        self.w,self.h = self.fuel.get_size()
        self.w*=.3
        self.h*=.2
        self.black=(0,0,0)
    def draw(self,screen):
        width=200
        self.fuel = pygame.transform.scale(self.fuel, (int(self.w), int(self.h)))
        screen.blit(self.fuel, ((260), 15))
        pygame.draw.rect(screen,self.black,(self.x,self.y,
                               self.x+width,self.y+self.height))
        pygame.draw.rect(screen,self.red,(self.x,self.y,
                            self.x+self.width,self.y+self.height))
        pygame.draw.rect(screen,self.black,(self.x,self.y,
                               self.x+width,self.y+self.height),3)

class Coins(Game):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.coin = pygame.image.load(r'D:/game/coin.png').convert_alpha()
        self.w,self.h = self.coin.get_size()
        self.w*=.04
        self.h*=.04
        self.hit=False

    def draw(self,screen,sx):
        self.coin = pygame.transform.scale(self.coin, (int(self.w), int(self.h)))

        screen.blit(self.coin, ((self.x-sx), self.y))
    def getBounds(self):
        (x0, y1) =(self.x, self.y)
        (x1, y0) = (x0+self.w , y1 -self.h)
        return (x0, y0, x1, y1)

class Hills(Game):
    def __init__(self,height,start,end):
        self.height=height
        self.start=start
        self.end=end

class FuelTank(Game):
    def __init__(self,x,y):
        self.x=x
        self.fuel = pygame.image.load('D:/game/petrol.png').convert_alpha()
        self.w,self.h = self.fuel.get_size()
        self.w*=.3
        self.h*=.3
        self.y=y-self.h
    def draw(self,screen,sx):
        self.fuel = pygame.transform.scale(self.fuel, (int(self.w),
                                                       int(self.h)))
        screen.blit(self.fuel, ((self.x-sx), self.y))
    def getBounds(self):
        (x0, y1) =(self.x, self.y)
        (x1, y0) = (x0+self.w , y1 -self.h)
        return (x0, y0, x1, y1)

class Boulder(Game):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.boulder = pygame.image.load('D:/game/boulder.png').convert_alpha()
        self.w,self.h = self.boulder.get_size()
        self.w*=.1
        self.h*=.1
        self.move=False
        self.speed=0
        self.speedX=0
        self.hit=False
        self.hitCount=0
        self.rotationAngle=0
        self.speedX=0
        self.stopMoving=False

    def draw(self,screen,sx):
        self.boulder = pygame.transform.scale(self.boulder, (int(self.w),
                                                             int(self.h)))
        rotatedImage2=self.rot_center(self.boulder,self.rotationAngle)
        screen.blit(rotatedImage2, ((self.x-sx), self.y))
    def fall(self):
        increment=5
        self.speed+=increment
        self.y+=self.speed
    def checkHit(self,boulders):
        if self.hitCount>=50:
            boulders.remove(self)
    def getBounds(self):
        (x0, y1) =(self.x, self.y)
        (x1, y0) = (x0+self.w , y1 -self.h)
        return (x0, y0, x1, y1)

class Plane(Game):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.plane= pygame.image.load('D:/game/plane.png').convert_alpha()
        self.w,self.h = self.plane.get_size()
        self.w*=.2
        self.h*=.2
        self.speed=0
        self.maxSpeed=400
        self.buffer=100

    def draw(self,screen,sx):
        self.plane = pygame.transform.scale(self.plane,
                                    (int(self.w), int(self.h)))
        screen.blit(self.plane, ((self.x-sx), self.y))
    def move(self,carx1):
        self.x+=self.speed
        increment=.4
        distance= self.x-carx1
        if distance>self.buffer:
            if self.speed>0:
                self.speed-=increment
        if distance<-self.buffer:
            if self.speed<=self.maxSpeed:
                self.speed+=increment
game1=Game(800,730)
game1.run()
pygame.quit()