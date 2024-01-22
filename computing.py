import math
from sys import exit
import pygame

#external files
from player import *
from maps import *
from printableObjects import *

#for fps mainly (only this for the moment but I may forget to update the message):
import time
import heapq

def main():
    #initialise
    pygame.init()
    pygame.display.set_caption("Doom_like")
    clock = pygame.time.Clock()
    
    gameLoop(clock)
    

def gameLoop(clock):
    myMap = Maps()
    myPlayer = Player()
    printObj = PrintableObjects()
    fps = []
    meanFPS = 1
    mean1PL = 0
    t = [time.time(),0]
    
    while True:

        #update
        allDists = myPlayer.rayCasting(myMap.getMap())
        printObj.computeWalls(allDists, myPlayer.getFov())
        #compute
        for event in pygame.event.get():
            #if we press the red cross
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #gesture of arrows and keys (mouse in the future)
            myPlayer.updateOnEvent(event)
        #mov
        myPlayer.updateMov(myMap.getMap())
        
        #print screen
        printObj.draw(myPlayer.getHeightVisu(), ["FPS : " + str(meanFPS), 100, 150, 50],["1% : " + str(mean1PL), 50,75, 125])
        #printObj.draw2D(myPlayer,myMap.getMap(), allDists)
        
        if printObj.areFPS():
            t[1]=time.time()
            fps.append(1/(t[1]-t[0]))
            store = 600
            if len(fps) > store:
                fps.pop(0)
            meanFPS = math.floor(sum(fps)/len(fps))
            PL = heapq.nsmallest(math.floor(store/100), fps)
            mean1PL = math.floor(sum(PL)/len(PL))
            t[0] = t[1]
            
        clock.tick(60)
main()

"""
What to improve ?
    Moving in diagonal gives more speed
    Looks a bit too rounded (infinit norme while computing allDists ?) (multiply by cos of the angle of the ray)
    Textures
    Look up and down
    Add mouse controll
"""