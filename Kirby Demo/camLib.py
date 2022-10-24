#class camera:
class Camera:
    def __init__(self, focus, level):
        self.xpos = 0
        self.ypos = 0
        self.__focus = focus
        self.__currentLevel = level
        self.__focusx = 0
        self.__focusy = 0
        self.mode = "Follow"
    def __init__(self, level):
        self.xpos = 0
        self.ypos = 0
        self.__currentLevel = level
        self.__focusx = 0
        self.__focusy = 0
        self.mode = "Control"
    def update(self):
        if self.mode == "Follow":
            self.__focusx = self.__focus.location[0]
            newPos = self.__focusx-124
            if newPos+256 < self.__currentLevel.maxiX*8:
                if newPos > 0:
                    self.xpos = newPos

    def movePos(self, xmove,ymove):
        self.__focusx += xmove
        if self.__focusx+256 > self.__currentLevel.maxiX*8:
            self.__focusx -= xmove
        elif self.__focusx < 0:
            self.__focusx -= xmove
        newPos = self.__focusx
        self.xpos = newPos
        