import pygame
import math

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