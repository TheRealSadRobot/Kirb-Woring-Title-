#class camera:
class Camera:
    def __init__(self, level, focus):
        self.xpos = 0
        self.ypos = 0
        self.__currentLevel = level
        self.__focusx = 0
        self.__focusy = 0
        if focus == None:
            self.mode = "Control"
        else:
            self.mode = "Follow"
            self.__focus = focus

    def update(self):
        if self.mode == "Follow":
            self.__focusx = self.__focus.location[0]
            newPos = self.__focusx-124
            if newPos+256 < self.__currentLevel.maxiX*8:
                if newPos > 0:
                    self.xpos = newPos
            self.__focusy = self.__focus.location[1]
            newPos = self.__focusy-120
            if newPos+240 < self.__currentLevel.maxiY*8:
                if newPos > 0:
                    self.ypos = newPos

    def refocus(self, location):
        if location[0] > 124:
            self.xpos = location[0]-124
        else:
            self.xpos = 0

    def movePos(self, xmove,ymove):
        self.__focusx += xmove
        if self.__focusx+256 > self.__currentLevel.maxiX*8:
            self.__focusx -= xmove
        elif self.__focusx < 0:
            self.__focusx -= xmove
        newPos = self.__focusx
        self.xpos = newPos
        
        self.__focusy += ymove
        if self.__focusy+240 > self.__currentLevel.maxiY*8:
            self.__focusy -= ymove
        elif self.__focusy < 0:
            self.__focusy -= ymove
        newPos = self.__focusy
        self.ypos = newPos
        
