import pygame
import math

class Player():
    def __init__(self):
        self.playerPosX = 4
        self.playerPosY = 2
        self.dx = [0,0]
        self.dy = [0,0]
        self.init_speed = 0.03
        self.speed = self.init_speed
        self.run = 1
        
        self.playerPosZ = 0
        self.heightVisu = 0
        
        self.theta = 0   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top (on the matMap)
        self.dt = 0
        self.circSpeed = math.pi/90
        
        self.fov = math.pi/2
        self.fovHalf = self.fov/2
        self.numbOfRays = 401
        self.cst = self.fov/(self.numbOfRays-1)
        self.thetas = [(self.theta-self.fovHalf+self.cst*i)%(2*math.pi) for i in range(self.numbOfRays)]
        self.vision_range = 20
        
    def update_on_event(self, event):
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
    
    def update_mov(self, matMap):
        self.theta = (self.theta + self.dt)%(2*math.pi)
        self.thetas = [(self.theta-self.fovHalf+self.cst*i) for i in range(self.numbOfRays)]

        speed_cos = self.run*self.speed*math.cos(self.theta)
        speed_sin = self.run*self.speed*math.sin(self.theta)

        up_x = 0
        up_y = 0

        sign_dx = abs(self.dx[0]*speed_sin+self.dx[1]*speed_cos)/(self.dx[0]*speed_sin+self.dx[1]*speed_cos + 0.000001)
        sign_dy = abs(self.dy[0]*speed_sin+self.dy[1]*speed_cos)/(self.dy[0]*speed_sin+self.dy[1]*speed_cos + 0.000001)
        dist_player_walls = 0.1
        
        #if player moving in the map
        if math.floor(self.playerPosY + self.dy[0]*speed_sin+self.dy[1]*speed_cos) >= 0 and math.floor(self.playerPosY + self.dy[0]*speed_sin+self.dy[1]*speed_cos) <= len(matMap)-1 and math.floor(self.playerPosX + self.dx[0]*speed_sin+self.dx[1]*speed_cos) >= 0 and math.floor(self.playerPosX + self.dx[0]*speed_sin+self.dx[1]*speed_cos) <= len(matMap[0])-1 :
            
            #must try because if player has to stay out of the map, not working
            try :
                if matMap[math.floor(self.playerPosY+self.dy[0]*speed_sin+self.dy[1]*speed_cos + sign_dy*dist_player_walls)][math.floor(self.playerPosX)] == 0 :
                    up_y += self.dy[0]*speed_sin+self.dy[1]*speed_cos
            except :
                pass
            try :
                if matMap[math.floor(self.playerPosY)][math.floor(self.playerPosX+self.dx[0]*speed_sin+self.dx[1]*speed_cos + sign_dx*dist_player_walls)] == 0 :
                    up_x += self.dx[0]*speed_sin+self.dx[1]*speed_cos
            except:
                pass
        else:
            up_y += self.dy[0]*speed_sin+self.dy[1]*speed_cos
            up_x += self.dx[0]*speed_sin+self.dx[1]*speed_cos
        
        #if going too fast, it will control the speed
        speed_control = self.speed*self.run / math.sqrt(up_x**2 + up_y**2 + 0.000001)
        up_x *= speed_control
        up_y *= speed_control

        self.playerPosX += up_x
        self.playerPosY += up_y

        if self.playerPosZ > 0:
            self.playerPosZ -= 14

        if self.heightVisu < self.playerPosZ:
            self.heightVisu += 14
        elif self.heightVisu > self.playerPosZ:
            self.heightVisu -= 8

    def is_wall(self, matMap, x, y):
        if x>=0 and y>=0 and x<len(matMap[0]) and y<len(matMap) :
            return matMap[y][x] == 1
        return False

    def ray_casting(self, matMap):
        distances = []
        colors = []
        for theta in self.thetas:

            sign_x = round(abs(math.cos(theta))/(math.cos(theta)+0.001))
            sign_y = round(abs(math.sin(theta))/(math.sin(theta)+0.001))

            verif_x = (sign_x+1)/2-self.playerPosX%1
            verif_y = sign_y * abs(verif_x * math.tan(theta))
            distance_h = math.sqrt((verif_x)**2 + (verif_y)**2)
            is_wall_bool = self.is_wall(matMap, round(self.playerPosX + verif_x + (sign_x-1)/2), math.floor(self.playerPosY + verif_y))
            while not is_wall_bool and distance_h<self.vision_range:
                verif_x += sign_x
                verif_y += sign_y * abs(math.tan(theta))
                is_wall_bool = self.is_wall(matMap, round(self.playerPosX + verif_x + (sign_x-1)/2), math.floor(self.playerPosY + verif_y))
                distance_h = math.sqrt((verif_x)**2 + (verif_y)**2)
            
            verif_y = (sign_y+1)/2-self.playerPosY%1
            verif_x = sign_x * abs(verif_y / (math.tan(theta)+0.000001))
            distance_v = math.sqrt((verif_x)**2 + (verif_y)**2)
            is_wall_bool = self.is_wall(matMap, math.floor(self.playerPosX + verif_x), round(self.playerPosY + verif_y + (sign_y-1)/2))
            while not is_wall_bool and distance_v < self.vision_range and distance_v < distance_h :
                verif_y += sign_y
                verif_x += sign_x / abs(math.tan(theta)+0.000001)
                is_wall_bool = self.is_wall(matMap, math.floor(self.playerPosX + verif_x), round(self.playerPosY + verif_y + (sign_y-1)/2))
                distance_v = math.sqrt((verif_x)**2 + (verif_y)**2)

            distances.append(min(distance_h, distance_v)*abs(math.cos(self.theta-theta))) # abs(math.cos(self.theta-theta)) makes walls less rounded in 2.5D (will reduce distances in 2D)
            if distances[-1] >= self.vision_range*abs(math.cos(self.theta-theta)):
                distances[-1] = False

        return distances
    

    def get_height_visu(self):
        return self.heightVisu
    
    def get_fov(self):
        return self.fov