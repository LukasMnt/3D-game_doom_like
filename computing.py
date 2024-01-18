import math
from sys import exit
import pygame

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

matMap=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
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

playerPosX = 2
playerPosY = 2
dx = [0,0]
dy = [0,0]
theta = 45   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top
dt = 0
initSpeed = 0.03
speed = initSpeed
run = 1
circSpeed = 3

playerPosZ = 0
heightVisu = 0

fov = 60
fov = fov/2
numbOfRays = 101
cst = 2*fov/(numbOfRays-1)
thetas = [(theta-fov+cst*i)*math.pi/180 for i in range(numbOfRays)]
theta2 = theta*math.pi/180

d = distanceR(playerPosX,playerPosY, matMap, thetas, numbOfRays)

#displayPart
pygame.init()
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
    d = distanceR(playerPosX,playerPosY, matMap, thetas, numbOfRays)
    thetas = [(theta-fov+cst*i)*math.pi/180 for i in range(numbOfRays)]
    theta2 = theta*math.pi/180
    walls = displayWalls(d, screen)
    
    for event in pygame.event.get():
        #if we press the red cross
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                dx = [dx[0],dx[1]+1]
                dy = [dy[0]+1,dy[1]]
            if event.key == pygame.K_s:
                dx = [dx[0],dx[1]-1]
                dy = [dy[0]-1,dy[1]]
            if event.key == pygame.K_a:
                dx = [dx[0]-1,dx[1]]
                dy = [dy[0],dy[1]+1]
            if event.key == pygame.K_d:
                dx = [dx[0]+1,dx[1]]
                dy = [dy[0],dy[1]-1]
            if event.key == pygame.K_RIGHT :
                dt += circSpeed
            if event.key == pygame.K_LEFT :
                dt -= circSpeed
            if event.key == pygame.K_LCTRL :
                if playerPosZ == 0:
                    playerPosZ = -96
                    speed /= 4
                elif playerPosZ < 0:
                    playerPosZ = 0
                    speed = initSpeed
            elif event.key == pygame.K_SPACE :
                if playerPosZ == 0 and heightVisu == 0:
                    playerPosZ = 420
            if event.key == pygame.K_LSHIFT :
                run *= 2
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT :
                dt -= circSpeed
            if event.key == pygame.K_LEFT :
                dt += circSpeed
            if event.key == pygame.K_w:
                dx = [dx[0],dx[1]-1]
                dy = [dy[0]-1,dy[1]]
            if event.key == pygame.K_s:
                dx = [dx[0],dx[1]+1]
                dy = [dy[0]+1,dy[1]]
            if event.key == pygame.K_a:
                dx = [dx[0]+1,dx[1]]
                dy = [dy[0],dy[1]-1]
            if event.key == pygame.K_d:
                dx = [dx[0]-1,dx[1]]
                dy = [dy[0],dy[1]+1]
            if event.key == pygame.K_LSHIFT :
                run /= 2
    
    theta += dt
    speedCos = run*speed*math.cos(theta2)
    speedSin = run*speed*math.sin(theta2)
    if matMap[math.floor(playerPosX + dx[0]*speedCos+dx[1]*speedSin)][math.floor(playerPosY)]!=1 :
        playerPosX+= dx[0]*speedCos+dx[1]*speedSin
    if matMap[math.floor(playerPosX)][math.floor(playerPosY + dy[0]*speedCos+dy[1]*speedSin)]!=1 :
        playerPosY+= dy[0]*speedCos+dy[1]*speedSin
    if playerPosZ > 0:
        playerPosZ -= 14
    if heightVisu < playerPosZ:
        heightVisu += 14
    elif heightVisu > playerPosZ:
        heightVisu -= 8
    
    #print screen
    screen.blit(bgTop, (0,-screen.get_height()//2+ heightVisu))
    screen.blit(bgBot, (0,screen.get_height()//2+ heightVisu))
    for i in range(len(walls)):
        x = i*screen.get_width()/len(walls)
        y = screen.get_height()//2 - walls[i].get_height() // 2 + heightVisu
        screen.blit(walls[i], (x,y))
    
    screen.blit(crosshairV, ((screen.get_width()-crosshairV.get_width())//2,(screen.get_height()-crosshairV.get_height())//2))
    screen.blit(crosshairH, ((screen.get_width()-crosshairH.get_width())//2,(screen.get_height()-crosshairH.get_height())//2))
    
    pygame.display.update()
    clock.tick(60)