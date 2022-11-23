import json
import pygame
import time
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))

class Object:
    def __init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level):
        self.charName = charName
        #behavior type
        self.speed = [0,0]
        self.location =[xlocation, ylocation]
        self.dir = "right"
        self.pallateName = pallate
        self.pallate = Datafile["Character"]["Pallates"][self.charName][pallate]
        self.fallSpeed = 7
        self.jumpHeight = 15
        self.grounded = False
        self.currentLevel = Level
        #current sprite
        self.animFrame = "Idle1"
        self.animFrameNumber = 0
        self.animation = "Idle"
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
        self.mouthfull = False
        self.renderLayer = renderLayer
        #add to array of all objects
        (arrayDestination).append(self)
        self.objlist = arrayDestination

    def collideWithObj(self):
        for object in self.objlist:
            if object != self:
                #if top or bottom is between target body
                if (self.location[1] >= object.location[1] and self.location[1] <= object.location[1]+object.spriteSize[1]) or (self.location[1]+self.spriteSize[1] >= object.location[1] and self.location[1]+self.spriteSize[1] <= object.location[1]+object.spriteSize[1]):
                    #print(f"{self.charName} {self.pallateName}: Y-intersect")
                    #if left or right is between target body
                    if (self.location[0] >= object.location[0] and self.location[0] <= object.location[0]+object.spriteSize[0]) or (self.location[0]+self.spriteSize[0] >= object.location[0] and self.location[0]+self.spriteSize[0] <= object.location[0]+object.spriteSize[0]):
                        #print(f"{self.charName} {self.pallateName}: X-intersect")
                        #print("COLLISION")
                        #return true
                        return object

    def update(self, cam):
        """self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.left = (int(self.location[0]), int(self.location[1]+self.spriteSize[1]/2))
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]+self.spriteSize[1]))"""
        self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]-self.spriteSize[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]-self.spriteSize[1]/2)-1)
        self.left = (int(self.location[0]), int(self.location[1]-self.spriteSize[1]/2)-2)
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))
        self.move()
        self.camera = cam
        self.animate()
        #if clicked
        #render sprite at location
        self.animFrame = Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][0]
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName][self.animFrame]
        #print(f"{self.grounded}\b")
        try:
            spriteAlterx = self.spriteSize[0]-Datafile["Character"]["SpriteSize"]["Overrides"][self.charName][self.animFrame][0]
            spriteAltery = self.spriteSize[1]-Datafile["Character"]["SpriteSize"]["Overrides"][self.charName][self.animFrame][1]
            #self.location[1]+= spriteAltery
        except:
            spriteAlterx = 0
            spriteAltery = 0
        self.sprite = pygame.transform.scale(self.sprite,(self.spriteSize[0],self.spriteSize[1]))
        #print(self.sprite.get_size())
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
        if len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) == 3:
             self.sprite.blit(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),(0,0))
        elif len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) == 4:
             self.sprite.blit(pygame.transform.flip(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),True,False),(0,0))
        self.sprite.blit(self.pallateApply(self.pallate, self.sprite),(0,0))
        if self.dir == "right":
            self.renderLayer.blit(self.sprite, (self.location[0]-cam.xpos,self.location[1]+spriteAltery-cam.ypos-self.spriteSize[1]), (0,0,self.spriteSize[0],self.spriteSize[1]))
        else:
            self.renderLayer.blit(pygame.transform.flip(self.sprite,1,0), (self.location[0]-cam.xpos,self.location[1]+spriteAltery-cam.ypos-self.spriteSize[1]), (0,0,self.spriteSize[0],self.spriteSize[1]))
        pygame.draw.rect(self.renderLayer,(255,0,0),(self.top[0]-cam.xpos,self.top[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(255,255,0),(self.bottom[0]-cam.xpos,self.bottom[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,0,255),(self.left[0]-cam.xpos,self.left[1]-cam.ypos,1,1))
        pygame.draw.rect(self.renderLayer,(0,255,0),(self.right[0]-cam.xpos,self.right[1]-cam.ypos,1,1))
        #if isinstance(self, Player):
            #print(self.blockedTop, self.grounded,self.speed[1])

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
    
    def move(self):
        self.location[0] += self.speed[0]
        self.location[1] = int(self.location[1] + self.speed[1]/2)
    
    def collisionCheck(self, point):
        #print(f"{self.charName} {self.pallateName} is testing collision")
        try:
            #check all four points on character.
            #find what tile type they are on
            tilecountx = (point[0]//8)
            #print(f"{self.charName} {self.pallateName} has it's x test")
            tilecounty = (point[1]//8)
            #print(f"{self.charName} {self.pallateName} has it's y test")
            #print(tilecountx,tilecounty)
            tilenum = str(self.currentLevel.collisionData[tilecounty][tilecountx])
            #print(f"{self.charName} {self.pallateName} has it's tile")
            tiletype = (Datafile["Tilekey"][tilenum])
            #print(f"{self.charName} {self.pallateName} has it's tiletype")
            #print(tiletype)
            if tiletype != "Air":
                if self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 1:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][8-point[0]%8][point[1]%8] == 1:
                        #print(f"{self.charName} {self.pallateName} is reigestering collision with an x-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                elif self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 2:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8][8-point[1]%8] == 1:
                        #print(f"{self.charName} {self.pallateName} is reigestering collision with a y-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                elif self.currentLevel.file["FlipMap"][tilecounty][tilecountx] == 3:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][8-point[0]%8][8-point[1]%8] == 1:
                        #print(f"{self.charName} {self.pallateName} is reigestering collision with a dual-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
                else:
                    if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8][point[1]%8] == 1:
                        #print(f"{self.charName} {self.pallateName} is reigestering collision with a non-flipped block: type {tiletype}")
                        return True
                    else:
                        return False
            else:
                return False
        except:
            return True
            #print(f"{self.charName} {self.pallateName} is reigestering collision")
        
    def walk(self):
        if self.floating == False:
            if self.mouthfull == False:
                self.playAnimation("Walk")
            else:
                self.playAnimation("FullWalk")
        if self.dir == "right":
            if self.blockedRight == False:
                self.speed[0] = 1
        elif self.dir == "left":
            if self.blockedLeft == False:
                self.speed[0] = -1
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
            #print(Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])])
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
                #print(Datafile["CollisionKey"][str(self.currentLevel.collisionData[self.bottom[1]//8][self.bottom[0]//8])])
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
            self.flap = True
            self.location[1] -= 5
            self.grounded = False
            self.playAnimation("Jump")
            self.speed[1] = -(self.jumpHeight)
        try:
            self.behaviorTimer = 0
            self.behaviorItr += 1
            self.flap = False
            self.fallSpeed = 7
        except:
            pass
    def float(self):
        if self.flap == False and self.attack == False and self.mouthfull == False:
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
    def __init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level):
        Object.__init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.alive = True
        self.mouthfull = False
        self.attack = False
        self.respawnpoint = (xlocation,ylocation)

    def update(self,cam):
        Object.update(self,cam)
        if(self.alive == True):
            self.playerScript()
        else:
            self.deathfall(cam)
            self.animate()
            self.physicsSim()

    def playerScript(self):
        self.collisionTest()
        collide = self.collideWithObj()
        #code for death and inhale
        if self.attack == True or self.floating == True:
            self.fallSpeed = 2
        else:
            self.fallSpeed = 7
        if isinstance(collide, Enemy):
            if self.attack == True:
                if self.dir == "right" and collide.right[0] > self.right[0]:
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
            collide.playAnimationOnce("Death","Idle")
        #run physics sim
        if self.grounded == False:
            self.physicsSim()
        else:
            self.floating = False
            self.speed[1] = 0
        #grounded and ungrounded
        if self.attack == True:
            for enemy in self.objlist:
                if enemy != self:
                    if isinstance(enemy, Enemy):
                        if self.dir == "right" and (enemy.location[0]-self.right[0]) <= 40 and (enemy.location[0]-self.right[0]) > 0:
                            if (self.top[1]-enemy.location[1]) <= 16 and (self.bottom[1]-enemy.location[1]) > -16:
                                #print(f"RIGHT: Suck in {enemy.pallateName}")
                                if enemy.left[1] > self.right[1]:
                                    #enemy.location[1] += (enemy.location[1] - self.bottom[1])/5
                                    enemy.speed[1] -= 1
                                elif enemy.left[1] < self.right[1]:
                                    #enemy.location[1] -= (enemy.location[1] - self.bottom[1])/5
                                    enemy.speed[1] += 1
                                else:
                                    enemy.speed[1] = 0
                                if enemy.left[0] > self.right[0]:
                                    #enemy.location[0] -= (enemy.location[0] - self.right[0])/5
                                    enemy.speed[0] -= 1
                                    
                        elif self.dir == "left" and (self.left[0]-enemy.right[0]) <= 40 and (self.left[0]-enemy.right[0]) > 0:
                            if (self.top[1]-enemy.location[1]) <= 16 and (self.bottom[1]-enemy.location[1]) > -16:
                                #print(f"LEFT: Suck in {enemy.pallateName}")
                                if enemy.right[1] > self.left[1]:
                                    #enemy.location[1] += (enemy.location[1] - self.bottom[1])/5
                                    enemy.speed[1] -= 1
                                elif enemy.right[1] < self.left[1]:
                                    #enemy.location[1] -= (enemy.location[1] - self.bottom[1])/5
                                    enemy.speed[1] += 1
                                else:
                                    enemy.speed[1] = 0
                                if enemy.right[0] < self.left[0]:
                                    #enemy.location[0] -= (enemy.location[0] - self.right[0])/5
                                    enemy.speed[0] += 1
        #check for input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_i]:
            self.Kill()
        if keys[pygame.K_d]:
            if self.startInhale ==False:
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
                        self.startInhale = True
        else:
            self.attack = False
            self.startInhale = False
                    
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
        #print(self.speed[1])
        #print(self.flap)
        #print(self.animation)
        if self.grounded == True:
            if keys[pygame.K_DOWN]:
                if self.mouthfull == False:
                    self.crouch()
                else:
                    self.mouthfull = False
                    self.playAnimationOnce("Swallow","Crouch")
            else:
                self.crouching = False
            self.floating = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                if self.attack == False:
                    if self.mouthfull == False:
                        self.playAnimation("Walk")
                    else:
                        self.playAnimation("FullWalk")
            else:
                if self.attack == False:
                    if self.mouthfull == False:
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
                    if self.mouthfull == False:
                        self.playAnimationOnce("Roll","Fall")
                    else:
                        self.playAnimation("FullJump")
            if self.speed[1] > 0:
                if self.floating == False:
                    if self.mouthfull == False:
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
                    if self.mouthfull == False:
                        self.playAnimation("Jump")
                    elif self.attack== True:
                        self.playAnimation("Inhale")
                    else:
                        self.playAnimation("FullJump")
            if keys[pygame.K_SPACE]:
                self.float()
            else:
                self.flap = False

        #top blocked only
        if self.blockedTop == True:
            self.speed[1] = 2

    def collisionTest(self):
        #check for collisions
        if self.collisionCheck(self.bottom) == True:
            itr = 0
            while True:
                if self.collisionCheck([self.bottom[0],self.bottom[1]-(itr)]) == True:
                    itr+= 1
                else:
                    self.location[1] -= itr-1
                    break
            self.grounded = True
        elif self.collisionCheck((self.bottom[0], self.bottom[1]+1)) == True:
            self.location[1] += 1
            self.grounded = True
        else:
            self.grounded = False

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
            
        if self.collisionCheck(self.left) == True:
            itr = 1
            while True:
                if self.collisionCheck([self.left[0]+itr,self.left[1]]) == True:
                    itr += 1
                else:
                    self.location[0] += itr-1
                    break
            self.blockedLeft = True
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
        else:
            self.blockedRight = False

    def physicsSim(self):
        if self.speed[1] < self.fallSpeed:
            self.speed[1] += 1
        else:
            self.speed[1] = self.fallSpeed

    def Kill(self):
        if self.alive == True:
            print("Player Death")
            self.alive = False
            self.floating = False
            self.mouthfull = False
            self.attack = False
            self.grounded = False
            time.sleep(1)
            self.speed[1] = -15
            self.fallSpeed = 7

    def deathfall(self, cam):
        self.fallSpeed = 7
        if self.location[1] > cam.ypos+256:
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
    def __init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level):
        Object.__init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
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
        #print(self.location)

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
        self.top = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]-self.spriteSize[1]))
        self.right = (int(self.location[0]+self.spriteSize[0]), int(self.location[1]-self.spriteSize[1]/2))
        self.left = (int(self.location[0]), int(self.location[1]-self.spriteSize[1]/2))
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]))
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
                    if (self.right[1]-Object.right[1]) < 16 and (self.right[1]-Object.right[1]) > -16:
                        
                        if Object.dir == "right" and (self.left[0]-Object.right[0]) <= 40 and (self.left[0]-Object.right[0]) >= 0:
                            self.interrupted = True
                            if self.StunItr != 10:
                                self.speed[0] = 0
                                self.speed[1] = 0
                                self.StunItr += 1
                                
                        elif Object.dir == "left" and (Object.left[0]-self.right[0]) <= 40 and (Object.left[0]-self.right[0]) >= 0:
                            self.interrupted = True
                            if self.StunItr != 10:
                                self.speed[0] = 0
                                self.speed[1] = 0
                                self.StunItr += 1
                        else:
                            self.interrupted = False
                    else:
                        self.interrupted = False
                else:
                    self.interrupted = False
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
#class Trigger(Object):
