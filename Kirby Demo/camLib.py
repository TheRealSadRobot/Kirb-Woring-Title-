#class camera:
class Camera:
    def __init__(self, level, focus):
        self.xpos = 0
        self.ypos = 0
        self.__currentLevel = level
        self.__focusx = 0
        self.__focusy = 0
        self.__burner = False
        self.lockMove = False
        if focus == None:
            self.mode = "Control"
        else:
            self.mode = "Follow"
            self.__focus = focus

    def update(self):
        if self.mode == "Follow" and self.lockMove == False:
            try:
                self.__burner = self.__currentLevel.collisionData[int((self.ypos-self.ypos%8+120)/8)][int((self.xpos-self.xpos%8+256)/8)]
                self.__focusx = self.__focus.location[0]
                newPos = self.__focusx-128
                if newPos+256 < self.__currentLevel.maxiX*8:
                    if newPos >= 0:
                        self.xpos = newPos
                    else:
                        self.xpos = 0
            except:
                self.xpos = 256*((self.xpos-self.xpos%256)/256)
            try:
                self.__focusy = self.__focus.location[1]
                self.__burner = self.__currentLevel.collisionData[int((self.ypos-self.ypos%8+240)/8)][int((self.xpos-self.xpos%8+255)/8)]
                newPos = self.__focusy-140
                if newPos+240 < self.__currentLevel.maxiY*8:
                    if newPos >= 0:
                            self.ypos = newPos
                    else:
                        self.ypos = 0
            except:
                self.ypos = 240*((self.ypos-self.ypos%240)/240)
            #print(self.xpos,self.ypos)

    def refocus(self, location):
        if location[0] > 124:
            self.xpos = location[0]-124
        else:
            self.xpos = 0
            
        if location[1] > 120:
            self.ypos = location[1]-120
        else:
            self.ypos = 0

    def movePos(self, xmove,ymove):
        self.__focusx += xmove
        if self.__focusx+256 > self.__currentLevel.maxiX*8:
            self.__focusx -= xmove
        elif self.__focusx < 0:
            self.__focusx = 0
        """else:
            self.__focusx += -1"""
        newPos = self.__focusx
        self.xpos = newPos
        
        self.__focusy += ymove
        if self.__focusy+240 > self.__currentLevel.maxiY*8:
            self.__focusy -= ymove
        elif self.__focusy < 0:
            #print("arg")
            self.__focusy = 0
        """else:
            self.__focusy += -1"""
        newPos = self.__focusy
        self.ypos = newPos
        
