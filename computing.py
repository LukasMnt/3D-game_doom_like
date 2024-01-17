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
def distanceR(playerPos, matMap, thetas, numbOfRays):
    i=0
    distances = [0 for i in range(numbOfRays)]
    for theta in thetas:
        isWall = False
        while not isWall :
            distances[i] += 0.1
            watchX = playerPos[1]+distances[i]*math.cos(theta)
            watchY = playerPos[0]+distances[i]*math.sin(theta)
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

playerPos = (1.1,1.1)
theta = 45   #where do you watch ? 0 = right, 90 = down, 180 = left, 270 = -90 = top

fov = 80    #if next to a wall and fov of 90, not working
fov = fov/2
numbOfRays = 101
cst = 2*fov/(numbOfRays-1)
thetas = [(theta-fov+cst*i)*math.pi/180 for i in range(numbOfRays)]

d = distanceR(playerPos, matMap, thetas, numbOfRays)

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

while True:
    #update
    for event in pygame.event.get():
        #if we press the red cross
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        screen.blit(bg, (0,0))
        for i in range(len(walls)):
            x = i*screen.get_width()/len(walls)
            y = screen.get_height()//2 - walls[i].get_height() // 2
            screen.blit(walls[i], (x,y))
        
        pygame.display.update()
        clock.tick(60)