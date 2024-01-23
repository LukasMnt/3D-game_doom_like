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
    
    game_loop(clock)
    

def game_loop(clock):
    myMap = Maps()
    myPlayer = Player()
    printObj = PrintableObjects()
    fps = []
    meanFPS = 1
    mean_1_percent_low = 0
    t = [time.time(),0]
    
    while True:
        #compute
        allDists = myPlayer.ray_casting(myMap.get_map())
        printObj.compute_walls(allDists, myPlayer.get_fov())
        
        #looking for events
        for event in pygame.event.get():
            #if we press the red cross
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #gesture of arrows and keys (mouse in the future)
            myPlayer.update_on_event(event)
        
        #mov
        myPlayer.update_mov(myMap.get_map())
        
        #print screen
        printObj.draw(myPlayer.get_height_visu(), ["FPS : " + str(meanFPS), 100, 150, 50],["1% : " + str(mean_1_percent_low), 50,75, 125])
        #printObj.draw_2D(myPlayer,myMap.get_map(), allDists)
        
        #compute curent FPS and 1% Low for 600 frames (10 second in an normal case)
        if printObj.are_FPS():
            t[1]=time.time()
            fps.append(1/(t[1]-t[0]))
            store = 600
            if len(fps) > store:
                fps.pop(0)
            meanFPS = math.floor(sum(fps)/len(fps))
            percent_low_list = heapq.nsmallest(math.floor(store/100), fps)
            mean_1_percent_low = math.floor(sum(percent_low_list)/len(percent_low_list))
            t[0] = t[1]
        
        #pygame FPS limite
        clock.tick(60)
main()

"""
What to improve ?
    Textures
    Look up and down
    Add mouse controll
"""