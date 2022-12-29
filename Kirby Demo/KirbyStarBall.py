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
import camLib
import StarballLib
import HostLib
import time
import threading
from functools import partial
#create window

def getData(theBall, items, connectionHost):
    while True:
        global datalist
        datalist = []
        for item in items:
            try:
                if item == theBall:
                    #print("sending data")
                    HostLib.sendToClient(item.sendList,connectionHost)
                #print("Testing next obj")
                if item.multiplayerMode != "HOST":
                    ##print("object is network-based")
                    data = HostLib.loop(item.multiplayerMode)
                    datalist.append(data)
                    ##print("got data")
                else:
                    if item == theBall:
                        #print("waiting for data")
                        data = HostLib.loop(connectionHost)
                        datalist.append(data)
                    else:
                        HostLib.sendToClient(item.sendList,connectionHost)
                    ##print("object is host:")
                    #print("sent data")
            except Exception as e:
                #itr += 1
                print(e)
                #print("communication breakdown:", item.charName, item.pallateName)
                pass

hostvar = int(input("1.Host\n2.Clint"))
pygame.init()
screenscale = 1
winsizex = 256
winsizey = 240
xval = 0
yval = 0
P1Score = 0
P2Score = 0
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
connectionHost = HostLib.connect(hostvar)

MainRoom = levelLib.Level("Castle", "StarballRing",Objects,charLayer)
if hostvar == 1:
    Player = gameLib.Player(0,"Kirby","Copy",56,100,Objects,charLayer, "Normal",MainRoom,"HOST")
    Player2 = gameLib.Player(1,"Kirby","Copy",256,100,Objects,charLayer, "Dee",MainRoom,connectionHost)
    theBall = gameLib.Ball(2,"StarBall", "Copy", 124, 182, Objects, charLayer, "Shoot1",MainRoom,"HOST")
    mainCam = camLib.Camera(MainRoom,Player)
else:
    Player = gameLib.Player(0,"Kirby","Copy",56,100,Objects,charLayer, "Normal",MainRoom,connectionHost)
    Player2 = gameLib.Player(1,"Kirby","Copy",256,100,Objects,charLayer, "Dee",MainRoom,"HOST")
    theBall = gameLib.Ball(2,"StarBall", "Copy", 124, 182, Objects, charLayer, "Shoot1",MainRoom,connectionHost)
    mainCam = camLib.Camera(MainRoom,Player2)

#Test = gameLib.Attack("Kirby","None",150,100,Objects,charLayer,"Dee",MainRoom,500,Player,"circle")
#loop
inputs = pygame.key.get_pressed()
itr = 0
global datalist
datalist = []
inputThread = threading.Thread(target = partial(getData, theBall, Objects, connectionHost))
inputThread.daemon = True
connectionHost.settimeout(0.01)
inputThread.start()

while True:
    print(datalist)
    MainRoom.loadLevel(TileLayer, mainCam)
    #time.sleep(0.05)
    fpstimer.tick(60)
    #update gameobjects
    #send data over network
    keys = pygame.key.get_pressed()
    for item in Objects:
        #print(f"{item.charName}{item.pallateName} update cycle")
        item.update(mainCam)
        
    for data in datalist:
        for object in Objects:
            if object.ID == data[7]:
                #print("match found: ", object.ID)
                if object == theBall:
                    object.ballchecks(data,connectionHost)
                    if item.multiplayerMode != "HOST":
                        object.checks(data)
                else:
                    object.checks(data)
    mainCam.update()
    #print(theBall.blockedLeft)
    P1Score,P2Score = StarballLib.StarballUpdate(theBall,P1Score,P2Score)
    #draw the frame
    displayPane.blit(TileLayer, (0,0))
    displayPane.blit(charLayer, (0,0))
    charLayer.fill((0,0,0))
    TileLayer.fill((0,0,0))
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
