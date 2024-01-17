import math

def distanceR(playerPos, matMap, thetas, numbOfRays):
    i=0
    distances = [0 for i in range(numbOfRays)]
    for theta in thetas:
        isWall = False
        while not isWall :
            distances[i] += 0.1
            watchX = playerPos[0]+distances[i]*math.cos(theta)
            watchY = playerPos[1]+distances[i]*math.sin(theta)
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

playerPos = (1,1)
fov = 80
numbOfRays = 10
cst = 2*fov/(numbOfRays-1)
theta = 45
thetas = [(theta-fov+cst*i)*math.pi/180 for i in range(numbOfRays)]

#premier mur a disatance de 8
d = distanceR(playerPos, matMap, thetas, numbOfRays)
