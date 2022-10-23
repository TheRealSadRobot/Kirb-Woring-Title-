#imports
#setup
#level Layout should be like this:
    #inside .json file for level:
        #Layot of level, in the form of a list of lists of numbers, which correspond to the tilekey in the main Datafile
        #Layout of Objects in the level, in the form of a list of lists of item properties
        #Theme Map, in the same form as layout, with numbers corresponding to tilesets.
        #FlipMap, in the same form as layout, with entries determining the nature of flipping
        #locations of Music and BGs
#def main
    #while True
        #display Level
        #if mode is place blocks:
            #placeblocks
        #else if mode is place objects
            #placeobject
#def placeblocks
        #if square of level is clicked:
            #place a block there
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
