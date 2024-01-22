import pygame
import math

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
        self.thetas = [(self.theta-self.fovHalf+self.cst*i)%(2*math.pi) for i in range(self.numbOfRays)]

        #not important, used to debug ray casting
        self.colorRayCasting = []
        #########################################
        
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
        speed_cos = self.run*self.speed*math.cos(self.theta)
        speed_sin = self.run*self.speed*math.sin(self.theta)
        self.thetas = [(self.theta-self.fovHalf+self.cst*i) for i in range(self.numbOfRays)]
        if math.floor(self.playerPosY + self.dy[0]*speed_sin+self.dy[1]*speed_cos) >= 0 and math.floor(self.playerPosY + self.dy[0]*speed_sin+self.dy[1]*speed_cos) <= len(matMap)-1 and math.floor(self.playerPosX + self.dx[0]*speed_sin+self.dx[1]*speed_cos) >= 0 and math.floor(self.playerPosX + self.dx[0]*speed_sin+self.dx[1]*speed_cos) <= len(matMap[0])-1 :
            try :
                if matMap[math.floor(self.playerPosY+self.dy[0]*speed_sin+self.dy[1]*speed_cos)][math.floor(self.playerPosX)] == 0 :
                    self.playerPosY += self.dy[0]*speed_sin+self.dy[1]*speed_cos
            except :
                pass
            try :
                if matMap[math.floor(self.playerPosY)][math.floor(self.playerPosX+self.dx[0]*speed_sin+self.dx[1]*speed_cos)] == 0 :
                    self.playerPosX += self.dx[0]*speed_sin+self.dx[1]*speed_cos
            except:
                pass
        else:
            self.playerPosY += self.dy[0]*speed_sin+self.dy[1]*speed_cos
            self.playerPosX += self.dx[0]*speed_sin+self.dx[1]*speed_cos
        
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
        ray_imp = 0.03
        distances = [0.03 for i in range(self.numbOfRays)]
        i=0
        colors = []
        for theta in self.thetas:
            is_wall_bool = False
            xStep = ray_imp*math.cos(theta)
            yStep = ray_imp*math.sin(theta)
            watchX = self.playerPosX
            watchY = self.playerPosY
            while not is_wall_bool and distances[i]<30 :
                watchX += xStep
                watchY += yStep
                if math.floor(watchX) >= 0 and math.floor(watchY) >= 0 and math.floor(watchX) < len(matMap[0]) and math.floor(watchY) < len(matMap):
                    if matMap[math.floor(watchY)][math.floor(watchX)] == 1:
                        is_wall_bool = True

                distances[i] += ray_imp

            if distances[i] >= 30:
                distances[i] = False
            else :
                distances[i] *= abs(math.cos(self.theta-theta)) # abs(math.cos(self.theta-theta)) makes walls less rounded in 2.5D (will reduce distances in 2D)
                
            i+=1

            #not important, used to debug ray casting
            colors.append((0,255,255))
            #########################################

        #not important, used to debug ray casting
        self.colorRayCasting = colors
        #########################################

        return distances

    def rayCasting(self, matMap):
        distances = []
        colors = []
        for theta in self.thetas:

            signe_x = round(abs(math.cos(theta))/(math.cos(theta)+0.001))
            signe_y = round(abs(math.sin(theta))/(math.sin(theta)+0.001))

            verif_x = 1-self.playerPosX%1
            verif_y = math.tan(theta)*verif_x
            distance_h = math.sqrt((verif_x)**2 + (verif_y)**2)
            is_wall_bool = self.isWall(matMap, round(self.playerPosX + verif_x), math.floor(self.playerPosY + verif_y))
            while not is_wall_bool and distance_h<20:
                verif_x += 1
                verif_y += math.tan(theta)
                is_wall_bool = self.isWall(matMap, round(self.playerPosX + verif_x), math.floor(self.playerPosY + verif_y))
                distance_h = math.sqrt((verif_x)**2 + (verif_y)**2)
    
            verif_y = 1-self.playerPosY%1
            verif_x = (verif_y) / (math.tan(theta)+0.0001)
            distance_v = math.sqrt((verif_x)**2 + (verif_y)**2)
            is_wall_bool = self.isWall(matMap, math.floor(self.playerPosX + verif_x), round(self.playerPosY + verif_y))
            while not is_wall_bool and distance_v<20 :
                verif_y += 1
                verif_x += 1 / (math.tan(theta)+0.0001)
                is_wall_bool = self.isWall(matMap, math.floor(self.playerPosX + verif_x), round(self.playerPosY + verif_y))
                distance_v = math.sqrt((verif_x)**2 + (verif_y)**2)

            #not important, used to debug ray casting
            if min(distance_h, distance_v) == distance_v:
                colors.append((255,0,255))
            else:
                colors.append((0,255,0))
            #########################################

            distances.append(min(distance_h, distance_v)*abs(math.cos(self.theta-theta))) # abs(math.cos(self.theta-theta)) makes walls less rounded in 2.5D (will reduce distances in 2D)
        
        #not important, used to debug ray casting
        self.colorRayCasting = colors
        #########################################

        return distances
    

    def getHeightVisu(self):
        return self.heightVisu
    
    def getFov(self):
        return self.fov