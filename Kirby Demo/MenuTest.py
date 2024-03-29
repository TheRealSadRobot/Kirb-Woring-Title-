#imports
import pygame
import gameLib
import levelLib
import camLib
import time

#start
#create window
pygame.init()
screenscale = 3
winsizex = 256
winsizey = 240
xval = 0
yval = 0
invis = (0,255,62)
window = pygame.display.set_mode((winsizex*screenscale,winsizey*screenscale))
fpstimer = pygame.time.Clock()

#array of game objects
Objects = []
#layer for sprites
#layer for BG tiles
base = pygame.Surface((winsizex, winsizey))
base.fill((0,0,0))
backLayer = pygame.Surface((winsizex, winsizey))
TileLayer = pygame.Surface((winsizex, winsizey))
charLayer = pygame.Surface((winsizex, winsizey))
charLayer.set_colorkey(invis)
backLayer.set_colorkey(invis)
TileLayer.set_colorkey(invis)
displayPane = pygame.Surface((winsizex,winsizey))

#display menu
print("1. Test Room 2. Starball Test")

#get selection
num = int(input(">>"))

#load level and other resources
if num == 1:
    currentLevel = levelLib.Level("Castle", "TestRoom1",Objects,charLayer)
elif num == 2:
    currentLevel = levelLib.Level("Castle", "StarballRing",Objects,charLayer)

Water = gameLib.fluid(1,"Water",100,50,Objects,backLayer,"Water",currentLevel,[80,400])
Door = gameLib.door(2,"Door",56,168,Objects,charLayer,"White",currentLevel,["Normal",[256,64],[16,32],"load"])
Platform = gameLib.platform(3,"Platform",200,100,Objects,charLayer,"Stormy",currentLevel,[0,True,[["line",[0.5,-1.5],50],["line",[-0.5,1.5],50]],0,"Cloud",[48,72]])
TriggerTest = gameLib.enterTrigger(1,"Null",256,0,Objects,backLayer,"Null",currentLevel,["Player",["beam",[32,0,32,30,"tileset","6",256,240]],["abilitychange","lvlAlterRange"]])
Player = gameLib.Player(0,"Kirby",56,100,Objects,charLayer,"Normal",currentLevel,["beam","HOST"])
#Test = gameLib.Attack("Kirby","None",150,100,Objects,charLayer,"Dee",currentLevel,500,Player,"circle")
mainCam = camLib.Camera(currentLevel,Player)

#run
#loop
while True:
    currentLevel.loadLevel(TileLayer, mainCam)
    #print(currentLevel.name)
    #time.sleep(0.2)
    fpstimer.tick(60)
    #update gameobjects
    for item in Objects:
        if currentLevel.pauseobj == None:
            #print(item.charName)
            item.update(mainCam)
        elif isinstance(item,gameLib.Player):
            item.pausePlayerScript()
    mainCam.update()
    #draw the frame
    displayPane.blit(base,(0,0))
    displayPane.blit(backLayer, (0,0))
    displayPane.blit(TileLayer, (0,0))
    displayPane.blit(charLayer, (0,0))
    charLayer.fill(invis)
    TileLayer.fill(invis)
    backLayer.fill(invis)
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
