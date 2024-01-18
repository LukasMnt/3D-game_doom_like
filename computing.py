import math
from sys import exit
import pygame

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
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
    def updateMap():
        pass
    
    def changeMap():
        pass

class Player():
    def __init__(self):
        self.playerPosX = 2
        self.playerPosY = 2
        self.dx = [0,0]
        self.dy = [0,0]
        self.theta = 45   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top (on the matMap)
        self.dt = 0
        self.initSpeed = 0.03
        self.speed = self.initSpeed
        self.run = 1
        self.circSpeed = 3
        
        self.playerPosZ = 0
        self.heightVisu = 0
        
        self.fov = 60/2
        self.numbOfRays = 101
        self.cst = 2*self.fov/(self.numbOfRays-1)
        self.thetas = [(self.theta-self.fov+self.cst*i)*math.pi/180 for i in range(self.numbOfRays)]
        self.theta2 = self.theta*math.pi/180
        
    def updateOnEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.dx = [self.dx[0],self.dx[1]+1]
                self.dy = [self.dy[0]+1,self.dy[1]]
            if event.key == pygame.K_s:
                self.dx = [self.dx[0],self.dx[1]-1]
                self.dy = [self.dy[0]-1,self.dy[1]]
            if event.key == pygame.K_a:
                self.dx = [self.dx[0]-1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]+1]
            if event.key == pygame.K_d:
                self.dx = [self.dx[0]+1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]-1]
            if event.key == pygame.K_RIGHT :
                self.dt += self.circSpeed
            if event.key == pygame.K_LEFT :
                self.dt -= self.circSpeed
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
            if event.key == pygame.K_LSHIFT :
                self.run *= 2
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT :
                self.dt -= self.circSpeed
            if event.key == pygame.K_LEFT :
                self.dt += self.circSpeed
            if event.key == pygame.K_w:
                self.dx = [self.dx[0],self.dx[1]-1]
                self.dy = [self.dy[0]-1,self.dy[1]]
            if event.key == pygame.K_s:
                self.dx = [self.dx[0],self.dx[1]+1]
                self.dy = [self.dy[0]+1,self.dy[1]]
            if event.key == pygame.K_a:
                self.dx = [self.dx[0]+1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]-1]
            if event.key == pygame.K_d:
                self.dx = [self.dx[0]-1,self.dx[1]]
                self.dy = [self.dy[0],self.dy[1]+1]
            if event.key == pygame.K_LSHIFT :
                self.run /= 2
    
    def updateMouv(self, myMap):
        self.theta += self.dt
        self.theta = self.theta%360
        self.theta2 = self.theta*math.pi/180
        
        speedCos = self.run*self.speed*math.cos(self.theta2)
        speedSin = self.run*self.speed*math.sin(self.theta2)
        if myMap.matMap[math.floor(self.playerPosX + self.dx[0]*speedCos+self.dx[1]*speedSin)][math.floor(self.playerPosY)]!=1 :
            self.playerPosX+= self.dx[0]*speedCos+self.dx[1]*speedSin
        if myMap.matMap[math.floor(self.playerPosX)][math.floor(self.playerPosY + self.dy[0]*speedCos+self.dy[1]*speedSin)]!=1 :
            self.playerPosY+= self.dy[0]*speedCos+self.dy[1]*speedSin
        
        if self.playerPosZ > 0:
            self.playerPosZ -= 14
            
        if self.heightVisu < self.playerPosZ:
            self.heightVisu += 14
        elif self.heightVisu > self.playerPosZ:
            self.heightVisu -= 8

        

#displayPart
def displayWalls(d, screen):
    numbOfSlices = len(d)
    walls = [pygame.Surface((math.ceil(screen.get_width()/numbOfSlices),2*800/d[i])) for i in range(numbOfSlices)]
    for wall in walls:
        wall.fill("#8B4009")
    return walls

#rayPart
def distanceR(playerPosX, playerPosY, matMap, thetas, numbOfRays):
    i=0
    rayImp = 0.01
    distances = [0.1 for i in range(numbOfRays)]
    for theta in thetas:
        isWall = False
        xUp = rayImp*math.cos(theta)
        yUp = rayImp*math.sin(theta)
        watchX = playerPosY
        watchY = playerPosX
        while not isWall :
            distances[i] += rayImp
            watchX += xUp
            watchY += yUp
            if matMap[math.floor(watchY)][math.floor(watchX)] == 1:
                isWall = True
        i+=1
    return distances


def main():
    myMap = Maps()
    myPlayer = Player()
    
    d = distanceR(myPlayer.playerPosX,myPlayer.playerPosY, myMap.matMap, myPlayer.thetas, myPlayer.numbOfRays)
    
    #displayPart
    pygame.init()
    
    #invisible cursor
    pygame.mouse.set_visible(False)
    width=pygame.display.Info().current_w
    height=pygame.display.Info().current_h
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Doom_like")
    clock = pygame.time.Clock()
    
    bgTop = pygame.Surface((width,height))
    bgTop.fill("#00F3FF")
    bgBot = pygame.Surface((width,height))
    bgBot.fill("#10AF08")
    
    crosshairV = pygame.Surface((2,16))
    crosshairV.fill("#FF0000")
    crosshairH = pygame.Surface((16,2))
    crosshairH.fill("#FF0000")
    
    walls = displayWalls(d, screen)
    
    while True:
        #update
        d = distanceR(myPlayer.playerPosX,myPlayer.playerPosY, myMap.matMap, myPlayer.thetas, myPlayer.numbOfRays)
        myPlayer.thetas = [(myPlayer.theta-myPlayer.fov+myPlayer.cst*i)*math.pi/180 for i in range(myPlayer.numbOfRays)]
        walls = displayWalls(d, screen)
        
        for event in pygame.event.get():
            #if we press the red cross
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            myPlayer.updateOnEvent(event)
        
        myPlayer.updateMouv(myMap)
        
        #print screen
        screen.blit(bgTop, (0,-screen.get_height()//2+ myPlayer.heightVisu))
        screen.blit(bgBot, (0,screen.get_height()//2+ myPlayer.heightVisu))
        for i in range(len(walls)):
            x = i*screen.get_width()/len(walls)
            y = screen.get_height()//2 - walls[i].get_height() // 2 + myPlayer.heightVisu
            screen.blit(walls[i], (x,y))
        
        screen.blit(crosshairV, ((screen.get_width()-crosshairV.get_width())//2,(screen.get_height()-crosshairV.get_height())//2))
        screen.blit(crosshairH, ((screen.get_width()-crosshairH.get_width())//2,(screen.get_height()-crosshairH.get_height())//2))
        
        pygame.display.update()
        clock.tick(60)
    
main()