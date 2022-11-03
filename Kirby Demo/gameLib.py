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
        self.mod = 0
        self.animation = "Idle"
        self.animType = "Loop"
        self.animBacklog = "Fall"
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.animItr = 0
        self.sprite = pygame.Surface((self.spriteSize[0],self.spriteSize[1]))
        self.blockedTop = False
        self.float = False
        self.flap = False
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
        self.move()
        self.animate()
        #if clicked
        #render sprite at location
        self.animFrame = Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][0]
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName][self.animFrame]
        #print(f"{self.grounded}\b")
        self.sprite = pygame.transform.scale(self.sprite,(self.spriteSize[0],self.spriteSize[1]))
        #print(self.sprite.get_size())
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
        if len(Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber]) > 2:
             self.sprite.blit(pygame.transform.rotate(self.sprite,Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][2]),(0,0))
        self.sprite.blit(self.pallateApply(self.pallate, self.sprite),(0,0))
        if self.dir == "right":
            self.renderLayer.blit(self.sprite, (self.location[0]-cam.xpos,self.location[1]), (0,0,self.spriteSize[0],self.spriteSize[1]))
        else:
            self.renderLayer.blit(pygame.transform.flip(self.sprite,1,0), (self.location[0]-cam.xpos,self.location[1]), (0,0,self.spriteSize[0],self.spriteSize[1]))

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
                        selfrenderLayer.fill((0,255,0), ((point[0],point[1]), (0,0)))
                        return True
                    else:
                        return False
            else:
                return False
        except:
            return True
            #print(f"{self.charName} {self.pallateName} is reigestering collision")

class Player(Object):
    def __init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level):
        Object.__init__(self, charName, xlocation, ylocation, arrayDestination,renderLayer, pallate,Level)
        self.alive = True
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
        collide = self.collideWithObj()
        if isinstance(collide, Enemy):
            self.Kill()
        #run physics sim
        if self.grounded == False:
            self.physicsSim()
        else:
            self.float = False
            self.speed[1] = 0
        #grounded and ungrounded
        #check for input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.Kill()
        if keys[pygame.K_LEFT]:
            self.dir = "left"
            #if not blocked on left side
            if self.blockedLeft == False:
                self.speed[0] = -1
        elif keys[pygame.K_RIGHT]:
            self.dir = "right"
            if self.blockedRight == False:
                self.speed[0] = 1
        else:
            self.speed[0] = 0
        #grounded only
        #print(self.speed[1])
        #print(self.flap)
        #print(self.animation)
        if self.grounded == True:
            self.float = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                self.playAnimation("Walk")
            else:
                self.playAnimation("Idle")
            if keys[pygame.K_SPACE]:
                if self.flap == False:
                    if self.mod == 1:
                        self.flap = True
                    self.mod = 1
                    self.grounded = False
                    self.playAnimation("Jump")
                    self.speed[1] = -(self.jumpHeight)
            else:
                self.flap = False
                self.mod = 0
        #ungrounded only
        elif self.grounded == False:
            if self.speed[1] == 0:
                if self.animation == "Fall":
                    pass
                else:
                    self.playAnimationOnce("Roll","Fall")
            if self.speed[1] > 0:
                if self.float == False:
                    self.playAnimation("Fall")
                else:
                    self.playAnimation("Float")
            else:
                if self.float == False:
                    self.playAnimation("Jump")
            if keys[pygame.K_SPACE]:
                if self.flap == False:
                    self.flap = True
                    if self.float == False:
                        self.float = True
                        self.playAnimationOnce("Inflate", "Float")
                    else:
                        self.playAnimationOnce("Flap","Float")
                    self.speed[1] = -self.jumpHeight/2
            else:
                self.flap = False
                
            if self.float == True:
                self.fallSpeed = 2
            else:
                self.fallSpeed = 7

        #top blocked only
        if self.blockedTop == True:
            self.speed[1] = 2

        #check for collisions
        self.bottom = [self.location[0]+8,self.location[1]+16]
        if self.collisionCheck(self.bottom) == True:
            itr = 1
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

        self.top = [self.location[0]+8,self.location[1]]
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
            
        self.left = [self.location[0],self.location[1]+7]
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
            
        self.right = [self.location[0]+16,self.location[1]+7]
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
            self.float = False
            self.grounded = False
            time.sleep(1)
            self.speed[1] = -15
            self.fallSpeed = 7

    def deathfall(self, cam):
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

    def update(self, cam):
        #pygame.draw.rect(self.renderLayer, (0,255,0), (self.location[0]+self.spriteSize[0]/2, self.location[1]+self.spriteSize[1],1,1))
        self.bottom = (int(self.location[0]+self.spriteSize[0]/2), int(self.location[1]+self.spriteSize[1]))
        #print(self.bottom)
        if self.collisionCheck(self.bottom) == True:
            itr = 1
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
        if self.grounded == False:
            self.physicsSim()
            print("DEE NOT GROUNDED")
        else:
            self.speed[1] = 0
       
        Object.update(self,cam)

    def Kill(self):
        pass

    def physicsSim(self):
        if self.speed[1] < self.fallSpeed:
            self.speed[1] += 1
        else:
            self.speed[1] = self.fallSpeed

#class Trigger(Object):
