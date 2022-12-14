import json
import pygame
import time
import math
import abilityLib
import HostLib
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))

class Object:
    def __init__(self, ID, charName,ability, xlocation, ylocation, arrayDestination,renderLayer,pallate,Level):
        self.ID = ID
        self.lastkeys = pygame.key.get_pressed()
        self.charName = charName
        #behavior type
        self.alive = True
        self.inhaled = False
        self.mouthed = None
        self.inmouth = None
        self.inhalingnum = 0
        self.speed = [0,0]
        self.ability = ability
        self.location =[xlocation, ylocation]
        self.dir = "right"
        self.pallateName = pallate
        self.pallate = Datafile["Character"]["Pallates"][self.charName][pallate]
        self.fallSpeed = 7
        self.jumpHeight = 15
        self.grounded = False
        self.blockedTop = False
        self.blockedRight = False
        self.blockedLeft = False
        self.currentLevel = Level
        #current sprite
        if type(self).__name__== "Ball":
            self.animFrame = "Roll1"
            self.animation = "Idle"
        elif type(self).__name__ == "Attack":
            self.animFrame = "Shoot1"
            self.animation = "Shoot"
        else:
            self.animFrame = "Idle1"
            self.animation = "Idle"
        self.animFrameNumber = 0
        self.animType = "Loop"
        self.animBacklog = "Fall"
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.animItr = 0
        self.sprite = pygame.Surface((self.spriteSize[0],self.spriteSize[1]))
        self.StunItr = 0
        self.blockedTop = False
        self.floating = False
        self.flap = False
        self.crouching = False
        self.attack = False
        self.firePressed = False
        self.mouthfull = 0
        self.collide = []
        self.renderLayer = renderLayer
        #add to array of all objects
        self.objlist = arrayDestination
        self.objlist.append(self)
        self.getpoints()
        self.sendList = [self.crouching]
        if self.mouthed != None:
            self.sendList.append(self.objlist.index(self.mouthed))
        else:
            self.sendList.append(None)
        self.sendList.append(self.mouthfull)
        if self.inmouth != None:
            self.sendList.append(self.objlist.index(self.inmouth))
        else:
            self.sendList.append(None)
        self.sendList.append(self.speed)
        self.sendList.append(self.location)
        self.sendList.append(self.lastkeys)
        self.sendList.append(self.ID)
        #self.sendList = [self.crouching, self.objlist.index(self.mouthed),self.mouthfull,self.objlist.index(self.inmouth),self.speed,self.location,self.lastkeys]

    def delete(self):
        self.objlist.remove(self)

    def collideWithObj(self):
        self.collide = []
        for obj in self.objlist:
            if obj != self and obj != self.inmouth:
                #if top or bottom is between target body
                if (self.location[1] >= obj.location[1] and self.location[1] <= obj.location[1]+obj.spriteSize[1]) or (self.location[1]+self.spriteSize[1] >= obj.location[1] and self.location[1]+self.spriteSize[1] <= obj.location[1]+obj.spriteSize[1]):
                    ##print(f"{self.charName} {self.pallateName}: Y-intersect")
                    #if left or right is between target body
                    if (self.location[0] >= obj.location[0] and self.location[0] <= obj.location[0]+obj.spriteSize[0]) or (self.location[0]+self.spriteSize[0] >= obj.location[0] and self.location[0]+self.spriteSize[0] <= obj.location[0]+obj.spriteSize[0]):
                        ##print(f"{self.charName} {self.pallateName}: X-intersect")
                        ##print("COLLISION")
                        #return true
                        self.collide.append(obj)

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
        if data[3] != None:
            if self.inmouth != None:
                if data[3] != self.objlist.index(self.inmouth):
                    self.inmouth = self.objlist[data[3]]
                    #print("Mouth Contents Repair")
                elif data[3] != self.inmouth:
                    self.inmouth = self.objlist[data[3]]
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

    def getpoints(self):
        """self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.left = (int(self.location[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]+self.spriteSize[1]))"""
        self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]-self.spriteSize[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]-self.spriteSize[1]/2)-1)
        self.left = (int(self.location[0]), int(self.location[1]-self.spriteSize[1]/2)-1)
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))

    def update(self, cam):
        self.sendList = [self.crouching]
        if self.mouthed != None:
            self.sendList.append(self.objlist.index(self.mouthed))
        else:
            self.sendList.append(None)
        self.sendList.append(self.mouthfull)
        if self.inmouth != None:
            self.sendList.append(self.objlist.index(self.inmouth))
        else:
            self.sendList.append(None)
        self.sendList.append(self.speed)
        self.sendList.append(self.location)
        self.sendList.append(self.lastkeys)
        self.sendList.append(self.ID)
        
        self.getpoints()
        self.move()
        self.camera = cam
        self.animate()
        self.render()
        #if clicked
        pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-cam.xpos,self.top[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-cam.xpos,self.bottom[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,0,255),(self.left[0]-cam.xpos,self.left[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-cam.xpos,self.right[1]-cam.ypos,1,1))
        #if isinstance(self, Player):
            ##print(self.speed[0],self.speed[1])

    def render(self):
        #render sprite at location
        self.animFrame = Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][0]
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName][self.animFrame]
        ##print(f"{self.grounded}\b")
        try:
            spriteAlterx = self.spriteSize[0]-Datafile["Character"]["SpriteSize"]["Overrides"][self.charName][self.animFrame][0]
            spriteAltery = self.spriteSize[1]-Datafile["Character"]["SpriteSize"]["Overrides"][self.charName][self.animFrame][1]
            #self.location[1]+= spriteAltery
        except:
            spriteAlterx = 0
            spriteAltery = 0
        self.sprite = pygame.transform.scale(self.sprite,(self.spriteSize[0],self.spriteSize[1]))
        ##print(self.sprite.get_size())
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
        if len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) == 3:
             self.sprite.blit(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),(0,0))
        elif len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) == 4:
             self.sprite.blit(pygame.transform.flip(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),True,False),(0,0))
        self.sprite.blit(self.pallateApply(self.pallate, self.sprite),(0,0))
        if self.dir == "right":
            self.renderLayer.blit(self.sprite, (self.location[0]-self.camera.xpos,self.location[1]+spriteAltery-self.camera.ypos-self.spriteSize[1]), (0,0,self.spriteSize[0],self.spriteSize[1]))
        else:
            self.renderLayer.blit(pygame.transform.flip(self.sprite,1,0), (self.location[0]-self.camera.xpos,self.location[1]+spriteAltery-self.camera.ypos-self.spriteSize[1]), (0,0,self.spriteSize[0],self.spriteSize[1]))
        
    def pallateApply(self, pallate, sprite):
        #for each color in sprite:
        for color in range(len(pallate)):
            colorSprite = pygame.Surface(sprite.get_size())
            #replace with corrosponding pallate color
            colorSprite.fill(pallate[color])
            sprite.set_colorkey(Datafile["Character"]["Pallates"][self.charName]["Normal"][color])
            colorSprite.blit(sprite, (0,0))
            sprite.blit(colorSprite, (0,0))
        return sprite

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

    def distanceToCollide(self,point,searchAxis,searchDirection):
        itr = 0
        if searchAxis == 0:
            while True:
                if isinstance(self, Player):
                    pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]+itr-self.camera.xpos,self.top[1]-self.camera.ypos,1,1))
                    pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]+itr-self.camera.xpos,self.bottom[1]-self.camera.ypos,1,1))
                    pygame.draw.rect(self.renderLayer,(0,0,255),(self.left[0]+itr-self.camera.xpos,self.left[1]-self.camera.ypos,1,1))
                    pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]+itr-self.camera.xpos,self.right[1]-self.camera.ypos,1,1))
                if self.collisionCheck((point[searchAxis]+itr,point[1])):   
                    break
                itr += 1*searchDirection
        else:
            while True:
                if isinstance(self, Player):
                    pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-self.camera.xpos,self.top[1]-self.camera.ypos+itr,1,1))
                    pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-self.camera.xpos,self.bottom[1]-self.camera.ypos+itr,1,1))
                    pygame.draw.rect(self.renderLayer,(0,0,255),(self.left[0]-self.camera.xpos,self.left[1]-self.camera.ypos+itr,1,1))
                    pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-self.camera.xpos,self.right[1]-self.camera.ypos+itr,1,1))
                if self.collisionCheck((point[0],point[searchAxis]+itr)):   
                    break
                itr += 1*searchDirection
        return itr
    
    def move(self):
        if self.alive == True:
            #if isinstance(self, Player):
                ##print(self.speed[0])
            if self.collisionCheck((self.right[0]+self.speed[0],self.right[1]+int(self.speed[1]/2))) == True:
                if self.collisionCheck((self.right[0]+self.speed[0],self.right[1])) == False:
                    self.location[0] += self.speed[0]
                else:
                    self.location[0] += self.distanceToCollide(self.right, 0, 1)
                    
            elif self.collisionCheck((self.left[0]+self.speed[0],self.left[1]+int(self.speed[1]/2))) == True:
                if self.collisionCheck((self.left[0]+self.speed[0],self.left[1])) == False:
                    self.location[0] += self.speed[0]
                else:
                    self.location[0] += self.distanceToCollide(self.left, 0, -1)
            else:
                self.location[0] += self.speed[0]
            self.getpoints()
            if self.collisionCheck((self.top[0]+self.speed[0],self.top[1]+int(self.speed[1]/2))) == True:
                if self.collisionCheck((self.top[0],self.top[1]+int(self.speed[1]/2))) == False:
                    self.location[1] += int(self.speed[1]/2)
                else:
                    self.location[1] += self.distanceToCollide(self.top, 1, -1)
            elif self.collisionCheck((self.bottom[0]+self.speed[0],self.bottom[1]+int(self.speed[1]/2))) == True:
                if self.collisionCheck((self.bottom[0],self.bottom[1]+int(self.speed[1]/2))) == False:
                    self.location[1] += int(self.speed[1]/2)
                else:
                    self.location[1] += self.distanceToCollide(self.bottom, 1, 1)
            else:
                self.location[1] += int(self.speed[1]/2)
            self.getpoints()
        else:
            self.location[0] += self.speed[0]
            self.location[1] += int(self.speed[1]/2)
    
    def collisionCheck(self, point):
        ##print(f"{self.charName} {self.pallateName} is testing collision")
        try:
            #check all four points on character.
            #find what tile type they are on
            tilecountx = (point[0]//8)
            ##print(f"{self.charName} {self.pallateName} has it's x test")
            tilecounty = (point[1]//8)
            ##print(f"{self.charName} {self.pallateName} has it's y test")
            ##print(tilecountx,tilecounty)
            tilenum = str(self.currentLevel.collisionData[tilecounty][tilecountx])
            ##print(f"{self.charName} {self.pallateName} has it's tile")
            tiletype = (Datafile["Tilekey"][tilenum])
            ##print(f"{self.charName} {self.pallateName} has it's tiletype")
            ##print(tiletype)
            if tiletype != "Air":
                if self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 1:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][8-point[0]%8][point[1]%8] == 1:
                        ##print(f"{self.charName} {self.pallateName} is reigestering collision with an x-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                elif self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 2:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8][8-point[1]%8] == 1:
                        ##print(f"{self.charName} {self.pallateName} is reigestering collision with a y-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                elif self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 3:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][8-point[0]%8][8-point[1]%8] == 1:
                        ##print(f"{self.charName} {self.pallateName} is reigestering collision with a dual-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                else:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8][point[1]%8] == 1:
                        ##print(f"{self.charName} {self.pallateName} is reigestering collision with a non-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
            else:
                return False
        except:
            return True
            ##print(f"{self.charName} {self.pallateName} is reigestering collision")
        
    def walk(self):
        if self.floating == False:
            if self.mouthfull == 0:
                self.playAnimation("Walk")
            else:
                self.playAnimation("FullWalk")
        if self.dir == "right":
            if self.blockedRight == False:
                self.speed[0] = 2
        elif self.dir == "left":
            if self.blockedLeft == False:
                self.speed[0] = -2
        try:
            self.behaviorTimer += 1
            if self.behaviorTimer >= self.behaviors[self.behaviorItr][1]:
                self.behaviorTimer = 0
                self.behaviorItr += 1
        except:
            pass


    def crouch(self):
        self.speed[0] = 0
        self.crouching = True
        #if isinstance(self, Player):
            ##print(Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])])
        if Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])] == "Floor45":
            if self.currentLevel.file["FlipMap"][self.bottom[1]//8][self.bottom[0]//8] == 0:
                if self.dir == "right":
                    self.playAnimation("Crouch45")
                else:
                    self.playAnimation("Crouch135")
            elif self.currentLevel.file["FlipMap"][self.bottom[1]//8][self.bottom[0]//8] == 1:
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
        self.speed[0] = 0
        if self.crouching == False:
            #if isinstance(self, Player):
                ##print(Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])])
            if Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])] == "Floor45":
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
                self.playAnimation("Jump")
                self.location[1] -= 2
                self.grounded = False
                self.speed[1] = -(self.jumpHeight)
        try:
            self.behaviorTimer = 0
            self.behaviorItr += 1
            self.flap = False
            self.fallSpeed = 7
        except:
            pass
    def float(self):
        if self.flap == False and self.attack == False and self.mouthfull == 0:
            self.flap = True
            self.flap = True
            if self.floating == False:
                self.floating = True
                self.playAnimationOnce("Inflate", "Float")
            else:
                self.playAnimationOnce("Flap","Float")
            self.speed[1] = -self.jumpHeight/2
        try:
            self.fallSpeed = 2
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

