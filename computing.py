import math
from sys import exit
import pygame

#displayPart
def displayWalls(d, screen):
    numbOfSlices = len(d)
    walls = [pygame.Surface((math.ceil(screen.get_width()/numbOfSlices),2*800/d[i])) for i in range(numbOfSlices)]
    for wall in walls:
        wall.fill("#FF0000")
    return walls

#rayPart
def distanceR(playerPosX, playerPosY, matMap, thetas, numbOfRays):
    i=0
    distances = [0 for i in range(numbOfRays)]
    for theta in thetas:
        isWall = False
        while not isWall :
            distances[i] += 0.1
            watchX = playerPosY+distances[i]*math.cos(theta)
            watchY = playerPosX+distances[i]*math.sin(theta)
            watchX = math.floor(watchX)
            watchY = math.floor(watchY)
            if matMap[watchY][watchX] == 1:
                isWall = True
        i+=1
    return distances

matMap=[[1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]]

playerPosX = 1.1
playerPosY = 1.1
dx = [0,0]
dy = [0,0]
theta = 0   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top
dt = 0
initSpeed = 0.1
speed = initSpeed
circSpeed = 2

playerPosZ = 0
heightVisu = 0

fov = 60    #if next to a wall and fov of 90, not working
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

bg = pygame.Surface((width,height))
bg.fill("#000000")

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
                dt = circSpeed
            elif event.key == pygame.K_LEFT :
                dt = -circSpeed
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
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT :
                dt = 0
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
    
    theta += dt
    speedCos = speed*math.cos(theta2)
    speedSin = speed*math.sin(theta2)
    if matMap[math.floor(playerPosX + dx[0]*speedCos+dx[1]*speedSin)][math.floor(playerPosY + dy[0]*speedCos+dy[1]*speedSin)]!=1:
        playerPosX+= dx[0]*speedCos+dx[1]*speedSin
        playerPosY+= dy[0]*speedCos+dy[1]*speedSin
    if playerPosZ > 0:
        playerPosZ -= 14
    if heightVisu < playerPosZ:
        heightVisu += 14
    elif heightVisu > playerPosZ:
        heightVisu -= 8
    
    #print screen
    screen.blit(bg, (0,0))
    for i in range(len(walls)):
        x = i*screen.get_width()/len(walls)
        y = screen.get_height()//2 - walls[i].get_height() // 2 + heightVisu
        screen.blit(walls[i], (x,y))
    
    pygame.display.update()
    clock.tick(60)