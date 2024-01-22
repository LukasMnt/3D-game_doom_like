import math
from sys import exit
import pygame

#for fps mainly (only this for the moment but I may forget to update the message):
import time
import heapq

class Maps():
    def __init__(self):
        self.matMap=   [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
                        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                        [1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
    def getMap(self):
        return self.matMap
    
    def updateMap():
        pass
    
    def changeMap():
        pass

class Player():
    def __init__(self):
        self.playerPosX = 4
        self.playerPosY = 2
        self.dx = [0,0]
        self.dy = [0,0]
        self.initSpeed = 0.03
        self.speed = self.initSpeed
        self.run = 1
        
        self.playerPosZ = 0
        self.heightVisu = 0
        
        self.theta = 0   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top (on the matMap)
        self.dt = 0
        self.circSpeed = math.pi/90
        
        self.fov = math.pi/2
        self.fovHalf = self.fov/2
        self.numbOfRays = 400
        self.cst = self.fov/(self.numbOfRays-1)
        self.thetas = [(self.theta-self.fovHalf+self.cst*i) for i in range(self.numbOfRays)]

        self.colorRayCasting = []
        
    def updateOnEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.dx = [self.dx[0],self.dx[1]+1]
                self.dy = [self.dy[0]+1,self.dy[1]]
            if event.key == pygame.K_a:
                self.dx = [self.dx[0]+1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]-1]
            if event.key == pygame.K_s:
                self.dx = [self.dx[0],self.dx[1]-1]
                self.dy = [self.dy[0]-1,self.dy[1]]
            if event.key == pygame.K_d:
                self.dx = [self.dx[0]-1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]+1]

            if event.key == pygame.K_RIGHT :
                self.dt += self.circSpeed
            if event.key == pygame.K_LEFT :
                self.dt -= self.circSpeed

            if event.key == pygame.K_LSHIFT :
                self.run *= 2

            if event.key == pygame.K_LCTRL :
                if self.playerPosZ == 0:
                    self.playerPosZ = -96
                    self.speed /= 4
                elif self.playerPosZ < 0:
                    self.playerPosZ = 0
                    self.speed = self.initSpeed
            elif event.key == pygame.K_SPACE :
                if self.playerPosZ == 0 and self.heightVisu == 0:
                    self.playerPosZ = 420
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.dx = [self.dx[0],self.dx[1]-1]
                self.dy = [self.dy[0]-1,self.dy[1]]
            if event.key == pygame.K_a:
                self.dx = [self.dx[0]-1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]+1]
            if event.key == pygame.K_s:
                self.dx = [self.dx[0],self.dx[1]+1]
                self.dy = [self.dy[0]+1,self.dy[1]]
            if event.key == pygame.K_d:
                self.dx = [self.dx[0]+1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]-1]

            if event.key == pygame.K_RIGHT :
                self.dt -= self.circSpeed
            if event.key == pygame.K_LEFT :
                self.dt += self.circSpeed
            
            if event.key == pygame.K_LSHIFT :
                self.run /= 2
    
    def updateMov(self, matMap):
        self.theta = (self.theta + self.dt)%(2*math.pi)
        speedCos = self.run*self.speed*math.cos(self.theta)
        speedSin = self.run*self.speed*math.sin(self.theta)
        self.thetas = [(self.theta-self.fovHalf+self.cst*i) for i in range(self.numbOfRays)]
        if math.floor(self.playerPosY + self.dy[0]*speedSin+self.dy[1]*speedCos) >= 0 and math.floor(self.playerPosY + self.dy[0]*speedSin+self.dy[1]*speedCos) <= len(matMap)-1 and math.floor(self.playerPosX + self.dx[0]*speedSin+self.dx[1]*speedCos) >= 0 and math.floor(self.playerPosX + self.dx[0]*speedSin+self.dx[1]*speedCos) <= len(matMap[0])-1 :
            try :
                if matMap[math.floor(self.playerPosY+self.dy[0]*speedSin+self.dy[1]*speedCos)][math.floor(self.playerPosX)] == 0 :
                    self.playerPosY += self.dy[0]*speedSin+self.dy[1]*speedCos
            except :
                pass
            try :
                if matMap[math.floor(self.playerPosY)][math.floor(self.playerPosX+self.dx[0]*speedSin+self.dx[1]*speedCos)] == 0 :
                    self.playerPosX += self.dx[0]*speedSin+self.dx[1]*speedCos
            except:
                pass
        else:
            self.playerPosY += self.dy[0]*speedSin+self.dy[1]*speedCos
            self.playerPosX += self.dx[0]*speedSin+self.dx[1]*speedCos
        
        if self.playerPosZ > 0:
            self.playerPosZ -= 14

        if self.heightVisu < self.playerPosZ:
            self.heightVisu += 14
        elif self.heightVisu > self.playerPosZ:
            self.heightVisu -= 8

    def isWall(self, matMap, x, y):
        try:
            return matMap[y][x] == 1
        except:
            return False


    # ray casting (not optimised at all)
    def distancesD(self, matMap):
        rayImp = 0.03
        distances = [0.03 for i in range(self.numbOfRays)]
        i=0
        colors = []
        for theta in self.thetas:
            isWallBool = False
            xStep = rayImp*math.cos(theta)
            yStep = rayImp*math.sin(theta)
            watchX = self.playerPosX
            watchY = self.playerPosY
            while not isWallBool and distances[i]<30 :
                watchX += xStep
                watchY += yStep
                if math.floor(watchX) >= 0 and math.floor(watchY) >= 0 and math.floor(watchX) < len(matMap[0]) and math.floor(watchY) < len(matMap):
                    if matMap[math.floor(watchY)][math.floor(watchX)] == 1:
                        isWallBool = True

                distances[i] += rayImp

            if distances[i] >= 30:
                distances[i] = False
                
            i+=1
            colors.append((0,255,255))
        return distances, colors

    def rayCasting(self, matMap):
        distances = []
        colors = []
        for theta in self.thetas:
            verif_x = 1-self.playerPosX%1
            verif_y = math.tan(theta)*verif_x
            distance_H = math.sqrt((verif_x)**2 + (verif_y)**2)
            isWallBool = self.isWall(matMap, round(self.playerPosX + verif_x), math.floor(self.playerPosY + verif_y))
            while not isWallBool and distance_H<20:
                verif_x += 1
                verif_y += math.tan(theta)
                isWallBool = self.isWall(matMap, round(self.playerPosX + verif_x), math.floor(self.playerPosY + verif_y))
                distance_H = math.sqrt((verif_x)**2 + (verif_y)**2)
    
            verif_y = 1-self.playerPosY%1
            verif_x = verif_y / (math.tan(theta)+0.0001)
            distance_V = math.sqrt((verif_x)**2 + (verif_y)**2)
            isWallBool = self.isWall(matMap, math.floor(self.playerPosX + verif_x), round(self.playerPosY + verif_y))
            while not isWallBool and distance_V<20 :
                verif_y += 1
                verif_x += 1 / (math.tan(theta)+0.0001)
                isWallBool = self.isWall(matMap, math.floor(self.playerPosX + verif_x), round(self.playerPosY + verif_y))
                distance_V = math.sqrt((verif_x)**2 + (verif_y)**2)

            if min(distance_H, distance_V) == distance_V:
                colors.append((255,0,0))
            else:
                colors.append((0,255,0))

            distances.append(min(distance_H, distance_V))
        return distances, colors
    

    def getHeightVisu(self):
        return self.heightVisu
    
    def getFov(self):
        return self.fov