class Player(Object):
    def __init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,multiplayerMode):
        Object.__init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.alive = True
        self.attack = False
        self.attack = False
        self.startInhale = False
        self.multiplayerMode = multiplayerMode
        self.respawnpoint = (xlocation,ylocation)

    def update(self,cam):
        Object.update(self,cam)
        if(self.alive == True):
            self.playerScript()
            ##print(self.location)
        else:
            self.deathfall(cam)
            self.animate()
            self.physicsSim()

    def playerScript(self):
        self.collisionTest()
        self.collideWithObj()
        #run physics sim
        if self.grounded == False:
            self.physicsSim()
        else:
            self.floating = False
            self.speed[1] = 0
        #grounded and ungrounded
        #check for input
        if self.multiplayerMode == "HOST":
            keys = pygame.key.get_pressed()
            self.lastkeys = keys
        else:
            keys = self.lastkeys
        if keys[pygame.K_i]:
            self.Kill()
        if keys[pygame.K_d]:
            abilityLib.Copy(self)
            """if self.startInhale ==False:
                if self.mouthfull == False:
                    self.floating = False
                    if self.attack== False:
                        self.playAnimationOnce("InhaleStart","Inhale")
                    else:
                        self.playAnimation("Inhale")
                    self.attack = True
                else:
                    self.playAnimation("Full")
                    if self.attack == False:
                        self.mouthfull = False
                        self.startInhale = True"""
        else:
            self.attack = False
            self.firePressed = False
                    
        if keys[pygame.K_LEFT] and self.attack == False:
            self.dir = "left"
            #if not blocked on left side
            """if self.blockedLeft == False:
                self.speed[0] = -1"""
            self.walk()
        elif keys[pygame.K_RIGHT] and self.attack == False:
            self.dir = "right"
            """if self.blockedRight == False:
                self.speed[0] = 1"""
            self.walk()
        else:
            self.speed[0] = 0
        #grounded only
        ##print(self.speed[1])
        ##print(self.flap)
        ##print(self.animation)
        if self.grounded == True:
            if keys[pygame.K_DOWN]:
                if self.mouthfull == 0:
                    self.crouch()
                else:
                    self.playAnimationOnce("Swallow","Crouch")
                    self.mouthfull = 0
                    try:
                        self.inmouth.respawn()
                    except:
                        pass
                    self.inmouth = None
            else:
                self.crouching = False
            self.floating = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                if self.attack == False:
                    if self.mouthfull == 0:
                        self.playAnimation("Walk")
                    else:
                        self.playAnimation("FullWalk")
            else:
                if self.attack == False:
                    if self.mouthfull == 0:
