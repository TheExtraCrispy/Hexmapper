#HXM format
#
#   Dict with these fields:
#   name        -   string name of map
#   width       -   Number of hexes across the width
#   height      -   Number of hexes from top to bottom
#   grid        -   Dict mapping coordinate to hex 
#   image       -   background image

#HEX format
#
#   Custom class with
#
#   q, r, s     -   coordinates
#   notes       -   plaintext attached to hex
#   name        -   Custom name, name defaults to coords unless altered. 
#   color       -   color fill string
#   stipple     -   stipple string
#   icon        -   reference to small image overlaid on hex
import pickle
import math
from PIL import Image



class HexTile:
    def __init__(self, q, r, s, name=None, notes=None, color="grey", visibility="hidden", stipple=None):

        self.q = q
        self.r = r
        self.s = s

        self.name = name
        self.notes = notes
        self.color = color
        self.stipple = stipple

        #TODO: TESTING THIS
        self.visibility = visibility

    def getNeighbors(self):
        #returns a list of coordinates for this hex's neighbors
        return [
                self.shiftCoord(1, 0, -1), 
                self.shiftCoord(1, -1, 0), 
                self.shiftCoord(0, -1, 1), 
                self.shiftCoord(-1, 0, 1), 
                self.shiftCoord(-1, 1, 0), 
                self.shiftCoord(0, 1, -1)
               ]

    def shiftCoord(self, dq, dr, ds):
        return (self.q + dq, self.r + dr, self.s + ds)
    
    def getCoord(self):
        return (self.q, self.r, self.s)
    
    def getCoordStr(self):
        return f"{self.q}, {self.r}, {self.s}"

    def getName(self):
        return self.name
    
    def getNotes(self):
        return self.notes
    
    def setNotes(self, notes):
        self.notes = notes
    
    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color
    
    def getVisibility(self):
        return self.visibility
    
    def setVisibility(self, visibility):
        self.visibility = visibility

    def setStipple(self, stipple):
        self.stipple = stipple
class hxm:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

        self.grid = {}
        self.image = None
    
    def getHex(self, coord):
        return self.grid[coord]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
    
    def getHexes(self):
        return self.grid.values()
    
    def getImage(self):
        return self.image

    def setImage(self, image):
        self.image = image
    

    def revealNeighbors(self, hex):
        neighborCoords = hex.getNeighbors()
        hex.setVisibility("explored")

        for coord in neighborCoords:
            if coord in self.grid.keys():
                neighbor = self.getHex(coord)

                if(neighbor.getVisibility() == "hidden"):
                    neighbor.setVisibility("fogged")


    def addHex(self, coord, name=None, notes=None, color="grey", stipple="grey25"):
        if(not name is None):
            name = name
        else:
            name = str(coord)

        if(not notes is None):
            notes = notes
        else:
            notes = ""

        newHex = HexTile(*coord, name=name, notes=notes, color=color, stipple=stipple)

        self.grid[coord] = newHex

def save_hxm(name, data):
    #Saves provided data to an HXM file of the given name
    file = open(name, 'wb')
    pickle.dump(data, file)
    file.close()


def load_hxm(hxmpath):
    #Reads an HXM file and returns the stored dict.
    #Provide name of hxm file
    #TODO: Add file type check, file exists check

    file = open(hxmpath, 'rb')
    out = pickle.load(file)
    file.close()

    return out



def offsetToCube(row, col):
    q = col - (row + (row&1)) / 2
    r = row
    s = -q-r
    return (q, r, s)

def buildNewHXM(width, height):
    newMap = hxm("New Map", width, height)
    
    for col in range(-math.floor(width/2), width-math.floor(width/2)):
        for row in range(-math.floor(height/2), height-math.floor(height/2)):
            cubeCoord = offsetToCube(row, col)
            if cubeCoord == (0,0,0):
                newMap.addHex(cubeCoord, name="Origin", notes="", color="blue", stipple="gray25")
            else:
                newMap.addHex(cubeCoord, color="", stipple="")

    return newMap

def build_test_hxm(name):
    test = hxm(name, 3, 3)
    test.grid = build_test_grid()
    #test.image = Image.open("images/test.png")

    return test

def build_test_grid():
    grid = {}

    coord = (0,0,0)
    grid[coord] = HexTile(*coord, name="Origin", notes="Origin, TEST", color="black")

    coord = (0,-1,1)
    grid[coord] = HexTile(*coord, name="U_L", notes="U_L NEIGHBOR OF ORIGIN")

    coord = (1,-1,0)
    grid[coord] = HexTile(*coord, name="U_R", notes="U_R NEIGHBOR OF ORIGIN")

    coord = (-1,0,1)
    grid[coord] = HexTile(*coord, name="L", notes="L NEIGHBOR OF ORIGIN")

    coord = (1,0,-1)
    grid[coord] = HexTile(*coord, name="R", notes="R NEIGHBOR OF ORIGIN")

    coord = (-1,1,0)
    grid[coord] = HexTile(*coord, name="B_L", notes="B_L NEIGHBOR OF ORIGIN")

    coord = (0,1,-1)
    grid[coord] = HexTile(*coord, name="B_R", notes="B_R NEIGHBOR OF ORIGIN")

    return grid


#TESTING

map = build_test_hxm("test2")
save_hxm("test", map)

#map = load_hxm("test2")

# import matplotlib.pyplot as plt
# plt.figure()
# plt.imshow(map.image) 
# plt.show()  # display it

#print(map.grid[(0,0,0)].getNeighbors())

#for c in map.grid[(0,0,0)].getNeighbors():
#    print(map.grid[c].notes)