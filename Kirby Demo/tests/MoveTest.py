import pygame

class testObj:
    def __init__(self,output):
        self.output = output
        self.speed = [0,0]
        self.maxspeed = [10,10]
        self.location = [0,0]
    def update(self):
        if self.location[1] >= 450:
            self.location[1] = 450
            self.speed[1] = 0
        else:
            if self.speed[1] < 50:
                self.speed[1] += 2
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            #print("Dip")
            if abs(self.speed[0]) < self.maxspeed[0]:
                self.speed[0] += -1
        elif keys[pygame.K_RIGHT]:
            if abs(self.speed[0]) < self.maxspeed[0]:
                self.speed[0] += 1
        else:
            if self.speed[0] > 0:
                self.speed[0] -= 1
            elif self.speed[0] < 0:
                self.speed[0] += 1
        if keys[pygame.K_UP]:
            if abs(self.speed[1] < self.maxspeed[1]):
                self.speed[1] += -1
        elif keys[pygame.K_DOWN]:
            if abs(self.speed[1] < self.maxspeed[1]):
                self.speed[1] += 1
        if keys[pygame.K_SPACE]:
            self.speed[1] = -10
        else:
            if self.speed[1] > 0:
                self.speed[1] -= 1
            elif self.speed[1] < 0:
                self.speed[1] += 1
        self.location[0]+=self.speed[0]
        self.location[1]+=self.speed[1]
        pygame.draw.rect(self.output,(255,0,0),(self.location[0],self.location[1],10,10))
pygame.init()
displayPane = pygame.Surface((1000,500))
window = pygame.display.set_mode((1000,500))
fpstimer = pygame.time.Clock()
testObj1 = testObj(displayPane)
while True:
    fpstimer.tick(60)
    displayPane.fill((255,255,255))
    testObj1.update()
    window.blit(displayPane,(0,0))
    pygame.display.flip()
    pygame.event.get()