##                        if self.crouching == False:
##                            self.playAnimation("Idle")
##                        else:
##                            self.playAnimation("Crouch")
                        self.wait()
                    else:
                        self.playAnimation("Full")
            if keys[pygame.K_SPACE]:
                    """self.grounded = False
                    if self.mouthfull == False:
                        self.playAnimation("Jump")
                    else:
                        self.playAnimation("FullJump")
                    self.speed[1] = -(self.jumpHeight)"""
                    self.jump()
            else:
                self.flap = False
        #ungrounded only
        elif self.grounded == False:
            if self.speed[1] == 0:
                if self.animation == "Fall":
                    pass
                elif self.attack== True:
                    self.playAnimation("Inhale")
                else:
                    if self.mouthfull == 0:
                        self.playAnimationOnce("Roll","Fall")
                    else:
                        self.playAnimation("FullJump")
            if self.speed[1] > 0:
                if self.floating == False:
                    if self.mouthfull == 0:
                        self.playAnimation("Fall")
                        if self.attack== True:
                            self.playAnimation("Inhale")
                    else:
                        self.playAnimation("FullJump")
                elif self.attack== True:
                    self.playAnimation("Inhale")
                else:
                    self.playAnimation("Float")
            else:
                if self.floating == False:
                    if self.mouthfull == 0:
                        self.playAnimation("Jump")
                    elif self.attack== True:
                        self.playAnimation("Inhale")
                    else:
                        self.playAnimation("FullJump")
            if keys[pygame.K_SPACE]:
                self.float()
            else:
                self.flap = False
        
        #code for death and inhale
        if self.attack == True or self.floating == True:
            self.fallSpeed = 2
        else:
            self.fallSpeed = 7
        for obj in self.collide:
            if isinstance(obj, Enemy):
                if obj.inhaled == False:
                    self.Kill()
                """if self.dir == "right" and collide.right[0] > self.right[0]:
                    self.mouthfull = True
                    collide.Kill()
                elif self.dir == "left" and collide.left[0] < self.left[0]:
                    self.mouthfull = True
                    collide.Kill()
                else:
                    self.Kill()
            else:
                self.Kill()
        elif collide != None:
            collide.playAnimationOnce("Death","Idle")"""
                
        #top blocked only
        if self.blockedTop == True:
            self.speed[1] = 2

    def collisionTest(self):
        #check for collisions
        if self.collisionCheck(self.bottom) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.bottom[0],self.bottom[1]-(itr)]) == True:
                    itr+= 1
                else:
                    self.location[1] -= itr-1
                    break
            self.grounded = True
            self.getpoints()
        elif self.collisionCheck((self.bottom[0], self.bottom[1]+1)) == True:
            self.location[1] += 1
            self.grounded = True
            self.getpoints()
        else:
            self.grounded = False

        if self.collisionCheck(self.top) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.top[0],self.top[1]+(itr)]) == True:
                    itr+= 1
                else:
                    self.location[1] += itr
                    break
            self.blockedTop = True
            self.getpoints()
        else:
            self.blockedTop = False
            
        if self.collisionCheck(self.left) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.left[0]+itr,self.left[1]]) == True:
                    itr += 1
                else:
                    self.location[0] += itr-1
                    break
            self.blockedLeft = True
            self.getpoints()
        else:
            self.blockedLeft = False
            
        if self.collisionCheck(self.right) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.right[0]-itr,self.right[1]]) == True:
                    itr += 1
                else:
                    self.location[0] -= itr-1
                    break
            self.blockedRight = True
            self.getpoints()
        else:
            self.blockedRight = False

    def physicsSim(self):
        if self.speed[1] < self.fallSpeed:
            self.speed[1] += 1
        else:
            self.speed[1] = self.fallSpeed

    def Kill(self):
        if self.alive == True:
            #print("Player Death")
            self.alive = False
            self.floating = False
            self.mouthfull = 0
            self.attack = False
            self.grounded = False
            time.sleep(1)
            self.speed[1] = -15
            self.fallSpeed = 7

    def deathfall(self, cam):
        self.fallSpeed = 7
        cam.lockMove = True
        if self.location[1] > cam.ypos+256:
            cam.lockMove = False
            self.respawn(cam)
        self.playAnimation("Death")
        self.speed[0] = 0

    def respawn(self, cam):
        self.alive = True
        self.location[0] = self.respawnpoint[0]
        self.location[1] = self.respawnpoint[1]
        cam.refocus(self.location)

