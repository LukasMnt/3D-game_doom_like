import pygame
import math

class PrintableObjects():
    def __init__(self):
        # invisible cursor
        pygame.mouse.set_visible(False)
        
        # collecting user informations for the screen size
        self.displayWidth=pygame.display.Info().current_w
        self.displayHeight=pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.displayWidth,self.displayHeight))
        
        # just the temporar 'gound' and 'sky'
        self.bgTop = pygame.Surface((self.displayWidth,self.displayHeight))
        self.bgTop.fill("#00F3FF")
        self.bgBot = pygame.Surface((self.displayWidth,self.displayHeight))
        self.bgBot.fill("#10AF08")
        
        # simple crosshair
        self.crosshairV = pygame.Surface((2,16))
        self.crosshairV.fill("#FF0000")
        self.crosshairH = pygame.Surface((16,2))
        self.crosshairH.fill("#FF0000")
        
        # do you wanna have FPS shown on your screen ?
        self.show_FPS = True
        
    def compute_walls(self, allDists, fov):
        numbOfSlices = len(allDists)
        self.walls = []

        # for each wall, attribute it a size in function of the distance (if it exists of course)
        for i in range(numbOfSlices):
            # if there is a wall on this slice
            if allDists[i]:
                wallWidth = math.ceil(self.displayWidth/numbOfSlices)
                # My way :
                # wallHeigh = 1600/allDists[i]
                # chatGPT's way (after 1 hour of tries, no joke) (bard is quite a failure and GPT in bing is... WHY DOES HE SPEAK SPANNISH TO ME ????? (no joke the title of the question was spanish))
                wallHeigh = self.displayHeight / ((math.tan(fov/2) * allDists[i])+0.01)
                
                # creation of a simple wall, texture is basic for the moment
                wall = pygame.Surface((wallWidth, wallHeigh))
                wall.fill("#8B4009")
            else :
                # creation of an invisible wall
                wall = pygame.Surface((math.ceil(self.displayWidth/numbOfSlices), self.displayHeight/2), pygame.SRCALPHA, 32)
                wall = wall.convert_alpha()
            
            self.walls.append(wall)
            
    def draw(self, heightVisu, fps, percent_low):
        # first, draw the backgroud
        self.screen.blit(self.bgTop, (0,-self.displayHeight//2+ heightVisu))
        self.screen.blit(self.bgBot, (0,self.displayHeight//2+ heightVisu))
        
        # then, draw the wlls (upgrade to print them from back to front)
        for i in range(len(self.walls)):
            x = i*self.screen.get_width()/len(self.walls)
            y = self.screen.get_height()//2 - self.walls[i].get_height() // 2 + heightVisu
            self.screen.blit(self.walls[i], (x,y))
        
        # display the FPS if wanted
        if self.show_FPS :
            self.display_FPS(fps)
            self.display_FPS(percent_low)
        
        # end, print the crosshair
        self.screen.blit(self.crosshairV, ((self.screen.get_width()-self.crosshairV.get_width())//2,(self.screen.get_height()-self.crosshairV.get_height())//2))
        self.screen.blit(self.crosshairH, ((self.screen.get_width()-self.crosshairH.get_width())//2,(self.screen.get_height()-self.crosshairH.get_height())//2))
        
        pygame.display.update()

    def draw_2D(self, myPlayer, matMap, allDists):
        # background
        pygame.draw.rect(self.screen, (0,0,0), (0, 0, self.screen.get_width(), self.screen.get_height()))

        # the map
        for x in range(len(matMap[0])):
            for y in range(len(matMap)):
                if matMap[y][x] == 1:
                    mySurface = pygame.Surface((20,20))
                    mySurface.fill((255,0,0))
                    self.screen.blit(mySurface, ((x+2)*20, (y+2)*20))   # +2 is to have a small bordure

        # draw every single ray of the ray casting
        for i in range(len(myPlayer.thetas)):
            pygame.draw.line(self.screen, ((255,255,0)), ((2 + myPlayer.playerPosX)*20, (2 + myPlayer.playerPosY)*20), (20 * (2 + myPlayer.playerPosX + allDists[i]*math.cos(myPlayer.thetas[i])), 20 * (2 + myPlayer.playerPosY + allDists[i]*math.sin(myPlayer.thetas[i]))))

        # draw the ray that indicates player's looking direction
        pygame.draw.line(self.screen, (0,0,255), ((2 + myPlayer.playerPosX)*20, (2 + myPlayer.playerPosY)*20), (20*(2 + myPlayer.playerPosX + 20*math.cos(myPlayer.theta)), 20*(2 + myPlayer.playerPosY + 20*math.sin(myPlayer.theta))))
        # draw the player
        pygame.draw.circle(self.screen, (255,0,255), ((2 + myPlayer.playerPosX)*20, (2 + myPlayer.playerPosY)*20), 10)
        
        pygame.display.update()

        
    def display_FPS(self,fpsInf) :
        # font
        path = "BradBunR.ttf"
        font = pygame.font.Font(path,fpsInf[1])         # import font with the specified size
        img = font.render(fpsInf[0],True,(150,150,150)) # image of the text with font and color
        displayRect = img.get_rect()                    # get the rect equivalent of this image
        displayRect.center=(fpsInf[2],fpsInf[3])        # chose the coordinates where to draw
        self.screen.blit(img,displayRect)               # draw

    def are_FPS(self):
        return self.show_FPS