class PrintableObjects():
    def __init__(self):
        #invisible cursor
        pygame.mouse.set_visible(False)
        
        self.displayWidth=pygame.display.Info().current_w
        self.displayHeight=pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.displayWidth,self.displayHeight))
        
        self.bgTop = pygame.Surface((self.displayWidth,self.displayHeight))
        self.bgTop.fill("#00F3FF")
        self.bgBot = pygame.Surface((self.displayWidth,self.displayHeight))
        self.bgBot.fill("#10AF08")
        
        self.crosshairV = pygame.Surface((2,16))
        self.crosshairV.fill("#FF0000")
        self.crosshairH = pygame.Surface((16,2))
        self.crosshairH.fill("#FF0000")
        
        self.showFPS = True
        
    def computeWalls(self, allDists, fov):
        numbOfSlices = len(allDists)
        self.walls = []
        for i in range(numbOfSlices):
            if allDists[i] != False:
                wallWidth = math.ceil(self.displayWidth/numbOfSlices)
                #My way :
                #wallHeigh = 1600/allDists[i]
                #chatGPT's way (after 1 hour of tries, no joke) (bard is quite a failure and GPT in bing is... WHY DOES HE SPEAKS SPANNISH TO ME ????? (no joke the title of the question was spanish))
                wallHeigh = self.displayHeight / (math.tan(fov/2) * allDists[i])
                
                wall = pygame.Surface((wallWidth, wallHeigh))
                wall.fill("#8B4009")
            else :
                wall = pygame.Surface((math.ceil(self.displayWidth/numbOfSlices), self.displayHeight/2), pygame.SRCALPHA, 32)
                wall = wall.convert_alpha()
            
            self.walls.append(wall)
            
    def draw(self, heightVisu, fps, PL):
        #first, draw the backgroud
        self.screen.blit(self.bgTop, (0,-self.displayHeight//2+ heightVisu))
        self.screen.blit(self.bgBot, (0,self.displayHeight//2+ heightVisu))
        
        #then, draw the wlls (upgrade to print them from back to front)
        for i in range(len(self.walls)):
            x = i*self.screen.get_width()/len(self.walls)
            y = self.screen.get_height()//2 - self.walls[i].get_height() // 2 + heightVisu
            self.screen.blit(self.walls[i], (x,y))
        
        if self.showFPS :
            self.displayFPS(fps)
            self.displayFPS(PL)
        
        #end, print the crosshair
        self.screen.blit(self.crosshairV, ((self.screen.get_width()-self.crosshairV.get_width())//2,(self.screen.get_height()-self.crosshairV.get_height())//2))
        self.screen.blit(self.crosshairH, ((self.screen.get_width()-self.crosshairH.get_width())//2,(self.screen.get_height()-self.crosshairH.get_height())//2))
        
        pygame.display.update()

    def draw2D(self, myPlayer, matMap, allDists):
        pygame.draw.rect(self.screen, (0,0,0), (0, 0, self.screen.get_width(), self.screen.get_height()))
        for x in range(len(matMap[0])):
            for y in range(len(matMap)):
                if matMap[y][x] == 1:
                    mySurface = pygame.Surface((20,20))
                    mySurface.fill((255,0,0))
                    self.screen.blit(mySurface, (x*20, y*20))

        for i in range(len(myPlayer.thetas)):
            pygame.draw.line(self.screen, myPlayer.colorRayCasting[i], (myPlayer.playerPosX*20, myPlayer.playerPosY*20), (20 * (myPlayer.playerPosX + allDists[i]*math.cos(myPlayer.thetas[i])), 20 * (myPlayer.playerPosY + allDists[i]*math.sin(myPlayer.thetas[i]))))

        pygame.draw.line(self.screen, (0,0,255), (myPlayer.playerPosX*20, myPlayer.playerPosY*20), (20*(myPlayer.playerPosX + 20*math.cos(myPlayer.theta)), 20*(myPlayer.playerPosY + 20*math.sin(myPlayer.theta))))
        pygame.draw.circle(self.screen, (255,0,255), (myPlayer.playerPosX*20, myPlayer.playerPosY*20), 10)

        pygame.display.update()

        
    def displayFPS(self,fpsInf) :
        if False :
            path = "Documents/3-prog/Python/3D-game_doom_like/BradBunR.ttf"
        else :
            path = "BradBunR.ttf"
        font = pygame.font.Font(path,fpsInf[1])
        img = font.render(fpsInf[0],True,(150,150,150))
        displayRect = img.get_rect()
        displayRect.center=(fpsInf[2],fpsInf[3])
        self.screen.blit(img,displayRect)

    def areFPS(self):
        return self.showFPS

def main():
    #initialise
    pygame.init()
    pygame.display.set_caption("Doom_like")
    clock = pygame.time.Clock()
    
    gameLoop(clock)
    

def gameLoop(clock):
    myMap = Maps()
    myPlayer = Player()
    printObj = PrintableObjects()
    fps = []
    meanFPS = 1
    mean1PL = 0
    t = [time.time(),0]
    
    while True:

        #update
        allDists, myPlayer.colorRayCasting = myPlayer.rayCasting(myMap.getMap())
        printObj.computeWalls(allDists, myPlayer.getFov())
        #compute
        for event in pygame.event.get():
            #if we press the red cross
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #gesture of arrows and keys (mouse in the future)
            myPlayer.updateOnEvent(event)
        #mov
        myPlayer.updateMov(myMap.getMap())
        


        #print screen
        #printObj.draw(myPlayer.getHeightVisu(), ["FPS : " + str(meanFPS), 100, 150, 50],["1% : " + str(mean1PL), 50,75, 125])
        printObj.draw2D(myPlayer,myMap.getMap(), allDists)
        
        if printObj.areFPS():
            t[1]=time.time()
            fps.append(1/(t[1]-t[0]))
            store = 600
            if len(fps) > store:
                fps.pop(0)
            meanFPS = math.floor(sum(fps)/len(fps))
            PL = heapq.nsmallest(math.floor(store/100), fps)
            mean1PL = math.floor(sum(PL)/len(PL))
            t[0] = t[1]
            
        clock.tick(60)
main()

"""
What to improve ?
    Moving in diagonal doubles the speed (or time sqrt(2) idk)
    Looks a bit too rounded (infinit norme while computing allDists ?)
    Textures must be 
    Look up and down
    Add mouse controll
"""