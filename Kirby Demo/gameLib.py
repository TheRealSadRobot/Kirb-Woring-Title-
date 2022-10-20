import json
import pygame
import time
#spritesheet
Sheet = pygame.image.load("Kirbo Sprites.png")
#metadata for spritesheet
Datafile = json.load(open("Support.json"))

class Character:
    def __init__(self, charName, behaviorType, xlocation, ylocation, arrayDestination,renderLayer, pallate):
        self.charName = charName
        #behavior type
        self.behaviorType = behaviorType
        self.speed = [0,0]
        self.location =[xlocation, ylocation]
        self.dir = "right"
        self.pallate = Datafile["Character"]["Pallates"][self.charName][pallate]
        self.fallSpeed = 7
        self.jumpHeight = 15
        self.grounded = False
        #current sprite
        self.animFrame = "Idle1"
        self.animFrameNumber = 0
        self.animation = "Idle"
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.animItr = 0
        self.sprite = pygame.Surface((self.spriteSize[0],self.spriteSize[1]))
        self.blockedTop = False
        self.renderLayer = renderLayer
        #add to array of all objects
        arrayDestination.append(self)
        
    def update(self, cam):
        self.move()
        self.animate()
        #if behaviorType = player
        if self.behaviorType.lower() == "player":
            self.playerscript()
        #if clicked
        #render sprite at location
        self.animFrame = Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][0]
        self.spriteSize = Datafile["Character"]["SpriteSize"][self.charName][self.animFrame]
        self.spriteCoordinates = Datafile["Character"]["SpriteCoordinates"][self.charName][self.animFrame]
        #print(f"{self.grounded}\b")
        
        pygame.transform.scale(self.sprite,(self.spriteSize[0],self.spriteSize[1]))
        self.sprite.blit(Sheet, (0,0),(self.spriteCoordinates[0],self.spriteCoordinates[1],self.spriteSize[0],self.spriteSize[1]))
        self.sprite.blit(self.pallateApply(self.pallate, self.sprite),(0,0))
        if self.dir == "right":
            self.renderLayer.blit(self.sprite, (self.location[0]-cam.xpos,self.location[1]), (0,0,16,16))
        else:
            self.renderLayer.blit(pygame.transform.flip(self.sprite,1,0), (self.location[0]-cam.xpos,self.location[1]), (0,0,16,16))

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
            self.animItr = 0
            self.animFrameNumber = 0
            self.animation = animationName
        
    def animate(self):
        self.animItr += 1
        if self.animItr == Datafile["Character"]["Animations"][self.charName][self.animation][self.animFrameNumber][1]:
            self.animFrameNumber += 1
            self.animItr = 0
        if self.animFrameNumber == len(Datafile["Character"]["Animations"][self.charName][self.animation]):
            self.animFrameNumber = 0
            self.animItr = 0
        
    def moveTo(self):
        #move to the set location at the given speed
        pass
    
    def move(self):
        self.location[0] += self.speed[0]
        self.location[1] = int(self.location[1] + self.speed[1]/2)
        
    def clicked(self):
        #display annoyed sprite
        pass
    def interact(self):
        #if mode is NPC
            #check metadata for text
            #load text
            #paint
        #if mode is char statue:
            #check for what statue it is:
            #set player to statue char
            #set statue to player char
            #set statue char to player char
            #set other char to default value
        pass
    def playerscript(self):
        #run physics sim
        if self.grounded == False:
            if self.speed[1] < self.fallSpeed:
                self.speed[1] += 1
            else:
                self.speed[1] = self.fallSpeed
        else:
            self.speed[1] = 0
        #grounded and ungrounded
        #check for input
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.dir = "left"
            #if not blocked on left side
            if self.blockedLeft == False:
                self.speed[0] = -1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.dir = "right"
            if self.blockedRight == False:
                self.speed[0] = 1
        else:
            self.speed[0] = 0
        #grounded only
        if self.grounded == True:
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
                self.playAnimation("Walk")
            else:
                self.playAnimation("Idle")
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.playAnimation("Jump")
                self.speed[1] = -self.jumpHeight
                self.grounded = False
        #ungrounded only
        elif self.grounded == False:
            if self.speed[1] > 0:
                self.playAnimation("Fall")
            else:
                self.playAnimation("Jump")
                
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.playAnimation("Jump")
                self.speed[1] = -self.jumpHeight/2
                self.grounded = False

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
        
    def npcscript(self):
        pass
    def collisionCheck(self, point):
        try:
            #check all four points on character.
            #find what tile type they are on
            tilecountx = (point[0]//8)
            tilecounty = (point[1]//8)
            tilenum = str(Datafile["Layouts"]["Main Room"][tilecounty][tilecountx])
            tiletype = (Datafile["Tilekey"][tilenum])
            #print(tiletype)
            if tiletype != "Air":
                if Datafile["Terrain"]["CollisionData"][Datafile["CollisionKey"][tilenum]][point[0]%8][point[1]%8] == 1:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return True
        
#class textBox:

