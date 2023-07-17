import json
import pygame
import time
import math
import abilityLib
import levelLib
import HostLib
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))
#Object: core for all entities
    #Characters
        #NPCs
        #Players
        #Enemies
    #Fluids
    #Triggers
    #Doors

class Object:
    def __init__(self, ID, charName, xlocation, ylocation, arrayDestination,renderLayer,pallate,Level):
        self.ID = ID
        self.charName = charName
        #behavior type
        self.itr = 0
        self.currentLevel = Level
        self.dir = "right"
        self.sizex = 16
        self.sizey = 16
        self.speed = [0,0]
        #current sprite
        try:
            self.animFrame = Datafile["Character"]["Animations"][self.charName][list(Datafile["Character"]["Animations"][self.charName].keys())[0]][0][0]
            self.animation = list(Datafile["Character"]["Animations"][self.charName].keys())[0]
            self.animFrameNumber = 0
            self.animType = "Loop"
            self.animBacklog = "Fall"
            self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
            self.animItr = 0
            self.sprite = pygame.Surface((self.spriteSize[0],self.spriteSize[1]))
        except Exception as e:
            if isinstance(self,platform):
                raise(e)
        try:
            self.pallate = Datafile["Character"]["Pallates"][self.charName][pallate]
        except:
            pass
        self.collide = []
        self.renderLayer = renderLayer
        #add to array of all objects
        self.objlist = arrayDestination
        self.objlist.append(self)
        self.location = [xlocation,ylocation]
        self.getpoints()
    #removes object from list so that garbage collector will take it out
    def delete(self):
        self.objlist.remove(self)

    #test if two objects are colliding
    def collideWithObj(self):
        self.collide = []
        for obj in self.objlist:
            if obj != self:
                try:
                    #   if obj != self.inmouth:
                    #if top or bottom is between target body
                    if (self.bottom[1] >= obj.bottom[1] and self.top[1] <= obj.bottom[1]) or (self.bottom[1] >= obj.top[1] and self.top[1] <= obj.top[1]) or (self.bottom[1] <= obj.bottom[1] and self.top[1] >= obj.top[1]):
                        #if isinstance(self,Player):
                            #print(f"{obj.charName} {obj.pallateName}: Y-intersect")
                        #if left or right is between target body
                        if (self.left[0] <= obj.right[0] and self.right[0] >= obj.left[0]) or (self.left[0] <= obj.right[0] and self.right[0] >= obj.left[0]) or (self.right[0] <= obj.right[0] and self.left[0] >= obj.left[0]):
                            #if isinstance(self,Player):
                                #print(f"{obj.charName} {obj.pallateName}: X-intersect")
                            ##print("COLLISION")
                            #return true
                            self.collide.append(obj)
                    elif self.location[1] < obj.bottom[1] and self.location[1] > obj.top[1]:
                        if self.location[0] < obj.right[0] and self.location[0] > obj.left[0]:
                            self.collide.append(obj)
                except:
                    pass

    #test incoming network signals to ensure that all gamestates have the same movements
    def checks(self,data):
        #print(f"{self.charName}{self.pallateName} repairlog")
        if data[0] != self.crouching:
            self.crouching = data[0]
            #print("Key Stroke Repair")
        #print("crouch test passed")
        if data[1] != None:
            if self.mouthed != None:
                if data[1] != self.objlist.index(self.mouthed):
                    self.mouthed = self.objlist[data[1]]
                    #print("Consumed State Repair")
            elif self.mouthed != data[1]:
                    self.mouthed = self.objlist[data[1]]
                    #print("Consumed State Repair")
        elif self.mouthed != data[1]:
            self.mouthed = data[1]
            #print("Consumed State Repair")
        #print("mouthed test passed")
        if data[2] != self.mouthfull:
            self.mouthfull = data[2]
            #print("Jowel Repair")
        #print("mouthfull test passed")
        if data[3] != []:
            if self.inmouth != []:
                for num in range(len(data[3])):
                    obj = self.objlist[data[3][num]]
                    if not obj in self.inmouth:
                        self.inmouth[num] = obj
                        #print("Mouth Contents Repair")
            elif data[3] != self.inmouth:
                for num in data[3]:
                    self.inmouth.append(self.objlist[num])
                #print("Mouth Contents Repair")
        elif data[3] != self.inmouth:
            self.inmouth = data[3]
            #print("Mouth Contents Repair")
        #print("inmouth test passed")
        if data[4][0] != self.speed[0]:
            self.speed[0] = data[4][0]
            #print("Speed Repair")
        if data[4][1] != self.speed[1]:
            self.speed[1] = data[4][1]
            #print("Speed Repair")
        #print("speed test passed")
        if data[5][0] != self.location[0]:
            self.location[0] = data[5][0]
            #print("Locus Repair")
        if data[5][1] != self.location[1]:
            self.location[1] = data[5][1]
            #print("Locus Repair")
        #print("locus test passed")
        if data[6] != self.lastkeys:
            self.lastkeys = data[6]
            #print("Key Stroke Repair")
        #print("key test passed")

    #calculate the top,bottom,left,and right
    def getpoints(self):
        """self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.left = (int(self.location[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]+self.spriteSize[1]))"""
        if self.dir == "right":
            self.top = (int(self.location[0]), int(self.location[1]-int(self.sizey/2)))
            self.bottom = (int(self.location[0]), self.location[1]+int(self.sizey/2)-1)
            self.right = (self.location[0]+int(self.sizex/2)-1, self.location[1]-1)
            self.left = (self.location[0]-int(self.sizex/2), self.location[1]-1)
        else:
            self.top = (int(self.location[0])-1, int(self.location[1]-int(self.sizey/2)))
            self.bottom = (int(self.location[0])-1, self.location[1]+int(self.sizey/2)-1)
            self.right = (self.location[0]+int(self.sizex/2)-1, self.location[1]-1)
            self.left = (self.location[0]-int(self.sizex/2), self.location[1]-1)
        try:
            if self.getTileType(self.left) == "Floor45":
                if self.getTileFlip(self.left) == "0":
                    self.left = (self.location[0]-int(self.sizex/2), self.location[1]-1)
                elif self.getTileFlip(self.left) == "1":
                    self.left = (self.location[0]-int(self.sizex/2), self.location[1]-8-1)
            elif self.getTileType(self.bottom) == "Floor45":
                if self.getTileFlip(self.bottom) == "0":
                    self.left = (self.location[0]-int(self.sizex/2), self.location[1]-1)
                elif self.getTileFlip(self.bottom) == "1":
                    self.left = (self.location[0]-int(self.sizex/2), self.location[1]-8-1)
            if self.getTileType(self.right) == "Floor45":
                if self.getTileFlip(self.right) == "0":
                    self.right = (self.location[0]+int(self.sizex/2)-1, self.location[1]-8-1)
                elif self.getTileFlip(self.right) == "1":
                    self.right = (self.location[0]+int(self.sizex/2)-1, self.location[1]-1)
            if self.getTileType(self.bottom) == "Floor45":
                if self.getTileFlip(self.bottom) == "0":
                    self.right = (self.location[0]+int(self.sizex/2)-1, self.location[1]-8-1)
                elif self.getTileFlip(self.bottom) == "1":
                    self.right = (self.location[0]+int(self.sizex/2)-1, self.location[1]-1)
        except:
            pass

    def drawPoints(self):
        try:
            pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-self.camera.xpos,self.top[1]-self.camera.ypos,1,1))
            pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-self.camera.xpos,self.bottom[1]-self.camera.ypos,1,1))
            pygame.draw.rect(self.renderLayer,(0,216,255),(self.left[0]-self.camera.xpos,self.left[1]-self.camera.ypos,1,1))
            pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-self.camera.xpos,self.right[1]-self.camera.ypos,1,1))
            #time.sleep(0.01)
        except:
            pass

    def setCollideBoxSize(self,xSize,ySize):
        if self.crouching==True:
            print("yee")
        self.sizex = xSize
        self.sizey = ySize
        self.getpoints()
        if issubclass(type(self),Character):
            for obj in self.collide:
                if isinstance(obj,platform):
                    if self.bottom[1] > obj.top[1] and self.top[1] <= obj.top[1]:
                        self.location[1] += obj.top[1]-self.bottom[1]
        if self.grounded == True:
            if not self.collisionCheck(self.bottom):
                dist = self.distanceToCollide(self.bottom,1,1)
                if dist < xSize:
                    self.location[1] += dist
                    self.getpoints()
            else:
                dist = self.distanceToNotCollide(self.bottom,1,-1)
                if dist > -xSize:
                    self.location[1] += dist
                    self.getpoints()
                #print("collide box func call change")

    def sendPop(self):
        self.sendList = [self.crouching]
        if self.mouthed != None:
            self.sendList.append(self.objlist.index(self.mouthed))
        else:
            self.sendList.append(None)
        self.sendList.append(self.mouthfull)
        if self.inmouth != []:
            mouthIndexList = []
            for item in self.inmouth:
                mouthIndexList.append(self.objlist.index(item))
            self.sendList.append(mouthIndexList)
        else:
            self.sendList.append(self.inmouth)
        self.sendList.append(self.speed)
        self.sendList.append(self.location)
        self.sendList.append(self.lastkeys)
        self.sendList.append(self.ID)

    def update(self, cam):
        #self.speed = [0,0]
        if self.actTimer > 0:
            self.actTimer -= 1
            #print("dip")
        self.ladderCollide = 0
        self.sendPop()
        self.move()
        #print(self.blockedTop,self.blockedLeft,self.blockedRight,self.grounded)
        #print(self.bottom)
        #print(self.getTileType(self.top), self.getTileType(self.left), self.getTileType(self.right), self.getTileType(self.left))
        self.camera = cam
        self.animate()
        self.render()
        #if clicked
        """pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-cam.xpos,self.top[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-cam.xpos,self.bottom[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,216,255),(self.left[0]-cam.xpos,self.left[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-cam.xpos,self.right[1]-cam.ypos,1,1))"""
        #if isinstance(self, Player):
            ##print(self.speed[0],self.speed[1])
        #print(self.getTileType(self.bottom))
        self.wasBlockedLeft = self.blockedLeft
        self.wasBlockedRight = self.blockedRight
        self.wasBlockedTop = self.blockedTop
        self.wasGrounded = self.grounded

    def render(self):
        #render sprite at location
        self.animFrame = Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][0]
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName][self.animFrame]
        ##print(f"{self.grounded}\b")
        self.sprite = pygame.transform.scale(self.sprite,(self.spriteSize[0],self.spriteSize[1]))
        ##print(self.sprite.get_size())
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
        #if the length is 3, the sprite needs rotated
        if len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) == 3:
             self.sprite.blit(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),(0,0))
        #if the length is 4, the sprite needs flipped
        elif len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) == 4:
             self.sprite.blit(pygame.transform.flip(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),True,False),(0,0))
        self.sprite.blit(self.pallateApply(self.pallate, self.sprite),(0,0))
        self.sprite.set_colorkey((0,255,62))
        if self.dir == "right":
            self.renderLayer.blit(self.sprite,
                                  (int(self.location[0]-self.camera.xpos-(self.spriteSize[0]/2)),
                                   int(self.location[1]-self.camera.ypos-(self.spriteSize[1]/2))),
                                  (0,0,self.spriteSize[0],self.spriteSize[1]))
        else:
            self.renderLayer.blit(pygame.transform.flip(self.sprite,1,0), (int(self.location[0]-self.camera.xpos-(self.spriteSize[0]/2)),int(self.location[1]-self.camera.ypos-(self.spriteSize[1]/2))), (0,0,self.spriteSize[0],self.spriteSize[1]))
        
    def pallateApply(self, pallate, sprite):
        #for testing
        #test = pygame.display.set_mode((700,350))
        colorSprite = pygame.Surface(sprite.get_size())
        for color in range(len(pallate)):
            """#start of test
            test.blit(pygame.transform.scale(sprite,(350,350)),(0,0))
            test.blit(pygame.transform.scale(colorSprite,(350,350)),(350,0))
            pygame.display.flip()
            test.fill((0,255,68))
            time.sleep(1)
            #end of test"""
            sprite.set_colorkey(Datafile["Character"]["Pallates"][self.charName]["Normal"][color])
            colorSprite.fill(pallate[color])
            colorSprite.blit(sprite, (0,0))
            sprite.blit(colorSprite, (0,0))
            #print(color)#Datafile["Character"]["Pallates"][self.charName]["Normal"][color])
        """#start of test
        test.blit(pygame.transform.scale(sprite,(350,350)),(0,0))
        test.blit(pygame.transform.scale(colorSprite,(350,350)),(350,0))
        pygame.display.flip()
        test.fill((0,255,68))
        time.sleep(1)
        #end of test"""
        return colorSprite

    def playAnimation(self, animationName):
        if animationName != self.animation:
            if self.animType == "Stop":
                self.animBacklog = animationName
            else:
                self.animItr = 0
                self.animType = "Loop"
                self.animFrameNumber = 0
                self.animation = animationName

    def playAnimationOnce(self, animationName, animNext):
        if animationName != self.animation:
            self.animItr = 0
            self.animType = "Stop"
            self.animFrameNumber = 0
            self.animation = animationName
            self.animBacklog = animNext
        
    def animate(self):
        self.animItr += 1
        if self.animItr == Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][1]:
            self.animFrameNumber += 1
            self.animItr = 0
        if self.animFrameNumber == len(Datafile["Character"]["Animations"][self.charName][self.animation]):
            if self.animType == "Loop":
                self.animFrameNumber = 0
                self.animItr = 0
            else:
                self.animType = "Loop"
                self.playAnimation(self.animBacklog)

    def moveTo(self):
        #move to the set location at the given speed
        pass

    def collisionCorrect(self):
        #print(self.blockedLeft,self.blockedRight,self.blockedTop,self.grounded)
        if self.collisionCheck(self.location):
            #print("dip")
            leftDist = self.distanceToNotCollideInRange(self.location,0,-1)
            rightDist = self.distanceToNotCollideInRange(self.location,0,1)
            topDist = self.distanceToNotCollideInRange(self.location,1,-1)
            bottomDist = self.distanceToNotCollideInRange(self.location,1,1)
            distList = [topDist, rightDist, bottomDist, leftDist]
            print(distList)
            #distNameList = ["TOP","RIGHT","BOTTOM","LEFT"]
            finalDistIndex = 0
            for index in range(len(distList)):
                #print(f"Checking {distNameList[finalDistIndex]} against {distNameList[index]}")
                if abs(distList[index]) < abs(distList[finalDistIndex]):
                    finalDistIndex = index
                    #print(f"Switching to {distNameList[index]}")
            print(finalDistIndex)
            print(distList[finalDistIndex])
            if finalDistIndex == 0 or finalDistIndex == 2:
                self.location[1] += distList[finalDistIndex]
            else:
                self.location[0] += distList[finalDistIndex]
                
        if self.grounded == True:
            if self.blockedTop == False:
                self.location[1]+=self.distanceToNotCollide(self.bottom,1,-1)+1
                #print("collide test bottom func call change")
            """elif self.blockedLeft == False:
                self.location[0]+=self.distanceToNotCollide(self.bottom,0,-1)+1
            elif self.blockedRight == False:
                self.location[0]+=self.distanceToNotCollide(self.bottom,0,1)-1"""
            #self.render()
            #time.sleep(0.1)
            self.getpoints()
            #else:
                #give up
        if self.blockedTop == True:
            if self.grounded == False:
                self.location[1]+=self.distanceToNotCollide(self.top,1,1)-1
            """elif self.blockedLeft == False:
                self.location[0]+=self.distanceToNotCollide(self.top,0,-1)-1
            elif self.blockedRight == False:
                self.location[0]+=self.distanceToNotCollide(self.top,0,1)+1"""
            #self.render()
            #time.sleep(0.1)
            self.getpoints()
            #else:
                #give up
        if self.blockedLeft == True:
            if self.blockedRight == False:
                self.location[0]+=self.distanceToNotCollide(self.left,0,1)-1
            elif self.blockedTop == False:
                self.location[1]+=self.distanceToNotCollide(self.left,1,-1)+1
            elif self.grounded == False:
                self.location[1]+=self.distanceToNotCollide(self.left,1,1)-1
                #print("collide test left func call change")
            #self.render()
            #time.sleep(0.1)
            self.getpoints()
            #else:
                #give up
        if self.blockedRight == True:
            if self.blockedLeft == False:
                self.location[0]+=self.distanceToNotCollide(self.right,0,-1)+1
            elif self.blockedTop == False:
                self.location[1]+=self.distanceToNotCollide(self.right,1,-1)-1
            elif self.grounded == False:
                self.location[1]+=self.distanceToNotCollide(self.right,1,1)+1
                #print("collide test left func call change")
            #self.render()
            #time.sleep(0.1)
            self.getpoints()
            #else:
                #give up

    def collisionTests(self):
        #center check
        if self.collisionCheck(self.bottom) == True:
            self.grounded = True
        else:
            self.grounded = False
        if self.collisionCheck(self.top) == True:
            self.blockedTop = True
        else:
            self.blockedTop = False
        if self.collisionCheck(self.left) == True:
            self.blockedLeft = True
        else:
            self.blockedLeft = False
        if self.collisionCheck(self.right) == True:
            self.blockedRight = True
        else:
            self.blockedRight = False

    def distanceToCollide(self,point,searchAxis,searchDirection):
        try:
            itr = 0
            if searchAxis == 0:
                while True:
                    """if isinstance(self, Player):
                        pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]+itr-self.camera.xpos,self.top[1]-self.camera.ypos,1,1))
                        pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]+itr-self.camera.xpos,self.bottom[1]-self.camera.ypos,1,1))
                        pygame.draw.rect(self.renderLayer,(0,216,255),(self.left[0]+itr-self.camera.xpos,self.left[1]-self.camera.ypos,1,1))
                        pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]+itr-self.camera.xpos,self.right[1]-self.camera.ypos,1,1))"""
                    if self.collisionCheck((point[searchAxis]+itr,point[1])):   
                        break
                    itr += 1*searchDirection
            else:
                while True:
                    """if isinstance(self, Player):
                        pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-self.camera.xpos,self.top[1]-self.camera.ypos+itr,1,1))
                        pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-self.camera.xpos,self.bottom[1]-self.camera.ypos+itr,1,1))
                        pygame.draw.rect(self.renderLayer,(0,216,255),(self.left[0]-self.camera.xpos,self.left[1]-self.camera.ypos+itr,1,1))
                        pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-self.camera.xpos,self.right[1]-self.camera.ypos+itr,1,1))
                        #time.sleep(0.05)"""
                    if self.collisionCheck((point[0],point[searchAxis]+itr)):   
                        break
                    itr += 1*searchDirection
            return itr
        except Exception as e:
            return 4#print(e)
            
    def distanceToNotCollide(self,point,searchAxis,searchDirection):
        try:
            itr = 0
            if point[0] >= self.currentLevel.maxiX*8:
                return -(point[0]-self.currentLevel.maxiX*8)-1
            elif point[1] >= self.currentLevel.maxiY*8:
                return -(point[1]-self.currentLevel.maxiY*8)-1
            else:
                if searchAxis == 0:
                    while True:
                        if not self.collisionCheck((point[searchAxis]+itr,point[1])):   
                            break
                        itr += 1*searchDirection
                else:   
                    while True:
                        if self.collisionCheck((point[0],point[searchAxis]+itr)) == False:   
                            break
                        itr += 1*searchDirection

            return itr
        except Exception as e:
            print(e)
    
    def move(self):
        if self.mode != "dead":
            if (self.speed[0] > 0 and not self.blockedRight) or (self.speed[0] < 0 and not self.blockedLeft):
                if self.speed[0] > 0:
                    self.location[0] += math.ceil(self.speed[0])
                else:
                    self.location[0] += math.floor(self.speed[0])
            #else:
                #self.speed[0] = 0
            if (self.speed[1] > 0 and not self.grounded) or (self.speed[1] < 0 and not self.blockedTop):
                if self.speed[1] > 0:
                    self.location[1] += math.ceil(self.speed[1]/2)
                else:
                    self.location[1] += math.floor(self.speed[1]/2)
            #else:
                #self.speed[1] = 0
            self.getpoints()
            if self.grounded == True:
                dist = self.distanceToCollide(self.bottom,1,1)
                if abs(dist) < 16:
                    self.location[1] += dist
            self.getpoints()
            #self.collisionTest()
        else:
            if self.speed[0] > 0:
                    self.location[0] += math.ceil(self.speed[0])
            else:
                self.location[0] += math.floor(self.speed[0])
            if self.speed[1] > 0:
                    self.location[1] += math.ceil(self.speed[1]/2)
            else:
                self.location[1] += math.floor(self.speed[1]/2)

    def getTileType(self,point):
        """try:
            pygame.draw.rect(self.renderLayer,(0,255,255),(point[0]-self.camera.xpos,point[1]-self.camera.ypos,8,8))
        except:
            pass"""
        try:
            tilecountx = (point[0]//8)
            ##print(f"{self.charName} {self.pallateName} has it's x test")
            tilecounty = (point[1]//8)
            ##print(f"{self.charName} {self.pallateName} has it's y test")
            ##print(tilecountx,tilecounty)
            tilenum = str(self.currentLevel.collisionData[tilecounty][tilecountx])
            ##print(f"{self.charName} {self.pallateName} has it's tile")
            tiletype = (Datafile["CollisionKey"][tilenum])
            return tiletype
        except:
            return "Solid"
    
    def getTileFlip(self,point):
        try:
            tilecountx = (point[0]//8)
            ##print(f"{self.charName} {self.pallateName} has it's x test")
            tilecounty = (point[1]//8)
            ##print(f"{self.charName} {self.pallateName} has it's y test")
            ##print(tilecountx,tilecounty)
            tilenum = str(self.currentLevel.flipmap[tilecounty][tilecountx])
            ##print(f"{self.charName} {self.pallateName} has it's tile")
            return tilenum
        except:
            return "0"
    
    def collisionCheck(self, point):
        ##print(f"{self.charName} {self.pallateName} is testing collision")
        try:
            #you should check all four points on character.
            #check if colliding w/ platforms too
            #if  collisions contains platforms:
            for obj in self.objlist:
                if isinstance(obj,platform):
                    #print("checking...")
                    #if platform isn't semisolid, returns true if within borders
                    if obj.semisolid != True:
                        if point[0] <= obj.right[0] and point[0] >= obj.left[0]:
                            if point[1] >= obj.top[1] and point[1] <= obj.bottom[1]:
                                return True
                    #else, only triggers if a secondary point is not within the borders
                    elif (self.bottom[1] <= obj.top[1]+4 and self.speed[1] >= 0):
                        if point[0] <= obj.right[0] and point[0] >= obj.left[0]:
                            if point[1] >= obj.top[1] and point[1] <= obj.bottom[1]:
                                return True
            #find what tile type they are on
            if isinstance(self, Player):
                print(self.speed)
            tilecountx = int(point[0]//8)
            if point[0] <= 0 or point[1] <= 0:
                return True
            ##print(f"{self.charName} {self.pallateName} has it's x test")
            tilecounty = int(point[1]//8)
            point = (int(point[0]),int(point[1]))
            ##print(f"{self.charName} {self.pallateName} has it's y test")
            #print(tilecountx,tilecounty)
            tilenum = str(self.currentLevel.collisionData[tilecounty][tilecountx])
            #print(f"{self.charName} {self.pallateName} has it's tile")
            tiletype = (Datafile["CollisionKey"][tilenum])
            #print(f"{self.charName} {self.pallateName} has it's tiletype")
            ##print(tiletype)
            if tiletype != "Air":
                if self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 1:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][abs(7-point[0]%8)][point[1]%8] == 1:
                        #print(f"{self.charName} {self.pallateName} is reigestering collision with an x-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                elif self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 2:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8][abs(7-point[1]%8)] == 1:
                        ##print(f"{self.charName} {self.pallateName} is reigestering collision with a y-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                elif self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 3:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][abs(7-point[0]%8)][abs(7-point[1]%8)] == 1:
                        ##print(f"{self.charName} {self.pallateName} is reigestering collision with a dual-flipped block: type {tiletype}")
                        return True
                    else:
                        return False    
                else:
                    #check if out of bounds. if so, treat as if solid
                    thing =  Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8]
                    if thing[point[1]%8] == 1:
                        #print(f"{self.charName} {self.pallateName} is reigestering collision with a non-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
            else:
                return False
        except Exception as e:
            #print(self.right[0],self.currentLevel.maxiX*8)
            #raise e
            #print(e)
            #print(self.location[0])
            return True
            ##print(f"{self.charName} {self.pallateName} is reigestering collision")
                
    def slide(self):
        if self.flap == False:
            if self.dir == "left":
                self.speed[0] = -4
            else:
                self.speed[0] = 4
            self.slideItr = 16
            self.flap = True
            
    def getLadderCollide(self):
        if self.getTileType(self.bottom) == "Ladder":
            #print("Dip")
            self.ladderCollide += 1
        if self.getTileType(self.top) == "Ladder":
            #print("Dip")
            self.ladderCollide += 1
        if self.getTileType(self.left) == "Ladder":
            #print("Dip")
            self.ladderCollide += 1
        if self.getTileType(self.right) == "Ladder":
            #print("Dip")
            self.ladderCollide += 1
        
    def slideLoop(self):
        self.setCollideBoxSize(16,14)
        #print(self.speed[0])
        if self.dir == "left":
                self.speed[0] += 0.25
        else:
                self.speed[0] -= 0.25
        if self.grounded == False:
            fall = self.distanceToCollide(self.bottom,1,1)
            if fall < 16:
                self.location[1] += fall
                self.grounded = True
        """else:
            if self.dir == "left":
                if self.blockedLeft == True:
                    rise = self.distanceToNotCollide((int(self.right[0]+self.speed[0]),int(self.left[1]+self.speed[1])),1,-1)
                    if rise > -16:
                        self.location[1] += rise
            else:
                if self.blockedRight == True:
                    rise = self.distanceToNotCollide((int(self.right[0]+self.speed[0]),int(self.right[1]+self.speed[1])),1,-1)
                    if rise > -16:
                        self.location[1] +=ladderUp rise"""
            
        self.slideItr -= 1
        self.playAnimation("Slide")
        #print(self.slideItr)

    def ladderUp(self):
        #print("Triggered")
        if self.ladderCollide > 0:
            if self.climb == True:
                #self.grounded = True
                self.speed[1] = -4
            else:
                if self.getTileType(self.left) != "Ladder":
                    if self.getTileType(self.location) != "Ladder":
                        self.location[0] += (16-self.location[0]%8)
                    else:
                        self.location[0] += 8-self.location[0]%8
                elif self.getTileType(self.right) != "Ladder":
                    if self.getTileType(self.location) != "Ladder":
                        self.location[0] -= 8+(self.location[0]%8)
                    else:
                        self.location[0] -= self.location[0]%8
            self.climb = True
            self.flap = False
            self.grounded = False
            self.floating = False
            self.playAnimation("Climb")
        
    def ladderDown(self):
        if self.ladderCollide > 0:
            if self.climb == True:
                #self.grounded = True
                self.speed[1] = 4
            else:
                if self.getTileType(self.left) != "Ladder":
                    if self.getTileType(self.location) != "Ladder":
                        self.location[0] += (16-self.location[0]%8)
                    else:
                        self.location[0] += 8-self.location[0]%8
                elif self.getTileType(self.right) != "Ladder":
                    if self.getTileType(self.location) != "Ladder":
                        self.location[0] -= 8+(self.location[0]%8)
                    else:
                        self.location[0] -= self.location[0]%8
            self.climb = True
            self.flap = False
            self.floating = False
            self.playAnimation("Descend")

    def swimUp(self):
        if self.speed[1] > -2:
            self.speed[1] += -1
        else:
            self.speed[1] = -2
        self.grounded = False
        if not self.checkIfPointSubmerged(self.top) and self.speed[1] <= -2:
            #print("dip")
            self.jump()
    def swimDown(self):
        if self.speed[1] < 2:
            self.speed[1] += 1

    def fall(self):
        if self.floating == False:
            if self.mouthfull == 0:
                self.setCollideBoxSize(16,16)
                #if isinstance(self,Player):
                #    print(self.fallingTime)
                if self.fallingTime >= 60:
                    self.playAnimation("Roll")
                elif self.speed[1] == 0:
                    self.playAnimationOnce("Roll","Fall")
                elif self.speed[1] > 0:
                    self.playAnimation("Fall")
                else:
                    self.playAnimation("Jump")
            else:
                self.setCollideBoxSize(16,22)
                self.playAnimation("FullJump")
        else:
            self.playAnimation("Float")
            
    def walk(self):
        if self.crouching == False:
            if self.attack == False:
                if self.floating == False:
                    if self.mouthfull == 0:
                        self.setCollideBoxSize(16,16)
                        if self.grounded == True:
                            self.playAnimation("Walk")
                        else:
                            self.fall()
                    else:
                        self.setCollideBoxSize(16,22)
                        self.playAnimation("FullWalk")
                if self.dir == "right":
                    if self.blockedRight == False:
                        if self.speed[0] < 1:
                            self.speed[0] += 1
                        else:
                            self.speed[0] = 1
                elif self.dir == "left":
                    if self.blockedLeft == False:
                        if self.speed[0] > -1:
                            self.speed[0] += -1
                        else:
                            self.speed[0] = -1
                else:
                    self.speed[0] = 0
            else:
                self.speed[0] = 0
        try:
            self.behaviorTimer += 1
            if self.behaviorTimer >= self.behaviors[self.behaviorItr][1]:
                self.behaviorTimer = 0
                self.behaviorItr += 1
        except:
            pass
        
    def run(self):
        if self.attack == False:
            if self.floating == False:
                if self.mouthfull == 0:
                    self.setCollideBoxSize(16,16)
                    if self.grounded == True:
                        self.playAnimation("Run")
                    else:
                        self.fall()
                else:
                    self.setCollideBoxSize(16,22)
                    self.playAnimation("FullWalk")
            if self.dir == "right":
                if self.blockedRight == False:
                    if self.speed[0] < 2:
                        self.speed[0] += 2
                    else:
                        self.speed[0] = 2
            elif self.dir == "left":
                if self.blockedLeft == False:
                    if self.speed[0] > -2:
                        self.speed[0] += -2
                    else:
                        self.speed[0] = -2
            try:
                self.behaviorTimer += 1
                if self.behaviorTimer >= self.behaviors[self.behaviorItr][1]:
                    self.behaviorTimer = 0
                    self.behaviorItr += 1
            except:
                pass
            
    def crouch(self):
        self.setCollideBoxSize(8,8)
        if self.slideItr == 0:
            self.speed[0] = 0
        self.crouching = True
        #if isinstance(self, Player):
            ##print(Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])])
        if self.getTileType(self.bottom) == "Floor45":
            flip = int(self.getTileFlip(self.bottom))
            if flip == 0:
                if self.dir == "right":
                    self.playAnimation("Crouch45")
                else:
                    self.playAnimation("Crouch135")
            elif flip == 1:
                if self.dir == "right":
                    self.playAnimation("Crouch135")
                else:
                    self.playAnimation("Crouch45")
            else:
                self.playAnimation("Crouch")
        else:
            self.playAnimation("Crouch")
        try:
            self.behaviorTimer += 1
            if self.behaviorTimer >= self.behaviors[self.behaviorItr][1]:
                self.behaviorTimer = 0
                self.behaviorItr += 1
                self.crouching = False
        except:
            pass
        
    def wait(self):
        #self.speed[0] = 0
        if self.climb == False:
            if self.grounded == True:
                if self.crouching == False:
                    self.setCollideBoxSize(16,16)
                    if self.mouthfull == 0:
                        #if isinstance(self, Player):
                            ##print(Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])])
                        #if Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])] == "Floor45":
                        if self.getTileType(self.bottom) == "Floor45":
                            if self.currentLevel.file["FlipMap"][self.bottom[1]//8][self.bottom[0]//8] == 0:
                                if self.dir == "right":
                                    self.playAnimation("Stand45")
                                else:
                                    self.playAnimation("Stand135")
                            elif self.currentLevel.file["FlipMap"][self.bottom[1]//8][self.bottom[0]//8] == 1:
                                if self.dir == "right":
                                    self.playAnimation("Stand135")
                                else:
                                    self.playAnimation("Stand45")
                            else:
                                self.playAnimation("Idle")
                        else:
                            self.playAnimation("Idle")
                    else:
                        self.playAnimation("Full")
                        self.setCollideBoxSize(16,22)
                else:
                    self.setCollideBoxSize(16,8)
            else:
                self.fall()
        else:
            if self.speed[1] == 0:
                self.playAnimation("LadderIdle")
        try:
            self.behaviorTimer += 1
            if self.behaviorTimer >= self.behaviors[self.behaviorItr][1]:
                self.behaviorTimer = 0
                self.behaviorItr += 1
        except:
            pass

    def jump(self):
        if self.flap == False and self.attack == False:
            if self.blockedTop == False:
                self.flap = True
                self.climb = False
                if self.mouthfull == 0:
                    self.playAnimation("Jump")
                else:
                    self.playAnimation("FullJump")
                #self.location[1] -= 2
                self.grounded = False
                self.speed[1] = -(self.jumpHeight)
        try:
            self.behaviorTimer = 0
            self.behaviorItr += 1
            self.flap = False
        except:
            pass
        
    def float(self):
        self.setCollideBoxSize(16,16)
        if self.flap == False and self.attack == False and self.mouthfull == 0:
            self.flap = True
            self.flap = True
            if self.floating == False:
                self.floating = True
                self.playAnimationOnce("Inflate", "Float")
            else:
                self.playAnimationOnce("Flap","Float")
            self.speed[1] = int(-self.jumpHeight/2)
        try:
            self.behaviorTimer = 0
            self.behaviorItr += 1
            self.flap = False
        except:
            pass

    def flip(self):
        if self.dir == "right":
            self.dir = "left"
        else:
            self.dir = "right"
        try:
            self.behaviorTimer = 0
            self.behaviorItr += 1
        except:
            pass

    def findRouteOut(self,point):
        up = self.distanceToNotCollideInRange(point,1,-1)
        down = self.distanceToNotCollideInRange(point,1,1)
        left = self.distanceToNotCollideInRange(point,0,-1)
        right = self.distanceToNotCollideInRange(point,0,1)
        #print(up,down,left,right)
        if abs(up)>abs(down):
            if abs(left)>abs(right):
                return (right,down)
            else:
                return (left,down)
        else:
            if abs(left)>abs(right):
                return (right,up)
            else:
                return [left,up]

    def distanceToNotCollideInRange(self,point,searchAxis,searchDirection):
        try:
            itr = 0
            if point[0] >= self.currentLevel.maxiX*8 or point[1] >= self.currentLevel.maxiY*8:
                return 0
            else:
                if searchAxis == 0:
                    if searchDirection == 1:
                        while itr < 16:
                            if not self.collisionCheck((point[searchAxis]+itr,point[1])):   
                                break
                            itr += 1*searchDirection
                    else:
                        while itr > -16:
                            if not self.collisionCheck((point[searchAxis]+itr,point[1])):   
                                break
                            itr += 1*searchDirection
                else:
                    if searchDirection == 1:
                        while itr < 16:
                            if not self.collisionCheck((point[0],point[1]+itr)):   
                                break
                            itr += 1*searchDirection
                    else:
                        while itr > -16:
                            if not self.collisionCheck((point[0],point[1]+itr)):   
                                break
                            itr += 1*searchDirection
            return itr
        except:
            print("dip")
            return 0
    def submergedCheck(self):
        self.submerged = 0
        for obj in self.collide:
            if isinstance(obj,fluid):
                if self.top[1] > obj.top[1]:
                   self.submerged += 1 
                if self.bottom[1] < obj.bottom[1]:
                   self.submerged += 1
                if self.left[0] > obj.left[0]:
                   self.submerged += 1
                if self.right[0] < obj.right[0]:
                   self.submerged += 1
            if self.submerged > 3:
                return True
            else:
                return False

class Character(Object):
    def __init__(self, ID, charName, xlocation, ylocation, arrayDestination, renderLayer, pallate, Level, Uniques):
        Object.__init__(self, ID, charName, xlocation, ylocation, arrayDestination, renderLayer, pallate, Level)
        self.ability = Uniques[0]
        self.lastkeys = pygame.key.get_pressed()
        self.mode = "alive"
        self.inhaled = False
        self.mouthed = None
        self.inmouth = []
        self.inhalingnum = 0
        self.speedbuffer = [0,0]
        self.speed = [0,0]
        self.pallateName = pallate
        self.pallate = Datafile["Character"]["Pallates"][self.charName][pallate]
        self.maxfallspeed = 3
        self.fallspeed = 1
        self.fallingTime = 0
        self.walkSpeed = 1
        self.runSpeed = 2
        self.swimSpeed = 1
        self.jumpHeight = 15
        self.actTimer = 0
        self.grounded = False
        self.blockedTop = False
        self.blockedRight = False
        self.blockedLeft = False
        self.wasGrounded = False
        self.wasBlockedTop = False
        self.wasBlockedRight = False
        self.wasBlockedLeft = False
        self.StunItr = 0
        self.blockedTop = False
        self.floating = False
        self.flap = False
        self.crouching = False
        self.climb = False
        self.ladderCollide = 0
        self.submerged = 0
        self.slideItr = 0
        self.walking = False
        self.attack = False
        self.firePressed = False
        self.mouthfull = 0
        self.multiplayerMode = Uniques[1]
        #prepares the list for network communications
        self.sendList = [self.crouching]
        if self.mouthed != None:
            self.sendList.append(self.objlist.index(self.mouthed))
        else:
            self.sendList.append(None)
        self.sendList.append(self.mouthfull)
        if self.inmouth != []:
            self.sendList.append(self.objlist.index(self.inmouth))
        else:
            self.sendList.append([])
        self.sendList.append(self.speed)
        self.sendList.append(self.location)
        self.sendList.append(self.lastkeys)
        self.sendList.append(self.ID)
        #self.sendList = [self.crouching, self.objlist.index(self.mouthed),self.mouthfull,self.objlist.index(self.inmouth),self.speed,self.location,self.lastkeys]
        
        #checks if a point is under the collision box of a fluid block

    def hatRender(self):
        try:
            if self.ability != "copy":
                #pull relevant hat sprite
                anim = "Normal"
                frameno = 0
                hatframe = Datafile["Hats"]["Animations"][self.ability][anim][frameno][0]
                spritesize = Datafile["Hats"]["Size"][hatframe]
                coordinates = Datafile["Hats"]["Coordinates"][hatframe]
                #render on top of normal sprite
                hatsprite = pygame.Surface((spritesize[0],spritesize[1]))
                hatsprite.blit(Sheet, (0,0),(coordinates[0],coordinates[1],spritesize[0],spritesize[1]))
                #if the length is 3, the sprite needs rotated
                if len(Datafile["Hats"]["Animations"][self.ability][anim][frameno]) == 3:
                     hatsprite.blit(pygame.transform.rotate(hatsprite,Datafile["Hats"]["Animations"][self.ability][anim][frameno][2]),(0,0))
                #if the length is 4, the sprite needs flipped
                elif len(Datafile["Hats"]["Animations"][self.ability][anim][frameno]) == 4:
                     hatsprite.blit(pygame.transform.flip(pygame.transform.rotate(hatsprite,Datafile["Hats"]["Animations"][self.ability][anim][frameno][2]),True,False),(0,0))
                hatsprite.set_colorkey((0,255,62))
                if self.dir == "right":
                    self.renderLayer.blit(hatsprite,
                                          (int(self.location[0]-self.camera.xpos-spritesize[0]/2),
                                          int(self.location[1]-self.camera.ypos-(spritesize[1]*3/4)-self.spriteSize[1]/2)),
                                          (0,0,spritesize[0],spritesize[1]))
                else:
                    self.renderLayer.blit(pygame.transform.flip(hatsprite,1,0),
                                          (int(self.location[0]-self.camera.xpos-spritesize[0]/2),
                                          int(self.location[1]-self.camera.ypos-(spritesize[1]*3/4)-self.spriteSize[1]/2)),
                                          (0,0,spritesize[0],spritesize[1]))

        except Exception as e:
            raise e

    def checkIfPointSubmerged(self, point):
        for obj in self.collide:
            if isinstance(obj,fluid):
                if point[1] > obj.top[1] and point[1] < obj.bottom[1]:
                    if point[0] < obj.right[0] and point[0] > obj.left[0]:
                        return True
        return False
    
    #same as above, but for the whole object
    
    def squishTop(self):
        if self.floating == False and self.mouthfull == False and self.speed[1] < 0:
            if self.actTimer == 0:
                #print("squish here")
                self.setCollideBoxSize(8,8)
                self.getpoints()
                if not self.collisionCheck(self.top):
                    self.location[1] += self.distanceToCollide(self.top,1,-1)
                self.getpoints()
                self.playAnimation("Crouch")
                self.actTimer = 10
                #print("Hitbox Was Squished")
        
class Player(Character):
    def __init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques):
        Character.__init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques)
        self.attack = False
        self.startInhale = False
        self.respawnpoint = (xlocation,ylocation)

    def update(self,cam):
        #self.walk()
        self.pallate = Datafile["Character"]["Pallates"][self.charName][self.ability]
        #self.speed = [0,0]
        if self.actTimer > 0:
            self.actTimer -= 1
            #print("dip")
        self.camera = cam
        self.ladderCollide = 0
        self.sendPop()
        #print(self.location)
        #print(self.blockedTop,self.blockedLeft,self.blockedRight,self.grounded)
        #print(self.bottom)
        #print(self.getTileType(self.top), self.getTileType(self.left), self.getTileType(self.right), self.getTileType(self.left))
        if(self.mode == "alive"):
            #print(self.location,self.blockedLeft,self.blockedRight,self.blockedTop,self.grounded)
            self.getLadderCollide()
            self.submergedCheck()
            self.playerScript()
            self.move()
            #self.run()
            #self.physicsSim()
            self.collisionTests()
            self.collisionCorrect()
            ##print(self.location)
        elif self.mode == "dead":
            self.deathfall(cam)
            self.move()
            self.physicsSim()
        elif self.mode == "goalgamejump":
            self.getLadderCollide()
            self.submergedCheck()
            self.goalGamePlayerScript()
            self.move()
            self.collisionTests()
            self.collisionCorrect()
        self.animate()
        self.drawPoints()
        self.render()
        self.hatRender()
        self.wasBlockedLeft = self.blockedLeft
        self.wasBlockedRight = self.blockedRight
        self.wasBlockedTop = self.blockedTop
        self.wasGrounded = self.grounded
        #print(self.location)

    def goalGamePlayerScript(self):
        self.collideWithObj()
        #run physics sim
        if self.grounded == False and self.climb == False:
            self.physicsSim()
        else:
            self.fallingTime = 0
            self.floating = False
            self.speed[1] = 0
        #grounded and ungrounded
        #check for input
        if self.actTimer > 0:
            self.keys = self.lastkeys
        if self.multiplayerMode == "HOST":
            self.keys = pygame.key.get_pressed()
            self.lastkeys = self.keys
        else:
            self.keys = self.lastkeys
        if self.keys[pygame.K_SPACE]:
            if self.slideItr == 0:
                if self.grounded:
                    self.jump()
        else:
            self.flap = False
            
            if self.attack == False and self.grounded == False:
                self.fallingTime += 1
            else:
                self.fallingTime == 0

    def playerScript(self):
        self.collideWithObj()
        #run physics sim
        if self.grounded == False and self.climb == False:
            self.physicsSim()
        else:
            self.fallingTime = 0
            self.floating = False
            self.speed[1] = 0
        #grounded and ungrounded
        #check for input
        if self.actTimer > 0:
            self.keys = self.lastkeys
        if self.multiplayerMode == "HOST":
            self.keys = pygame.key.get_pressed()
            self.lastkeys = self.keys
        else:
            self.keys = self.lastkeys
            
        if self.keys[pygame.K_i]:
            self.Kill()
            self.climb = False
        if self.keys[pygame.K_c]:
            #self.mode = "goalgamejump"
            if self.ability == "copy":
                self.ability = "beam"
                print("Ability switched to: BEAM")
            elif self.ability == "beam":
                self.ability = "copy"
                print("Ability switched to: COPY")
        #print(self.submerged)
        if self.attack == True or self.floating == True:
            self.fallspeed = 1
            self.maxfallspeed = 2
        elif self.climb == True:
            self.maxfallspeed = 0
        elif self.submerged > 2:
            #print("wet")
            self.fallingTime = 0
            self.fallspeed = 0.25
            self.maxfallspeed = 0.5
        else:
            self.fallspeed = 1
            self.maxfallspeed = 7
        #print(self.actTimer)
        if self.actTimer == 0:
            if self.keys[pygame.K_d]:
                if self.submerged > 2:
                    if self.actTimer == 0:
                        if self.attack == True or self.mouthfull > 0:
                            try:
                                getattr(abilityLib,f"{self.ability}Attack")(self)
                            except Exception as e:
                                #print(e)
                                abilityLib.Copy(self)
                                self.climb = False
                        else:
                            abilityLib.WaterSpit(self)
                else:
                    try:
                        getattr(abilityLib,f"{self.ability}Attack")(self)
                    except Exception as e:
                        #print(e)
                        abilityLib.Copy(self)
                        self.climb = False
                self.climb = False
            else:
                self.attack = False
                self.firePressed = False
            #print(self.ladderCollide)
            if self.keys[pygame.K_UP]:
                #print(self.ladderCollide,self.attack,self.mouthfull)
                for obj in self.collide:
                    if type(obj).__name__ == "door":
                        print("uppity")
                        obj.interact(self)
                if self.attack == False and self.mouthfull == 0:
                    if self.ladderCollide > 0:
                        self.ladderUp()
                    elif self.submerged > 2:
                        self.swimUp()
            if self.keys[pygame.K_z]:
                #print(self.speed[1])
                print(self.ladderCollide)
            if self.keys[pygame.K_DOWN]:
                if self.submerged > 2:
                    self.swimDown()
                else:
                    if self.grounded == True:
                        if self.mouthfull == 0:
                            self.crouch()
                        else:
                            self.playAnimationOnce("Swallow","Crouch")
                            self.mouthfull = 0
                            for item in self. inmouth:
                                try:
                                    item.respawn()
                                except:
                                    pass
                                item.mouthed = None
                            self.inmouth = []
                    if self.attack == False and self.mouthfull == 0:
                        if self.ladderCollide > 0:
                            self.ladderDown()
            else:
                self.crouching = False
                
            if self.keys[pygame.K_SPACE]:
                if self.slideItr == 0:
                    if self.grounded:
                        if self.crouching:
                            self.slide()
                        else:
                            self.jump()
                            self.climb = False
                    elif self.climb:
                        self.jump()
                        self.climb = False
                    else:
                        if self.submerged > 2 and not self.keys[pygame.K_UP]:
                            self.flap = True
                            self.swimUp()
                        else:
                            self.float()
            else:
                self.flap = False
            
            #if floating:
            if self.submerged > 2:
                if self.floating == True:
                    #push to top of water body
                    self.speed[1] = -5
                
            if self.slideItr > 0:
                self.slideLoop()

            if self.keys[pygame.K_LEFT] and self.attack == False and self.slideItr == 0:
                self.dir = "left"
                self.climb = False
                #if not blocked on left side
                """if self.blockedLeft == False:
                    self.speed[0] = -1"""
                if self.walking == True and self.floating == False:
                    self.run()
                else:
                    self.walk()
                
            elif self.keys[pygame.K_RIGHT] and self.attack == False and self.slideItr == 0:
                self.dir = "right"
                self.climb = False
                """if self.blockedRight == False:
                    self.speed[0] = 1"""
                if self.walking == True and self.floating == False:
                    self.run()
                else:
                    self.walk()
            else:
                if self.walking == True:
                    self.itr += 1
                    if self.itr == 10:
                        self.walking = False
                        self.itr = 0
                elif self.speed[0] > 0 or self.speed[0] < 0:
                    self.walking = True
                if self.slideItr == 0:
                    self.speed[0] = 0
                    if self.attack == False:
                        self.wait()
                            
            if self.attack == False and self.grounded == False:
                self.fallingTime += 1
            else:
                self.fallingTime == 0
                
            for obj in self.collide:
                #print("Dip")

                if isinstance(obj, Enemy):
                    #print(obj.inhaled)
                    if obj.inhaled == False:
                        self.Kill()
        
        
        #print(self.speed)#[1],self.maxfallspeed,self.speed[1])
    def physicsSim(self):
        if self.speed[1] < self.maxfallspeed:
            self.speed[1] += self.fallspeed
        elif self.speed[1] > self.maxfallspeed:
            self.speed[1] -= self.fallspeed
        else:
            self.speed[1] = self.maxfallspeed
        if self.blockedTop == True:
            self.squishTop()

    def Kill(self):
        if self.mode == "alive":
            #print("Player Death")
            self.mode = "dead"
            self.floating = False
            self.mouthfull = 0
            self.attack = False
            self.grounded = False
            for item in self.inmouth:
                try:
                    item.mouthed = None
                except:
                    pass
            self.inmouth = []
            self.mouthed = None
            time.sleep(1)
            self.speed[1] = -15
            self.maxfallspeed = 7

    def deathfall(self, cam):
        self.maxfallspeed = 7
        cam.lockMove = True
        if self.location[1] > cam.ypos+256:
            cam.lockMove = False
            self.respawn(cam)
        self.playAnimation("Death")
        self.speed[0] = 0

    def respawn(self, cam):
        self.mode = "alive"
        self.location[0] = self.respawnpoint[0]
        self.location[1] = self.respawnpoint[1]
        cam.refocus(self.location)

class NPC(Character):
    def __init__(self, ID, charName, xlocation, ylocation, arrayDestination, renderLayer, pallate, Level, Uniques):
        super().__init__(ID, charName, xlocation, ylocation, arrayDestination, renderLayer, pallate, Level, Uniques)
    """def update(self,cam):
        self.camera = cam
        self.render()"""
#class Item(Object):
#class Block(Object):

class Enemy(Character):
    def __init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques):
        Character.__init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level, Uniques)
        self.behaviorItr = 0
        self.interrupted = False
        self.behaviorTimer = 0
        #there should be a list of programmed behaviors for each enemy, with each entry comprising a behavior and an accompanying variable
        self.behaviors = (("Walk",60),("Wait", 45),("Flip","Null"),("Crouch",10),("Jump","Null"))

    def update(self, cam):
    #print(self.inhaled)
        self.camera = cam
        self.collideWithObj()
        self.interruptTest()
        self.collisionTests()
        self.behavior()
        self.submergedCheck()
        #pygame.draw.rect(self.renderLayer, (0,255,0), (self.location[0]+self.spriteSize[0]/2, self.location[1]+self.spriteSize[1],1,1))
        if self.attack == True or self.floating == True or self.submerged > 2:
            self.maxfallspeed = 2
        elif self.climb == True:
            self.maxfallspeed = 0
        else:
            self.maxfallspeed = 7
        if self.blockedTop == True:
            self.speed[1] = 2
        if self.grounded == False and self.interrupted == False:
            self.physicsSim()
            #top blocked only
        else:
            #print(self.fallingTime)
            self.fallingTime = 0
            self.speed[1] = 0
        Character.update(self,cam)
        ##print(self.location)

    def Kill(self):
        self.inhaled = False
        self.mouthed = None
        self.location[0] = 256
        self.location[1] = 36

    def physicsSim(self):
        if self.speed[1] < self.maxfallspeed:
            self.speed[1] += self.fallspeed
        else:
            self.speed[1] = self.maxfallspeed


    def interruptTest(self):
        for Object in self.objlist:
            if isinstance(Object, Player):
                if Object.attack == True:
                    if (self.left[1]-Object.right[1]) < 16 and (self.right[1]-Object.left[1]) > -16:
                        
                        if Object.dir == "right" and (self.left[0]-Object.right[0]) <= 40 and (self.right[0]-Object.right[0]) >= 0:
                            self.interrupted = True
                            self.inhaled = True
                            if self.StunItr != 10:
                                self.speed = [0,0]
                                self.StunItr += 1
                                
                        elif Object.dir == "left" and (Object.left[0]-self.right[0]) <= 40 and (Object.left[0]-self.left[0]) >= 0:
                            self.interrupted = True
                            self.inhaled = True
                            if self.StunItr != 10:
                                self.speed = [0,0]
                                self.StunItr += 1
                        else:
                            self.interrupted = False
                            self.inhaled = False
                    else:
                        self.interrupted = False
                        self.inhaled = False
                else:
                    self.interrupted = False
                    self.inhaled = False
                    self.StunItr = 0

    def behavior(self):
        #get the current behavior
        if self.interrupted == False:
            if self.behaviorItr >= len(self.behaviors):
                self.behaviorItr = 0
            getattr(self, self.behaviors[self.behaviorItr][0].lower())()
            #if the behavior has a timer:
                    #if an iterator derived from the timer > 0:
                            #increment the timer down
                            #execute the action
            #else if the behavior has a goal
                    #keep doing the thing until the goal is reached
        else:
            self.playAnimationOnce("Roll","Fall")

class Attack(Object):
    def __init__(self,ID,charName,
                 xlocation,ylocation,arrayDestination,
                 renderLayer,pallate,Level,Uniques):
        Object.__init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.lifespan = Uniques[0]
        moveinfo = Uniques[1]
        self.alligience = Uniques[2]
        self.mode = Uniques[3]
        try:
            self.destroyConditions = Uniques[4]
        except:
            self.destroyConditions = None
        self.angle = 0
        if self.mode == "line":
            self.xspeed = moveinfo[0]
            self.yspeed = moveinfo[1]
        elif self.mode == "circle":
            self.radx = moveinfo[0]
            self.rady = moveinfo[1]
            self.center = moveinfo[3]
            self.angle = moveinfo[4]
        elif self.mode == "parent":
            self.offsetx = moveinfo[0]
            self.offsety = moveinfo[1]
        self.movespeed = moveinfo[2]
        #self.persistant = persistant
    def update(self,mainCam):
        self.camera = mainCam
        #Object.update(self,mainCam)
        self.animate()
        self.getpoints()
        if self.destroyConditions != None:
            if getattr(self, self.destroyConditions)() == False:
                self.delete()
        if self.lifespan > 0:
            if self.mode.lower() == "circle":
                self.circleMove(self.center)
            elif self.mode.lower() == "line":
                self.lineMove()
            elif self.mode.lower() == "parent":
                self.parentMove()
            self.lifespan -= 1
            self.collideWithObj()
            self.hitCheck()
            self.render()
        else:
            self.delete()
    def arcMove(self,startPoint,apexPoint,endPoint):
        pass
    def parentMove(self):
        self.location[0] = self.alligience.location[0]+self.offsetx
        self.location[1] = self.alligience.location[1]+self.offsety
    def circleMove(self,center):
        ##print(self.speed)
        rotSpeed = 0.1
        if self.angle < 360:
            self.angle += rotSpeed*self.movespeed
        else:
            self.angle = 0
        self.location[0] = center[0] + (math.cos(self.angle))*self.radx
        self.location[1] = center[1] + (math.sin(self.angle))*self.rady
            
    def lineMove(self):
        self.playAnimation("Shoot")
        self.location[0] += self.xspeed
        self.location[1] += self.yspeed
        
    def hitCheck(self):
        for hitObj in self.collide:
            ##print(type(hitObj))
            if hitObj != None and type(hitObj) != type(self.alligience) and type(hitObj) != type(self):
                #print(type(self.alligience))
                try:
                    hitObj.Kill()
                except:
                    pass
                #print("Dip")
    def moveTo(self,x,y):
        self.location = (x,y)

class platform(Object):
    def __init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques):
        Object.__init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer,pallate,Level)
        #a boolean that determines whether or not the platform is started when the player lands on it
        self.activate = Uniques[0]
        #boolean that determines whether or not the platform is a semisolid
        self.semisolid = Uniques[1]
        #list of lists
            #each sub-list contains the type of movement (line or arc) and the duration of the movement
        self.movement = Uniques[2]
        #whether or not to destroy the platform when it's done it's thing
        self.destroy = Uniques[3]
        #type of platform
        self.type = Uniques[4]
        #size lol
        self.sizex = Uniques[5][0]
        self.sizey = Uniques[5][1]

        self.loop = 0
        self.movetimer = 0
        #self.speed = [0,-0.5]self.angle = 0
        
    def parentMove(self):
        self.speed[0] = self.location[0] - (self.alligience.location[0]+self.offsetx)
        self.speed[1] = self.location[1] - (self.alligience.location[1]+self.offsety)
        
    def circleMove(self,center):
        ##print(self.speed)
        rotSpeed = 0.1
        if self.angle < 360:
            self.angle += rotSpeed*self.movespeed
        else:
            self.angle = 0
        self.speed[0] = self.location[0] - (center[0] + (math.cos(self.angle))*self.radx)
        self.speed[1] = self.location[1] - (center[1] + (math.sin(self.angle))*self.rady)
            
    def lineMove(self):
        pass
        
    def update(self,mainCam):
        self.camera = mainCam
        self.collideWithObj()
        self.childMove()
        self.calcMove()
        self.move()
        self.getpoints()
        self.render()
        self.drawPoints()

    def childMove(self):
        print(self.collide)
        for obj in self.collide:
            if issubclass(type(obj),Character) and obj.location[1] <= self.top[1] and obj.grounded == True:
                if self.semisolid == False:
                    #print("ymid")
                    obj.location[0]+=self.speed[0]
                    obj.location[1]+=self.speed[1]
                else:
                    if obj.slideItr <= 0:
                        obj.location[0] += self.speed[0]


    def calcMove(self):
        #if activated == True
        if True:
            #get the list of movements
            #select the appropriate phase of movement
            mode = self.movement[self.loop][0]
            moveinfo = self.movement[self.loop][1]
            #if the last one was done
            if mode.lower() == "circle":
                self.radx = moveinfo[0]
                self.rady = moveinfo[1]
                self.center = moveinfo[3]
                self.angle = moveinfo[4]
                self.circleMove(self.center)
            elif mode.lower() == "line":
                self.speed[0] = moveinfo[0]
                self.speed[1] = moveinfo[1]
                self.lineMove()
            elif mode.lower() == "parent":
                self.offsetx = moveinfo[0]
                self.offsety = moveinfo[1]
                self.parentMove()
            self.movetimer += 1
            if self.movetimer >= self.movement[self.loop][2]:
                self.movetimer = 0
                self.loop += 1
            if self.loop >= len(self.movement):
                self.loop = 0

    def move(self):
        self.location[0] += self.speed[0]
        self.location[1] += self.speed[1]
            
    def getpoints(self):
        self.top = (int(self.location[0]+self.sizex/2), int(self.location[1]))
        self.bottom = (int(self.location[0]+self.sizex/2), int(self.location[1]+self.sizey)-1)
        self.right = (self.location[0]+self.sizex-1, self.location[1]+int(self.sizey/2)-1)
        self.left = (self.location[0], self.location[1]+int(self.sizey/2)-1)
        
    def render(self):
        self.sprite = pygame.transform.scale(self.sprite,(self.sizex,self.sizey))
        frame = Datafile["Character"]["Animations"]["Platform"][self.type][self.animFrameNumber]
        if frame[1] == self.animItr:
            self.animItr = 0
            self.animFrameNumber += 1
        else:
            self.animItr += 1
        if self.animFrameNumber > len(Datafile["Character"]["Animations"]["Platform"][self.type])-1:
            self.animFrameNumber = 0
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"]["Platform"][frame[0]]
        #make canvas for l-r edges
        edgesprite = pygame.Surface((8,self.sizey))
        #fill sprite with middle
        counter = 0
        while counter < self.sizey:
            counter2 = 0
            while counter2 < self.sizex:
                self.sprite.blit(Sheet, (counter2,counter),(self.spriteCoordinates[0]+8,self.spriteCoordinates[1]+8,8,8))
                counter2 += 8
            counter += 8
        #fill edge canvas with l-edge sprite
        counter = 0
        while counter < self.sizey:
            edgesprite.blit(Sheet, (0,counter),(self.spriteCoordinates[0],self.spriteCoordinates[1]+8,8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (0,8))
        #fill edge canvas with r-edge sprite
        counter = 0
        while counter < self.sizey:
            edgesprite.blit(Sheet, (0,counter),(self.spriteCoordinates[0]+16,self.spriteCoordinates[1]+8,8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (self.sizex-8,8))
        #make canvas for t-b edges
        edgesprite = pygame.transform.scale(edgesprite, ((self.sizex,8)))
        #fill edge canvas with t-edge sprite
        counter = 0
        while counter < self.sizex:
            edgesprite.blit(Sheet, (counter,0),(self.spriteCoordinates[0]+8,self.spriteCoordinates[1],8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (0,0))
        #fill edge canvas with b-edge sprite
        counter = 0
        while counter < self.sizex:
            edgesprite.blit(Sheet, (counter,0),(self.spriteCoordinates[0]+8,self.spriteCoordinates[1]+16,8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (0,self.sizey-8))
        #add corners to canvas
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],8,8))
        self.sprite.blit(Sheet, (self.sizex-8,0),(self.spriteCoordinates[0]+16,self.spriteCoordinates[1],8,8))
        self.sprite.blit(Sheet, (0,self.sizey-8),(self.spriteCoordinates[0],self.spriteCoordinates[1]+16,8,8))
        self.sprite.blit(Sheet, (self.sizex-8,self.sizey-8),(self.spriteCoordinates[0]+16,self.spriteCoordinates[1]+16,8,8))
        #add decorations
        #place door in level
        self.sprite = self.pallateApply(self.pallate,self.sprite)
        self.renderLayer.blit(self.sprite,
                              (self.location[0]-self.camera.xpos,
                               self.location[1]-self.camera.ypos),
                              (0,0,self.sizex,self.sizey))

class door(Object):
    def __init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques):
        Object.__init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer,pallate,Level)
        self.doortype = Uniques[0]
        self.sizex = Uniques[2][0]
        self.sizey = Uniques[2][1]
        self.dest = Uniques[1]
        self.func = Uniques[3]
    def update(self,mainCam):
        self.camera = mainCam
        self.getpoints()
        self.render()
        self.drawPoints()
    def interact(self,trigger):
        if self.func=="load":
            print(trigger.objlist)
            todelete = []
            for obj in trigger.objlist:
                if obj != trigger:
                    todelete.append(obj)
            for obj in todelete:
                obj.delete()
            print(trigger.objlist)
            trigger.currentLevel.__init__("Castle", "TestRoom1",trigger.objlist,trigger.renderLayer)
            trigger.currentLevel.loadLevel(trigger.renderLayer, trigger.camera)
            trigger.location[0] = self.dest[0]
            trigger.location[1] = self.dest[1]
        elif self.doortype=="warp":
            trigger.location[0] = self.dest[0]
            trigger.location[1] = self.dest[1]
    def getpoints(self):
        self.top = (int(self.location[0]+self.sizex/2), int(self.location[1]))
        self.bottom = (int(self.location[0]+self.sizex/2), int(self.location[1]+self.sizey)-1)
        self.right = (self.location[0]+self.sizex-1, self.location[1]+int(self.sizey/2)-1)
        self.left = (self.location[0], self.location[1]+int(self.sizey/2)-1)
        
    def render(self):
        self.sprite = pygame.transform.scale(self.sprite,(self.sizex,self.sizey))
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"]["Door"][self.doortype]
        #make canvas for l-r edges
        edgesprite = pygame.Surface((8,self.sizey))
        #fill sprite with middle
        counter = 0
        while counter < self.sizey:
            counter2 = 0
            while counter2 < self.sizex:
                self.sprite.blit(Sheet, (counter2,counter),(self.spriteCoordinates[0]+8,self.spriteCoordinates[1]+8,8,8))
                counter2 += 8
            counter += 8
        #fill edge canvas with l-edge sprite
        counter = 0
        while counter < self.sizey:
            edgesprite.blit(Sheet, (0,counter),(self.spriteCoordinates[0],self.spriteCoordinates[1]+8,8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (0,8))
        #fill edge canvas with r-edge sprite
        counter = 0
        while counter < self.sizey:
            edgesprite.blit(Sheet, (0,counter),(self.spriteCoordinates[0]+16,self.spriteCoordinates[1]+8,8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (self.sizex-8,8))
        #make canvas for t-b edges
        edgesprite = pygame.transform.scale(edgesprite, ((self.sizex,8)))
        #fill edge canvas with t-edge sprite
        counter = 0
        while counter < self.sizex:
            edgesprite.blit(Sheet, (counter,0),(self.spriteCoordinates[0]+8,self.spriteCoordinates[1],8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (0,0))
        #fill edge canvas with b-edge sprite
        counter = 0
        while counter < self.sizex:
            edgesprite.blit(Sheet, (counter,0),(self.spriteCoordinates[0]+8,self.spriteCoordinates[1]+16,8,8))
            counter += 8
        #add edge canvas to door canvas
        self.sprite.blit(edgesprite, (0,self.sizey-8))
        #add corners to canvas
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],8,8))
        self.sprite.blit(Sheet, (self.sizex-8,0),(self.spriteCoordinates[0]+16,self.spriteCoordinates[1],8,8))
        self.sprite.blit(Sheet, (0,self.sizey-8),(self.spriteCoordinates[0],self.spriteCoordinates[1]+16,8,8))
        self.sprite.blit(Sheet, (self.sizex-8,self.sizey-8),(self.spriteCoordinates[0]+16,self.spriteCoordinates[1]+16,8,8))
        #add decorations
        #place door in level
        self.sprite = self.pallateApply(self.pallate,self.sprite)
        self.renderLayer.blit(self.sprite,
                              (self.location[0]-self.camera.xpos,
                               self.location[1]-self.camera.ypos),
                              (0,0,self.sizex,self.sizey))

class Ball(Character):
    def __init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques):
        Character.__init__(self,ID,charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,Uniques)
        self.multiplayerMode = Uniques[0]
        self.speed = [-1,2]
        self.interrupted = False
        self.hit = False
        self.updateStateItr = 0

    def interruptTest(self):
        for Object in self.objlist:
            if isinstance(Object, Player):
                if Object.attack == True:
                    if (self.left[1]-Object.right[1]) < 24 and (self.right[1]-Object.left[1]) > -24:
                        
                        if Object.dir == "right" and (self.left[0]-Object.right[0]) <= 48 and (self.left[0]-Object.right[0]) >= 0:
                            self.interrupted = True
                            self.inhaled = True
                            if self.StunItr != 10:
                                self.speed[0] = 0
                                self.speed[1] = 0
                                self.StunItr += 1
                                
                        elif Object.dir == "left" and (Object.left[0]-self.right[0]) <= 48 and (Object.left[0]-self.right[0]) >= 0:
                            self.interrupted = True
                            self.inhaled = True
                            if self.StunItr != 10:
                                self.speed[0] = 0
                                self.speed[1] = 0
                                self.StunItr += 1
                        else:
                            self.interrupted = False
                            self.inhaled = False
                            self.StunItr = 0
                    else:
                        self.interrupted = False
                        self.inhaled = False
                        self.StunItr = 0
                """else:
                    self.interrupted = False
                    self.inhaled = False
                    self.StunItr = 0"""
        
    """def collisionTests(self):
        #self.interrupted = False
        #check self.bottom collision
        rdist = self.distanceToCollide(self.bottom,1,1)
        ldist = self.distanceToCollide(self.bottom,1,1)
        if ldist > rdist:
            self.bottom = self.bottom
        else:
            self.bottom = self.bottom
        if self.collisionCheck(self.bottom) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.bottom[0],self.bottom[1]-(itr)]) == True:
                    itr+= 1
                else:
                    self.location[1] -= itr-1
                    break
            self.grounded = True
        else:
            self.grounded = False
        #check top collision
        if self.collisionCheck(self.top) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.top[0],self.top[1]+(itr)]) == True:
                    itr+= 1
                else:
                    self.location[1] += itr-1
                    break
            self.blockedTop = True
        else:
            self.blockedTop = False
        #check left collision
        if self.collisionCheck(self.left) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.left[0]+(itr),self.left[1]]) == True:
                    itr+= 1
                else:
                    self.location[0] += itr-1
                    break
            self.blockedLeft = True
        else:
            self.blockedLeft = False
        #check right collision
        if self.collisionCheck(self.right) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.right[0]-(itr),self.right[1]]) == True:
                    itr+= 1
                else:
                    self.location[0] -= itr-1
                    break
            self.blockedRight = True
        else:
            self.blockedRight = False"""
            
    def hitCheck(self):
        for obj in self.collide:
            if obj != None:
                if obj.right[0] < self.right[0]:
                    self.speed[0] += 1
                elif obj.left[0] > self.left[0]:
                    self.speed[0] -= 1
                
                if obj.top[1] < self.top[1]:
                    self.speed[1] += 2
                elif self.bottom[1] > obj.bottom[1]:
                    self.speed[1] -= 2
    def Kill(self):
        print("dip")

    def update(self,mainCam):
        self.camera = mainCam
        self.render()
        self.animate()
        if self.mouthed == None:
            if self.location[0] > self.camera.xpos+255:
                pygame.draw.rect(self.renderLayer,(255,0,0),(255,self.top[1],1,16))
            elif self.location[0] < self.camera.xpos:
                pygame.draw.rect(self.renderLayer,(255,0,0),(0,self.top[1],1,16))
            self.getpoints()
            self.collisionTests()
            self.collideWithObj()
            self.interruptTest()
            self.hitCheck()
            self.move()
            ##print(self.blockedLeft)
            #self.speed = [0,0]
            if self.interrupted == False:
                self.updateStateItr = 0
                if self.grounded == True:
                    self.speed[1] = -2
                if self.blockedTop == True:
                    self.speed[1] = 2
                if self.blockedLeft == True:
                    self.speed[0] = 1
                if self.blockedRight == True:
                    self.speed[0] = -1
        else:
            self.multiplayerMode = self.mouthed.multiplayerMode
            self.grounded = False
            self.blockedLeft = False
            self.blockedTop = False
            self.blockedRight = False
            self.speed = [0,0]
            self.inhaled = False
            self.location[0] = self.mouthed.location[0]
            self.location[1] = self.mouthed.location[1]
        
        self.sendList = [self.crouching]
        if self.mouthed != None:
            self.sendList.append(self.objlist.index(self.mouthed))
        else:
            self.sendList.append(None)
        self.sendList.append(self.mouthfull)
        if self.inmouth != []:
            self.sendList.append(self.objlist.index(self.inmouth))
        else:
            self.sendList.append([])
        self.sendList.append(self.speed)
        self.sendList.append(self.location)
        self.sendList.append(self.lastkeys)
        self.sendList.append(self.ID)
        if self.multiplayerMode == "HOST":
            self.sendList.append(self.multiplayerMode)
        else:
            self.sendList.append("Derp")
            
    def respawn(self):
        self.blockedLeft = False
        self.blockedTop = False
        self.blockedRight = False
        self.grounded = True
        self.mouthed = None
        self.location[0] = 248
        self.location[1]= 100
        self.speed[0] = 0
        self.speed[1] = 2
        
    def ballchecks(self, data, connection):
        try:
            if data[8] == self.multiplayerMode:
                self.multiplayerMode = connection
                return True
        except:
            pass

