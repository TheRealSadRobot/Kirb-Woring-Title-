#class camera:
class Camera:
    def __init__(self, focus, level):
        self.xpos = 0
        self.ypos = 0
        self.__focus = focus
        self.__currentLevel = level
        self.__focusx = 0
        self.__focusy = 0
    def update(self):
        self.__focusx = self.__focus.location[0]
        newPos = self.__focusx-124
        if newPos+256 < self.__currentLevel.maxiX*8:
            if newPos > 0:
                self.xpos = newPos