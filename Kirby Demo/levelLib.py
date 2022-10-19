import json
import pygame
import time
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))

class Level:
    def __init__(self, theme, name):
        self.__theme = theme
        self.__name = name
        self.__graphicsData = Datafile["Terrain"]["SpriteCoordinates"][theme]
        self.__collisionData = Datafile["Layouts"][self.__name]
        self.maxiY = len(Datafile["Layouts"][self.__name])
        self.maxiX = self.getMaxiX()

    def loadLevel(self, Receptacle, camera):
        for y in range(len(self.__collisionData)):
            for x in range(len(Datafile["Layouts"][self.__name][y])):
                graphics = self.__graphicsData.get(Datafile["Tilekey"][str(self.__collisionData[y][x])])
                Receptacle.blit(Sheet, ((x*8)-camera.xpos,(y*8)),(graphics[0],graphics[1],8,8))

    def pallateApply(self, pallate, sprite):
        #for each color in sprite:
        for color in range(len(pallate)):
            colorSprite = pygame.Surface(sprite.get_size())
            #replace with corrosponding pallate color
            colorSprite.fill(pallate[color])
            sprite.set_colorkey(Datafile["Character"]["Pallates"][self.charself.__name]["Normal"][color])
            colorSprite.blit(sprite, (0,0))
            sprite.blit(colorSprite, (0,0))
        return sprite

    def getMaxiX(self):
        longest = 0
        for y in range(len(self.__collisionData)):
            if len(self.__collisionData[y]) > len(self.__collisionData[longest]):
                longest = y
        return len(self.__collisionData[longest])
