import math
from sys import exit
import pygame

# external files
from player import *
from maps import *
from printableObjects import *

# for fps mainly (only this for the moment but I may forget to update the message):
import time
import heapq

# launch the game and initialize pygame (may I should have merge main and game_loop)
def main():
    #initialise
    pygame.init()
    pygame.display.set_caption("Doom_like")
    clock = pygame.time.Clock()
    game_loop(clock)
    
# apparition of the first objects and variables for the FPS and 1 percent low + the loop of the game
def game_loop(clock):
    myMap = Maps()
    myPlayer = Player()
    printObj = PrintableObjects()
    fps = []                # init for FPS
    meanFPS = 1             # init for FPS
    mean_1_percent_low = 0  # init for FPS
    t = [time.time(),0]     # time before first loop and init of second time
    
    # I know while True is not the best but exit() works pretty well
    while True:
        #compute walls
        allDists = myPlayer.ray_casting(myMap.get_map())
        printObj.compute_walls(allDists, myPlayer.get_fov())
        
        # looking for events
        for event in pygame.event.get():
            # if we press the red cross
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # gesture of arrows and keys (mouse in the future)
            myPlayer.update_on_event(event)
        
        # mov of the player
        myPlayer.update_mov(myMap.get_map())
        
        # print screen 2.5D (draw) or 2D (draw_2D)
        printObj.draw(myPlayer.get_height_visu(), ["FPS : " + str(meanFPS), 100, 150, 50],["1% : " + str(mean_1_percent_low), 50,75, 125])
        # printObj.draw_2D(myPlayer,myMap.get_map(), allDists)
        
        # compute curent FPS and 1% Low for 600 frames (10 second in an normal case)
        if printObj.are_FPS():
            t[1]=time.time()            # time after a loop
            fps.append(1/(t[1]-t[0]))   # avrage FPS on this loop
            store = 600                 # how many FPS to store
            if len(fps) > store:
                fps.pop(0)              # remove fist element of the list if too many FPS in the store
            meanFPS = math.floor(sum(fps)/len(fps))         # basic FPS mean
            percent_low_list = heapq.nsmallest(math.floor(store/100), fps)                  # take 1 lowest percent of last FPS
            mean_1_percent_low = math.floor(sum(percent_low_list)/len(percent_low_list))    # basic 1 percent low mean
            t[0] = t[1]                 # our time after a loop is now the old time (before the new loop)
        
        # pygame FPS limite
        clock.tick(60)
main()

"""
What to improve ?
    Textures
    Look up and down
    Add mouse controll
"""