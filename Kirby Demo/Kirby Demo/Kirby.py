"""
Filename:Kirby.py
Author: Taliesin Reese
Date: 8/25/2022
Version: 1.0
Purpose: serve some function in a fun way
"""
#imports
import pygame
import gameLib
import levelLib
import time
#create window
pygame.init()
screenscale = 2
winsizex = 256
winsizey = 240
xval = 0
yval = 0
window = pygame.display.set_mode((winsizex*screenscale,winsizey*screenscale))
fpstimer = pygame.time.Clock()

#title screen:
    #play music
    #load everything
    #animate main screen coming down
    #add text at bottom
    #when input is recieved:
        #transition effect
        #deload title screen text
        #move title screen back up
        #main room

#main room
    #move kirby to main room
    #if exit to left:
        #title screen
    #if enter area door:
        #area
    #if enter circumference door:
        #circumference
    #if enter basement:
        #basement

#area
    #move kirby to area room

#circumference
    #move kirby to circum room

#basement
    #move kirby to basement

#array of game objects
Objects = []
#layer for sprites
#layer for BG tiles
TileLayer = pygame.Surface((winsizex, winsizey))
charLayer = pygame.Surface((winsizex, winsizey))
charLayer.set_colorkey((0,0,0))
displayPane = pygame.Surface((winsizex,winsizey))

Player = gameLib.Character("Kirby","player",56,100,Objects,charLayer, "Normal")
NPCCircumference = gameLib.Character("Kirby","npc",24,100,Objects,charLayer, "Ice")
mainCam = levelLib.Camera(Player)
#loop
while True:
    levelLib.loadLevel(TileLayer, mainCam)
    fpstimer.tick(60)
    #update gameobjects
    for item in Objects:
        item.update(mainCam)
    mainCam.update()
    #draw the frame
    displayPane.blit(TileLayer, (0,0))
    displayPane.blit(charLayer, (0,0))
    charLayer.fill((0,0,0))
    window.blit(pygame.transform.scale(displayPane, (winsizex*screenscale,winsizey*screenscale)), (0,0))
    #put the stuff from the frame onto the window
    pygame.display.flip()
    #code for quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        """if event.type == pygame.key.get_pressed()[]:
            if event.key == pygame.K_LEFT and Player.blockedLeft == False:
                Player.speed[0] = -1
            if event.key == pygame.K_RIGHT and Player.blockedRight == False:
                Player.speed[0] = 1
            if event.key == pygame.K_SPACE and Player.blockedRight == False:
                Player.speed[1] = -10"""
