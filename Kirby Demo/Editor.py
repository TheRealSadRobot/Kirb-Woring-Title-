#imports
import levelLib
import camLib
import json
import pygame
import time

#setup
pygame.init()
screenscale = 3
winsizex = 256
winsizey = 240
levelObjects = []
itr = 0
tiletype = 1
window = pygame.display.set_mode((winsizex*screenscale,winsizey*screenscale))
charLayer = pygame.Surface((winsizex, winsizey))
tileLayer = pygame.Surface((winsizex, winsizey))
displayPane = pygame.Surface((winsizex,winsizey))
Datafile = json.load(open("Support.json"))

#level Layout should be like this:
    #inside .json file for level:
        #Layot of level, in the form of a list of lists of numbers, which correspond to the tilekey in the main Datafile
        #Layout of Objects in the level, in the form of a list of lists of item properties
        #Theme Map, in the same form as layout, with numbers corresponding to tilesets.
        #FlipMap, in the same form as layout, with entries determining the nature of flipping
        #locations of Music and BGs
#def main
def main():
    level = levelLib.Level("Beach", "TestRoom1",levelObjects,charLayer)
    mainCam = camLib.Camera(level,None)
    #while True
    while True:
        #put the stuff from the frame onto the window
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mainCam.movePos(-2,0)
        if keys[pygame.K_RIGHT]:
            mainCam.movePos(2,0)
        #if mode is place blocks:
            #placeblocks
        #else if mode is place objects
            #placeobject
        #code for quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #display Level
        level.loadLevel(tileLayer, mainCam)
        mainCam.update()
        #draw the frame
        displayPane.blit(tileLayer, (0,0))
        placeBlocks(level, mainCam)
        window.blit(pygame.transform.scale(displayPane, (winsizex*screenscale,winsizey*screenscale)), (0,0))
        tileLayer.fill((0,0,0))
        
#def placeblocks
def placeBlocks(level, camera):
    rawLocale = pygame.mouse.get_pos()
    cursorSpot = [int(rawLocale[0]/screenscale),int(rawLocale[1]/screenscale)]
    collisionCheck(cursorSpot,level,camera)
    #if square of level is clicked:
    print(int((cursorSpot[0]-cursorSpot[0]%8+(camera.xpos-camera.xpos%8)/8)))
    #print((cursorSpot[1]-cursorSpot[1]%8)/8)
    if pygame.mouse.get_pressed(3) == (1,0,0):
        #place a block there
        row =level.collisionData[int((cursorSpot[1]-cursorSpot[1]%8)/8)]
        row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = tiletype
    elif pygame.mouse.get_pressed(3) == (0,0,1):
        #place a block there
        row =level.collisionData[int((cursorSpot[1]-cursorSpot[1]%8)/8)]
        row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = 0
        #if add row button is pressed:
            #add a row
        #if add column button is pressed:
            #add a column
        #switch block stuff
        #flip block stuff
        #switch tileset stuff
#def placeobject
        #if pixel of level is clicked:
            #place an object there
        #switch object stuff
        #edit object properties stuff
    elif pygame.mouse.get_pressed(3) == (0,1,0):
        writeTo = open((f"LevelData\{level.getName()}.json"),'r+')
        writeThis = {"Layout":level.collisionData,"Tileset":level.tileset,"FlipMap":level.flipmap,"Objects":level.file["Objects"],"BG":level.file["BG"],"Music":level.file["Music"]}
        json.dump(writeThis,writeTo)
        print("Your Game--Saved!")

#collision Detection
def collisionCheck(point,level, camera):
    global itr
    #check all four points on character.
    #find what tile type they are on
    tilecountx = ((point[0]+camera.xpos)//8)
    tilecounty = (point[1]//8)
    tilenum = str(level.collisionData[tilecounty][tilecountx])
    tiletype = (Datafile["Tilekey"][tilenum])
    #print(tiletype)
    if itr < 30:
        pygame.draw.rect(displayPane,(0,0,255,0),(point[0]-point[0]%8-camera.xpos%8,point[1]-point[1]%8,8,8),1)
        itr += 1
    elif itr > 0:
        pygame.draw.rect(displayPane,(200,200,255,0),(point[0]-point[0]%8-camera.xpos%8,point[1]-point[1]%8,8,8),1)
        itr -= 1
    """if tiletype != "Air":
            if level.file["FlipMap"][tilecounty][tilecountx] != 0:
                    print("flipped")
                    time.wait(1)"""
    return tiletype
main()
