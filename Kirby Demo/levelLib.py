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
        #TEMP
        self.animlist = [[3,0,"BetaCurtainMove"]]
        #END TEMP
        #new list in level "L1" that with structure:
            #((x,y,((Thing to change,new setting,time to hold),etc.)),etc.)
        #new list here "L2" of L1's length. Used for timing
        #new list here "L3" of L1's length. Usedd to keep track of frames
        self.animList = self.file.get("animList")
        self.animTimer = []
        self.animFrames = []
        for num in range(len(self.animList)):
            self.animTimer.append(0)
            self.animFrames.append(0)
        for Object in self.file.get("Objects"):
            objectData =self.file['Objects'][Object]
            className = getattr(gameLib,f"{self.file['Objects'][Object][0]}")
            objectInLevel = className(objectData[1],objectData[2],objectData[3],objectData[4],objectData[5],renderLayer,objList,objectData[8],self)

    def loadLevel(self, Receptacle, camera):
        #for each entry in L2
        for item in range(len(self.animList)):
            #move up 1
            self.animTimer[item] += 1
            #if it exceeds or equals the frame duration count,
            if self.animTimer[item] >= Datafile["TileAnimations"][self.animList[item][2]][self.animFrames[item]][2]:
            #turn it to zero
                self.animTimer[item] = 0
            #move to next frame
                self.animFrames[item] += 1
            #if beyond final frame:
            if self.animFrames[item] >= len(Datafile["TileAnimations"][self.animList[item][2]][self.animFrames[item]]):
                #move back to first frame
                self.animFrames[item] = 0
            if Datafile["TileAnimations"][self.animList[item][2]][self.animFrames[item]][0] == "Layout":
                toEdit = self.collisionData
            elif Datafile["TileAnimations"][self.animList[item][2]][self.animFrames[item]][0] == "FlipMap":
                toEdit = self.flipmap
            elif Datafile["TileAnimations"][self.animList[item][2]][self.animFrames[item]][0] == "Tileset":
                toEdit = self.tileset
            toEdit[self.animList[item][1]][self.animList[item][0]] = Datafile["TileAnimations"][self.animList[item][2]][self.animFrames[item]][1]
            #print()
        for y in range(len(self.collisionData)):
            for x in range(len(self.collisionData[y])):
                #NOTE: graphicsData[Datafile["Themekey"][str(self.file["Tileset"][y][x])]] will access the theme
                graphics = self.__graphicsData.get(Datafile["Tilekey"][str(self.collisionData[y][x])])
                tile = pygame.Surface((8,8))
                tile.blit(Sheet, (0,0), (graphics[0],graphics[1],8,8))
                pallatename = Datafile["Pallatekey"][str(self.tileset[y][x])]
                pallate = Datafile["Pallates"][pallatename]
                tile = self.pallateApply(pallate,tile)
                if self.file["FlipMap"][y][x] == 1:
                    Receptacle.blit(pygame.transform.flip(tile,1,0), ((x*8)-camera.xpos,(y*8)-camera.ypos))
                elif self.file["FlipMap"][y][x] == 2:
                    Receptacle.blit(pygame.transform.flip(tile,0,1), ((x*8)-camera.xpos,(y*8)-camera.ypos))
                elif self.file["FlipMap"][y][x] == 3:
                    Receptacle.blit(pygame.transform.flip(tile,1,1), ((x*8)-camera.xpos,(y*8)-camera.ypos))
                else:
                    Receptacle.blit(tile, ((x*8)-camera.xpos,(y*8)-camera.ypos))

    def pallateApply(self, pallate, sprite):
        #for each color in sprite:
        colorSprite = pygame.Surface(sprite.get_size())
        for color in range(len(pallate)):
            #replace with corrosponding pallate color
            #print(pallate)
            colorSprite.fill(pallate[color])
            sprite.set_colorkey(Datafile["Pallates"]["Default"][color])
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
