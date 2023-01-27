import json
import gameLib
import pygame
import time
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))

class Level:
    def __init__(self, theme, name, renderLayer, objList):
        self.__name = name
        self.file =  json.load(open(f"LevelData\{self.__name}.json"))
        self.__graphicsData = Datafile["Terrain"]["SpriteCoordinates"]
        self.collisionData = self.file.get("Layout")
        self.flipmap = self.file.get("FlipMap")
        self.tileset = self.file.get("Tileset")
        self.maxiY = len(self.collisionData)
        self.maxiX = self.getMaxiX()
        for Object in self.file.get("Objects"):
            objectData =self.file['Objects'][Object]
            className = getattr(gameLib,f"{self.file['Objects'][Object][0]}")
            objectInLevel = className(objectData[1],objectData[2],objectData[3],objectData[4],objectData[5],renderLayer,objList,objectData[8],self)

    def loadLevel(self, Receptacle, camera):
        for y in range(len(self.collisionData)):
            for x in range(len(self.collisionData[y])):
                graphics = self.__graphicsData[Datafile["Themekey"][str(self.file["Tileset"][y][x])]].get(Datafile["Tilekey"][str(self.collisionData[y][x])])
                tile = pygame.Surface((8,8))
                tile.blit(Sheet, (0,0), (graphics[0],graphics[1],8,8))
                if self.file["FlipMap"][y][x] == 1:
                    Receptacle.blit(pygame.transform.flip(tile,1,0), ((x*8)-camera.xpos,(y*8)-camera.ypos))
                elif self.file["FlipMap"][y][x] == 2:
                    Receptacle.blit(pygame.transform.flip(tile,0,1), ((x*8)-camera.xpos,(y*8)-camera.ypos))
                elif self.file["FlipMap"][y][x] == 3:
                    Receptacle.blit(pygame.transform.flip(tile,1,1), ((x*8)-camera.xpos,(y*8)-camera.ypos))
                else:
                    Receptacle.blit(Sheet, ((x*8)-camera.xpos,(y*8)-camera.ypos),(graphics[0],graphics[1],8,8))

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
    def getName(self):
        return self.__name
    def getMaxiX(self):
        longest = 0
        for y in range(len(self.collisionData)):
            if len(self.collisionData[y]) > len(self.collisionData[longest]):
                longest = y
        return len(self.collisionData[longest])
