#imports
import levelLib
import camLib
import json
import pygame
import time
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial
Datafile = json.load(open("Support.json"))

#setup
pygame.init()
screenscale = 3
winsizex = 256
winsizey = 240
levelObjects = []
itr = 0
tiletype = 1
themetype = 0
storage = 0

fullscreen = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
              
window = pygame.display.set_mode((winsizex*screenscale,winsizey*screenscale))
pygame.display.set_caption("Kirby's Dream Level Editor")
pygame.display.set_icon(pygame.image.load("EditorLogo.png"))
charLayer = pygame.Surface((winsizex, winsizey))
tileLayer = pygame.Surface((winsizex, winsizey))
displayPane = pygame.Surface((winsizex,winsizey))
Datafile = json.load(open("Support.json"))

#level Layout should be like this:
    #inside .json file for level:
        #Layot of level, in the form of a list of lists of numbers, which correspond to the tilekey in the main Datafile
        #Layout of Objects in the level, in the form of a list of lists of item properties
        #Theme Map, in the same form as layout, with numbers corresponding to tilesets.
        #FlipMap, in the same form as layout, with entries determining the nature of flipping
        #locations of Music and BGs
#def main
def main():
    #level = levelLib.Level("Beach", "StarballRing",levelObjects,charLayer)
    level = levelLib.Level("Beach", "StarballRing",levelObjects,charLayer)
    mainCam = camLib.Camera(level,None)
    toolbarMake(level)
    #while True
    while True:
        #put the stuff from the frame onto the window
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mainCam.movePos(-2,0)
        if keys[pygame.K_RIGHT]:
            mainCam.movePos(2,0)
        if keys[pygame.K_UP]:
            mainCam.movePos(0,-2)
        if keys[pygame.K_DOWN]:
            mainCam.movePos(0,2)
        #if mode is place blocks:
            #placeblocks
        #else if mode is place objects
            #placeobject
        #code for quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    toolbar.destroy()
                except:
                    pass
                quit()
        #display Level
        level.loadLevel(tileLayer, mainCam)
        mainCam.update()
        #draw the frame
        displayPane.blit(tileLayer, (0,0))
        global toolvar
        global storage
        if storage != toolvar.get():
            popListbox()

        if toolvar.get() == 0:
            placeBlocks(level, mainCam)
        elif toolvar.get() == 1:
            flipBlocks(level,mainCam)
        elif toolvar.get() == 2:
            themeBlocks(level,mainCam)

        storage = toolvar.get()
        window.blit(pygame.transform.scale(displayPane, (winsizex*screenscale,winsizey*screenscale)), (0,0))
        tileLayer.fill((0,0,0))
        toolbar.update()
        
def toolbarMake(level):
    #tkinter window for change block type and select tools
    global toolbar
    global Tilebox
    toolbar = tkinter.Tk()
    toolbar.title("Tools")
    toolbar.wm_iconphoto(False, ImageTk.PhotoImage(Image.open("ToolboxIcon.png")))
    #toolbar.geometry(f"{winsizex}x{winsizey}")
    #add a list of all block types
    Tilebox = tkinter.Listbox(toolbar)
    #radio buttons for tool selection
    global BlockImg
    global FlipImg
    global ThemeImg
    global SaveImg
    global toolvar
    toolvar = tkinter.IntVar()
    popListbox()
    BlockImg = ImageTk.PhotoImage(Image.open("BlockBrushLogo.png"))
    FlipImg = ImageTk.PhotoImage(Image.open("FlipBrushLogo.png"))
    ThemeImg = ImageTk.PhotoImage(Image.open("ThemeBrushLogo.png"))
    SaveImg = ImageTk.PhotoImage(Image.open("SaveIcon.png"))
    BlockBrush = ttk.Radiobutton(toolbar, text = "Block Brush", image = BlockImg, compound = "left", variable = toolvar, value = 0)
    BlockBrush.pack()
    FlipBrush = ttk.Radiobutton(toolbar, text = "Flip Brush", image = FlipImg, compound = "left", variable = toolvar, value = 1)
    FlipBrush.pack()
    ttk.Radiobutton(toolbar, text = "Theme Brush", image = ThemeImg, compound = "left", variable = toolvar, value = 2).pack()	
    Tilebox.pack()
    RoomBelowBtn = tkinter.Button(toolbar, text = "New Screen Below", compound = "left", padx = 10, pady = 5, command = partial(screenAddDown, level))
    RoomBelowBtn.pack()
    """RoomAboveBtn = tkinter.Button(toolbar, text = "New Screen Below", compound = "left", padx = 10, pady = 5, command = partial(screenAddUp, level))
    RoomAboveBtn.pack()
    RoomLeftBtn = tkinter.Button(toolbar, text = "New Screen Below", compound = "left", padx = 10, pady = 5, command = partial(screenAddLeft, level))
    RoomLeftBtn.pack()
    RoomRightBtn = tkinter.Button(toolbar, text = "New Screen Below", compound = "left", padx = 10, pady = 5, command = partial(screenAddRight, level))
    RoomRightBtn.pack()"""
    SaveBtn = tkinter.Button(toolbar, text = "Save", image = SaveImg, compound = "left", padx = 10, pady = 5, command = partial(save, level))
    SaveBtn.pack()
    #add new row and column buttons
	#maybe add option to add whole screens?
    #tool to flip tiles
    #tool to add objects