class trigger(Object):
    def __init__(self, ID, charName, xlocation, ylocation,arrayDestination, renderLayer,pallate, Level):
        Object.__init__(self, ID, charName, xlocation, ylocation,arrayDestination, renderLayer,pallate, Level)
    def abilitychange(self,char,out):
        char.ability = out
        
    def lvlAlterRange(self,burner,lvlrange):
        #lvlrange should be list with format [xstart,ystart,xsize,ysize,factor to change, value to place in factor]
        for num in range(lvlrange[3]):
            data = getattr(self.currentLevel,lvlrange[4])
            for num2 in range(lvlrange[2]):
                value=num+lvlrange[1]
                data[value][num2+lvlrange[0]] = lvlrange[5]
        
class enterTrigger(trigger):
    def __init__(self, ID, charName, xlocation, ylocation,arrayDestination, renderLayer, Level, pallates, Uniques):
        trigger.__init__(self, ID, charName, xlocation, ylocation,arrayDestination, renderLayer, Level, pallates)
        self.targetType = Uniques[0]
        self.result = Uniques[1]
        self.value = Uniques[2]
        
    def getpoints(self):
        self.top = (int(self.location[0]+self.sizex/2), int(self.location[1]))
        self.right = (int(self.location[0]+self.sizex), int(self.location[1]+self.sizey/2))
        self.left = (int(self.location[0]), int(self.location[1]+self.sizey/2))
        self.bottom = (int(self.location[0]+self.sizex/2), int(self.location[1]+self.sizey))
        try:
            pygame.draw.rect(self.renderLayer,(255,0,0),(self.left[0]-self.camera.xpos,self.top[1]-self.camera.ypos,self.sizex,self.sizey))
        except:
            pass
        
    def update(self,mainCam):
        self.collisions = []
        self.camera = mainCam
        self.getpoints()
        for obj in self.objlist:
            if obj != self and type(obj).__name__:
                if (obj.left > self.left and self.right > obj.right) or (obj.left < self.left and self.right < obj.right):
                    if obj.top > self.top or self.bottom > obj.bottom:
                        self.collisions.append(obj)
                        
        for obj in self.collisions:
            if type(self.result) == list:
                for entry in range(len(self.value)):
                    func = getattr(self,self.value[entry])
                    if type(self.value) == list:
                        func(obj,self.result[entry])
                    else:
                        func(obj,self.value)
            else:
                func = getattr(self,self.result)
                func(obj,self.value)
