import json
import pygame
import time
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))

levelTileSet = "Beach"

def loadLevel(Receptacle, camera):
    for y in range(len(Datafile["Layouts"]["Main Room"])):
        for x in range(len(Datafile["Layouts"]["Main Room"][y])):
            tilecoordinates = Datafile["Terrain"]["SpriteCoordinates"][levelTileSet][Datafile["Tilekey"][str(Datafile["Layouts"]["Main Room"][y][x])]]
            Receptacle.blit(Sheet, ((x*8)-camera.xpos,(y*8)),(tilecoordinates[0],tilecoordinates[1],8,8))

def pallateApply(pallate, sprite):
    #for each color in sprite:
    for color in range(len(pallate)):
        colorSprite = pygame.Surface(sprite.get_size())
        #replace with corrosponding pallate color
        colorSprite.fill(pallate[color])
        sprite.set_colorkey(Datafile["Character"]["Pallates"][self.charName]["Normal"][color])
        colorSprite.blit(sprite, (0,0))
        sprite.blit(colorSprite, (0,0))
    return sprite

#class camera:
class Camera:
    def __init__(self, focus):
        self.xpos = 0
        self.ypos = 0
        self.__focus = focus
        self.__focusx = 0
        self.__focusy = 0
    def update(self):
        self.__focusx = self.__focus.location[0]
        self.xpos = self.__focusx-124
        