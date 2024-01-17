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
theta = 0   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top
speed = 0.1

fov = 80    #if next to a wall and fov of 90, not working
fov = fov/2
numbOfRays = 101
cst = 2*fov/(numbOfRays-1)
thetas = [(theta-fov+cst*i)*math.pi/180 for i in range(numbOfRays)]
theta2 = theta*math.pi/180

d = distanceR(playerPosX,playerPosY, matMap, thetas, numbOfRays)

#displayPart
pygame.init()
width=1500
height=800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Doom_like")
clock = pygame.time.Clock()

bg = pygame.Surface((width,height))
bg.fill("#000000")

walls = displayWalls(d, screen)

keys=[False,False,False,False]
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
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if keys[3]:
            if matMap[math.floor(playerPosX + speed*math.cos(theta2))][math.floor(playerPosY - speed*math.sin(theta2))]!=1:
                playerPosX+= speed*math.cos(theta2)
                playerPosY-= speed*math.sin(theta2)
        if keys[1]:
            if matMap[math.floor(playerPosX - speed*math.cos(theta2))][math.floor(playerPosY + speed*math.sin(theta2))]!=1:
                playerPosX-= speed*math.cos(theta2)
                playerPosY+= speed*math.sin(theta2)
        if keys[0]:
            if matMap[math.floor(playerPosX + speed*math.sin(theta2))][math.floor(playerPosY + speed*math.cos(theta2))]!=1:
                playerPosX+= speed*math.sin(theta2)
                playerPosY+= speed*math.cos(theta2)
        if keys[2]:
            if matMap[math.floor(playerPosX - speed*math.sin(theta2))][math.floor(playerPosY - speed*math.cos(theta2))]!=1:
                playerPosX-= speed*math.sin(theta2)
                playerPosY-= speed*math.cos(theta2)
    print(playerPosX,playerPosY)
    #print screen
    screen.blit(bg, (0,0))
    for i in range(len(walls)):
        x = i*screen.get_width()/len(walls)
        y = screen.get_height()//2 - walls[i].get_height() // 2
        screen.blit(walls[i], (x,y))
    
    pygame.display.update()
    clock.tick(60)