class fluid(Object):
    def __init__(self, ID,charName, xlocation, ylocation, arrayDestination,renderLayer,pallate,Level,Uniques):
        self.ID = ID
        self.charName = charName
        #behavior type
        self.location = [xlocation, ylocation]
        self.dir = "right"
        self.pallateName = pallate
        self.sizex = Uniques[0]
        self.sizey = Uniques[1]
        self.currentLevel = Level
        self.animFrameNumber = 0
        self.animType = "Loop"
        self.animBacklog = "Body"
        self.animItr = 0
        self.animation = "Top"
        self.animFrame = "Top1"
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.sprite = pygame.Surface((self.sizex,self.sizey))
        self.renderLayer = renderLayer
        #add to array of all objects
        self.objlist = arrayDestination
        self.objlist.append(self)
        #self.getpoints()
        self.sendList = [self.location]
        self.sendList.append(self.ID)
        
    def delete(self):
        Object.delete(self)

    def checks(self,data):
        if data[0] != self.location:
            self.crouching = data[0]
        if data[1] != self.ID:
            self.mouthfull = data[1]

    def sendPop(self):
        self.sendList = [self.location]
        self.sendList.append(self.ID)
        
    def animate(self):
        self.animItr += 1
        if self.animItr == Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][1]:
            self.animFrameNumber += 1
            self.animItr = 0
        if self.animFrameNumber == len(Datafile["Character"]["Animations"][self.charName][self.animation]):
            if self.animType == "Loop":
                self.animFrameNumber = 0
                self.animItr = 0
            else:
                self.animType = "Loop"
                self.playAnimation(self.animBacklog)
                
    def getpoints(self):
        self.top = (int(self.location[0]+self.sizex/2), int(self.location[1]))
        self.right = (int(self.location[0]+self.sizex), int(self.location[1]+self.sizey/2))
        self.left = (int(self.location[0]), int(self.location[1]+self.sizey/2))
        self.bottom = (int(self.location[0]+self.sizex/2), int(self.location[1]+self.sizey))
        pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-self.camera.xpos,self.top[1]-self.camera.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-self.camera.xpos,self.bottom[1]-self.camera.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,216,255),(self.left[0]-self.camera.xpos,self.left[1]-self.camera.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-self.camera.xpos,self.right[1]-self.camera.ypos,1,1))
    def render(self):
        self.animFrame = Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][0]
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName][self.animFrame]
        #render new sprite with the wave animation at the top and basic blue tile as all others
        xitr = 0
        while xitr < self.sizex:
            #print("Dip")
            self.sprite.blit(Sheet, (xitr,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
            xitr += 8
        #time.sleep(5)
        xitr = 0
        yitr = 8
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName]["Body"]
        while yitr < self.sizey:
            xitr = 0
            while xitr < self.sizex:
                #print("Dip")
                self.sprite.blit(Sheet, (xitr,yitr),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
                xitr += 8
            yitr += 8
        
        self.renderLayer.blit(self.sprite, (self.location[0]-self.camera.xpos-int(self.spriteSize[0]/2),self.location[1]-self.camera.ypos-int(self.spriteSize[1]/2)), (0,0,self.sizex,self.sizey))
    def update(self,mainCam):
        #class Trigger(Object):
        self.camera = mainCam
        self.getpoints()
        self.animate()
        self.render()