def popListbox():
    Tilebox.delete(0,tkinter.END)
    global toolvar
    if toolvar.get() == 0:
        for item in range(len(Datafile["Tilekey"])-1):
            Tilebox.insert(item, Datafile["Tilekey"][f"{item+1}"])
    elif toolvar.get() == 2:
        for item in range(len(Datafile["Pallatekey"])):
            Tilebox.insert(item, Datafile["Pallatekey"][f"{item}"])

def save(level):
    writeTo = open((f"LevelData\{level.getName()}.json"),'r+')
    writeThis = {"Layout":level.collisionData,
                 "Tileset":level.tileset,
                 "FlipMap":level.flipmap,
                 "Objects":level.file["Objects"],
                 "BG":level.file["BG"],
                 "Music":level.file["Music"],
                 "animList":level.animlist}
    json.dump(writeThis,writeTo)
    print("Your Game--Saved!")

def screenAddDown(level):
    global fullscreen
    for item in fullscreen:
        level.tileset.append(item)
        level.collisionData.append(item)
        level.flipmap.append(item)

#def themebrush
def themeBlocks(level,camera):
    global themetype
    try:
    #change block type if list entry is clicked
        themetype = Tilebox.curselection()[0]
    except:
        themetype = 0
    rawLocale = pygame.mouse.get_pos()
    cursorSpot = [int(rawLocale[0]/screenscale),int(rawLocale[1]/screenscale)]
    collisionCheck(cursorSpot,level,camera)
    if pygame.mouse.get_pressed(3) == (1,0,0):
        row = level.tileset[int(((cursorSpot[1]-cursorSpot[1]%8)+(camera.ypos-camera.ypos%8))/8)]
    #if the tile is not the max value on the Thememap:
        #add one to it
        #print(row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)])
        if row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] < len(Datafile["Pallatekey"]):
            row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = themetype
    #else:
        else:
        #set it to 0
            row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = 0

#def flipbrush
def flipBlocks(level,camera):
    rawLocale = pygame.mouse.get_pos()
    cursorSpot = [int(rawLocale[0]/screenscale),int(rawLocale[1]/screenscale)]
    collisionCheck(cursorSpot,level,camera)
    #if pygame.mouse.get_pressed(3) == (1,0,0):
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEBUTTONDOWN:
            row = level.flipmap[int(((cursorSpot[1]-cursorSpot[1]%8)+(camera.ypos-camera.ypos%8))/8)]
        #if the tile is not 3 on the flipmap:
            #add one to it
            if row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] <= 3:
                row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] += 1
        #else:
            else:
            #set it to 0
                row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = 0

#def placeblocks
def placeBlocks(level, camera):
    try:
    #change block type if list entry is clicked
        tiletype = Tilebox.curselection()[0]+1
    except:
        tiletype = 1
    rawLocale = pygame.mouse.get_pos()
    cursorSpot = [int(rawLocale[0]/screenscale),int(rawLocale[1]/screenscale)]
    collisionCheck(cursorSpot,level,camera)
    #if square of level is clicked:
    #print(int((cursorSpot[0]-cursorSpot[0]%8+(camera.xpos-camera.xpos%8)/8)))
    #print((cursorSpot[1]-cursorSpot[1]%8)/8)
    if pygame.mouse.get_pressed(3) == (1,0,0):
        #place a block there
        row = level.collisionData[int(((cursorSpot[1]-cursorSpot[1]%8)+(camera.ypos-camera.ypos%8))/8)]
        row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = tiletype
        global themetype
        print(themetype)
        try:
            #level.flipMap[int((cursorSpot[1]-cursorSpot[1]%8+(camera.ypos-camera.ypos%8))/8)][int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = themetype
            level.tileset[int((cursorSpot[1]-cursorSpot[1]%8+(camera.ypos-camera.ypos%8))/8)][int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = themetype
        except:
            pass
    elif pygame.mouse.get_pressed(3) == (0,0,1):
        #place a block there
        row = level.collisionData[int(((cursorSpot[1]-cursorSpot[1]%8)+(camera.ypos-camera.ypos%8))/8)]
        row[int(((cursorSpot[0]-cursorSpot[0]%8)+(camera.xpos-camera.xpos%8))/8)] = 0
        #if add row button is pressed:
            #add a row
        #if add column button is pressed:
            #add a column
        #switch block stuff
        #flip block stuff
        #switch tileset stuff
#def placeobject
        #if pixel of level is clicked:
            #place an object there
        #switch object stuff
        #edit object properties stuff

#collision Detection
def collisionCheck(point,level, camera):
    global itr
    #check all four points on character.
    #find what tile type they are on
    tilecountx = ((point[0]+camera.xpos)//8)
    tilecounty = ((point[1]-camera.ypos%8)//8)
    tilenum = str(level.collisionData[tilecounty][tilecountx])
    tiletype = (Datafile["Tilekey"][tilenum])
    #print(tiletype)
    if itr < 30:
        pygame.draw.rect(displayPane,(0,0,255,0),(point[0]-point[0]%8-camera.xpos%8,point[1]-point[1]%8-camera.ypos%8,8,8),1)
        itr += 1
    elif itr > 0:
        pygame.draw.rect(displayPane,(200,200,255,0),(point[0]-point[0]%8-camera.xpos%8,point[1]-point[1]%8-camera.ypos%8,8,8),1)
        itr -= 1
    """if tiletype != "Air":
            if level.file["FlipMap"][tilecounty][tilecountx] != 0:
                    print("flipped")
                    time.wait(1)"""
    return tiletype
main()
