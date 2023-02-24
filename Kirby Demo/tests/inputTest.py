import pygame

class testObj:
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print("Dip")
        if keys[pygame.K_RIGHT]:
            self.speed[0] = 1
        if keys[pygame.K_UP]:
            self.speed[1] = -1
        if keys[pygame.K_DOWN]:
            self.speed[1] = 1
pygame.init()
testObj1 = testObj()
while True:
    testObj1.update()
