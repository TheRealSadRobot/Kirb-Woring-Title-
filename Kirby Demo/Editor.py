#imports
import levelLib
import camLib
import pygame
#setup
#level Layout should be like this:
    #inside .json file for level:
        #Layot of level, in the form of a list of lists of numbers, which correspond to the tilekey in the main Datafile
        #Layout of Objects in the level, in the form of a list of lists of item properties
        #Theme Map, in the same form as layout, with numbers corresponding to tilesets.
        #FlipMap, in the same form as layout, with entries determining the nature of flipping
        #locations of Music and BGs
#def main
def main():
    pygame.init()
    screenscale = 3
    winsizex = 256
    winsizey = 240
    levelObjects = []
    charLayer = pygame.Surface((winsizex, winsizey))
    tileLayer = pygame.Surface((winsizex, winsizey))
    window = pygame.display.set_mode((winsizex*screenscale,winsizey*screenscale))
    displayPane = pygame.Surface((winsizex,winsizey))
    level = levelLib.Level("Beach", "TestRoom1",levelObjects,charLayer)
    mainCam = camLib.Camera(level)
    #while True
    while True:
        #display Level
        level.loadLevel(tileLayer, mainCam)
        mainCam.update()
        #draw the frame
        displayPane.blit(tileLayer, (0,0))
        window.blit(pygame.transform.scale(displayPane, (winsizex*screenscale,winsizey*screenscale)), (0,0))
        tileLayer.fill((0,0,0))
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
#def placeblocks
        #if square of level is clicked:
            #place a block there
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
main()