class NPC(Object):
    pass
#class Item(Object):
#class Block(Object):

class Enemy(Object):
    def __init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level):
        Object.__init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.behaviorItr = 0
        self.interrupted = False
        self.behaviorTimer = 0
        #there should be a list of programmed behaviors for each enemy, with each entry comprising a behavior and an accompanying variable
        self.behaviors = (("Walk",60),("Wait", 45),("Flip","Null"),("Crouch",10),("Jump","Null"))

    def update(self, cam):
        self.interruptTest()
        self.collisionTests()
        self.behavior()
        #pygame.draw.rect(self.renderLayer, (0,255,0), (self.location[0]+self.spriteSize[0]/2, self.location[1]+self.spriteSize[1],1,1))
        if self.blockedTop == True:
            self.speed[1] = 2
        if self.grounded == False:
            self.physicsSim()
            #top blocked only
        else:
            self.speed[1] = 0
        Object.update(self,cam)
        ##print(self.location)

    def Kill(self):
        self.location[0] = 256
        self.location[1] = 36

    def physicsSim(self):
        if self.speed[1] < self.fallSpeed:
            self.speed[1] += 1
        else:
            self.speed[1] = self.fallSpeed

    def collisionTests(self):
        """self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.left = (int(self.location[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]+self.spriteSize[1]))"""
        self.getpoints()
        #self.interrupted = False
        #check bottom collision
        if self.collisionCheck(self.bottom) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.bottom[0],self.bottom[1]-(itr)]) == True:
                    itr+= 1
                else:
                    self.location[1] -= itr-1
                    break
            self.grounded = True
        elif self.collisionCheck([self.bottom[0], self.bottom[1]+1]) == True:
            self.location[1] += 1
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
            self.blockedRight = False

    def interruptTest(self):
        for Object in self.objlist:
            if isinstance(Object, Player):
                if Object.attack == True:
                    if (self.left[1]-Object.right[1]) < 16 and (self.right[1]-Object.left[1]) > -16:
                        
                        if Object.dir == "right" and (self.left[0]-Object.right[0]) <= 40 and (self.left[0]-Object.right[0]) >= 0:
                            self.interrupted = True
                            self.inhaled = True
                            if self.StunItr != 10:
                                self.speed[0] = 0
                                self.speed[1] = 0
                                self.StunItr += 1
                                
                        elif Object.dir == "left" and (Object.left[0]-self.right[0]) <= 40 and (Object.left[0]-self.right[0]) >= 0:
                            self.interrupted = True
                            self.inhaled = True
                            if self.StunItr != 10:
                                self.speed[0] = 0
                                self.speed[1] = 0
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
            if self.behaviorItr >=len(self.behaviors):
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
    def __init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer,pallate,Level,lifespan,moveinfo,alligience,mode):
        Object.__init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.lifespan = lifespan
        self.alligience = alligience
        self.mode = mode
        if self.mode == "line":
            self.xspeed = moveinfo[0]
            self.yspeed = moveinfo[1]
        elif self.mode == "circle":
            self.radx = moveinfo[0]
            self.radx = moveinfo[1]
        self.movespeed = moveinfo[2]
        #self.persistant = persistant
        self.angle = 0
    def update(self,mainCam):
        self.camera = mainCam
        #Object.update(self,mainCam)
        self.animate()
        self.getpoints()
        if self.lifespan > 0:
            if self.mode.lower() == "circle":
                self.circleMove((150,100))
            elif self.mode.lower() == "line":
                self.lineMove()
            self.lifespan -= 1
            self.collideWithObj()
            self.hitCheck()
            self.render()
        else:
            self.delete()
    def arcMove(self,startPoint,apexPoint,endPoint):
        pass
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
                hitObj.Kill()
                #print("Dip")
    def moveTo(self,x,y):
        self.location = (x,y)


class Ball(Object):
    def __init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level,multiplayerMode):
        Object.__init__(self,ID,charName,ability, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.multiplayerMode = multiplayerMode
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
                else:
                    self.interrupted = False
                    self.inhaled = False
                    self.StunItr = 0
        
    def collisionTests(self):
        #self.interrupted = False
        #check bottom collision
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
            self.blockedRight = False
            
    def hitCheck(self):
        for obj in self.collide:
            if obj != None:
                if obj.right[0] < self.right[0]:
                    self.speed[0] += 1
                elif obj.left[0] > self.left[0]:
                    self.speed[0] -= 1
                if obj.top[1] < self.top[1]:
                    self.speed[1] += 2
                elif obj.bottom[1] > self.bottom[1]:
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
            #self.speed == [0,0]
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
        if self.inmouth != None:
            self.sendList.append(self.objlist.index(self.inmouth))
        else:
            self.sendList.append(None)
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
            
        #class Trigger(Object):
