
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import math 

import hxm
import textext

import icon

class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)
    
        self.hexaSize = 20
        self.polys = {}
    
    def setHexaSize(self, number):
        self.hexaSize = number
    
    
    def create_hexagone(self, x, y, coord, color = "black", fill="blue", color1=None, color2=None, color3=None, color4=None, color5=None, color6=None, stipple=None):
        """ 
        Compute coordinates of 6 points relative to a center position.
        Point are numbered following this schema :
    
        Points in euclidiean grid:  
                    6
                    
                5       1
                    .
                4       2
            
                    3
    
        Each color is applied to the side that link the vertex with same number to its following.
        Ex : color 1 is applied on side (vertex1, vertex2)
    
        Take care that tkinter ordinate axes is inverted to the standard euclidian ones.
        Point on the screen will be horizontally mirrored.
        Displayed points:
    
                    3
              color3/      \color2      
                4       2
            color4|     |color1
                5       1
              color6\      /color6
                    6
        
        """
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5

        print(x, y)

        point1 = (x+Δx, y+size/2)
        point2 = (x+Δx, y-size/2)
        point3 = (x   , y-size  )
        point4 = (x-Δx, y-size/2)
        point5 = (x-Δx, y+size/2)
        point6 = (x   , y+size  )
    
        #this setting allow to specify a different color for each side.
        if color1 == None:
            color1 = color
        if color2 == None:
            color2 = color
        if color3 == None:
            color3 = color
        if color4 == None:
            color4 = color
        if color5 == None:
            color5 = color
        if color6 == None:
            color6 = color
    
        # self.create_line(point1, point2, fill=color1, width=3)
        # self.create_line(point2, point3, fill=color2, width=3)
        # self.create_line(point3, point4, fill=color3, width=3)
        # self.create_line(point4, point5, fill=color4, width=3)
        # self.create_line(point5, point6, fill=color5, width=3)
        # self.create_line(point6, point1, fill=color6, width=3)
        
        if fill is None and stipple is None:
            self.polys[coord] =(self.create_polygon(point1, point2, point3, point4, point5, point6, outline="gray", fill="", tags=("clickable",)))

        elif fill != None and stipple is None:
            self.polys[coord] =(self.create_polygon(point1, point2, point3, point4, point5, point6, outline="gray", fill=fill, tags=("clickable",)))

        elif fill is None and stipple != None:
            self.polys[coord] =(self.create_polygon(point1, point2, point3, point4, point5, point6, outline="gray", fill="", stipple=stipple, tags=("clickable",)))

        elif fill != None and stipple != None:
            print("stip")
            self.polys[coord] =(self.create_polygon(point1, point2, point3, point4, point5, point6, outline="gray", fill=fill, stipple=stipple, tags=("clickable",)))

        
    
class HexagonalGrid(HexaCanvas):
    """ A grid whose each cell is hexagonal """
    def __init__(self, master, color="white", *args, **kwargs):
    
        HexaCanvas.__init__(self, master, background=color, *args, **kwargs)
        self.tag_bind("clickable", "<1>", self.onclick)
        self.oldHex = (0,0,0)
        self.selectedHex = (0,0,0)
        
    def setGridSize(self, rows, cols):
        self.update()
        pxWidth = self.winfo_width()
        pxHeight = self.winfo_height()

        self.gridHeight = rows
        self.gridWidth = cols
        grid_height = rows
        grid_width = cols

        scale = min(pxHeight/grid_height, pxWidth/grid_width)

        self.delete("all")
        Δx     = (scale**2 - (scale/2.0)**2)**0.5
        #width  = 2 * Δx * grid_width + Δx
        #height = 1.5 * scale * grid_height + 0.5 * scale
        
        self.width = pxWidth
        self.height = pxHeight 
        self.hexaSize = scale *0.6
        #self.loadImage(None)
    

    def loadImage(self, image):
        new_height = self.gridHeight*int((1+self.hexaSize)*1.66)
        new_width =  self.gridWidth*int((1+self.hexaSize)*1.66)

        old_width, old_height = image.size
        # if new_width/old_width < new_height/old_height is mathematically the same as
        if new_width * old_height < new_height * old_width:
            # reduce height to keep original aspect ratio
            new_height = max(1, old_height * new_width // old_width)
        else:
            # reduce width to keep original aspect ratio
            new_width = max(1, old_width * new_height // old_height)

        image = image.resize((new_width, new_height), Image.LANCZOS)
        imagetk = ImageTk.PhotoImage(image)        

        self.image = imagetk
        img = self.create_image(self.winfo_width()//2-self.hexaSize//2, self.winfo_height()//2, anchor=CENTER, image=imagetk, tags="bg_img")
        self.tag_lower(img)

    def cubeToOffset(self, q, r, s):
        col = q + (r - (r&1)) / 2
        row = r
        return (col, row)
    
    # def setCell(self, x, y, z, *args, **kwargs):
    #     col = x + (z - (z&1)) / 2
    #     row = z
    #     return self.setCellOffset(col, row, *args, **kwargs)
    
    def setCell(self, q, r, s, *args, **kwargs):
        size = self.hexaSize
        pix_x = size * (math.sqrt(3) * q  +  math.sqrt(3)/2 * r)
        pix_y = size * (3./2 * r)
        self.create_hexagone(pix_x+self.width/2, pix_y+self.height/2, (q, r, s), *args, **kwargs)

    def setCellOffset(self, xCell, yCell, *args, **kwargs ):
        """ Create a content in the cell of coordinates x and y. Could specify options throught keywords : color, fill, color1, color2, color3, color4; color5, color6"""
    
        #compute pixel coordinate of the center of the cell:
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5
    
        pix_x = Δx + 2*Δx*xCell + 2.25*size        #X offset 
        if yCell%2 ==1 :
            pix_x += Δx
    
        # Add 5 to avoid clipping on top row of hexes
        pix_y = size + yCell*1.5*size + 1.5*size

        self.create_hexagone(pix_x, pix_y, *args, **kwargs)
    
    def drawCenter(self):
        self.create_oval(self.width/2 - 5, self.height/2 - 5, self.width/2 + 5, self.height/2 + 5,fill="blue")

    def onclick(self, event):
        x = event.x - self.width/2
        y = event.y - self.height/2

        qfrac = (math.sqrt(3)/3 * x - 1/3 * y) / self.hexaSize
        rfrac = (2/3 * y) / self.hexaSize
        sfrac = -qfrac-rfrac        

        q = round(qfrac)
        r = round(rfrac)
        s = round(sfrac)

        q_diff = abs(q - qfrac)
        r_diff = abs(r - rfrac)
        s_diff = abs(s - sfrac)

        if (q_diff > r_diff and q_diff > s_diff):
            q = -r-s
        elif (r_diff > s_diff):
            r = -q-s
        else:
            s = -q-r

        cubeCoord = (int(q), int(r), int(s))
        
        self.oldHex = self.selectedHex
        self.selectedHex=(cubeCoord)
        print(self.selectedHex)



class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.initUI()
        icon.loadIcon(self)

    def initUI(self):
        self.title("Hexmapper")

        self.fogEnabled = BooleanVar()
        self.fogEnabled.set(False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=15)
        self.rowconfigure(0, weight=1)
        menubar = Menu(self)
        self.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=False)
        fileMenu.add_command(label="New HXM", command=self.newHXM)
        fileMenu.add_command(label="Save HXM", command=self.onQuickSave)
        fileMenu.add_command(label="Save HXM as...", command=self.onSave)
        fileMenu.add_command(label="Load HXM...", command=self.onLoad)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        mapMenu = Menu(menubar, tearoff=False)
        mapMenu.add_command(label="Add Image...", command=self.loadNewImage)
        mapMenu.add_checkbutton(label="Fog of War", variable=self.fogEnabled, command=self.toggleFog)
        mapMenu.add_command(label="Refog Map", command=self.refogMap)
        menubar.add_cascade(label="Map", menu=mapMenu)
        
        

        self.infoframe = Frame(self)
        self.mapframe = Frame(self)
       
        self.hexmap = HexagonalGrid(self.mapframe)
        self.hexmap.pack(expand=True, fill=BOTH)
        self.hexmap.bind("<1>", self.onClickHex)


        self.infoframe.grid(column=0, row=0, sticky="nsew")
        self.mapframe.grid(column=1, row=0, sticky="nsew")
        
        
        self.hexName = StringVar()
        self.hexCoord = StringVar()
        self.hexNotes = StringVar()

        self.hexTitleFrame = Frame(self.infoframe) 
        self.nameLabel = ttk.Label(self.hexTitleFrame, textvariable=self.hexName, justify=CENTER, font=('Helvetica', 18, 'bold'), width=30)
        self.subtitleLabel = ttk.Label(self.hexTitleFrame, textvariable=self.hexCoord, justify=CENTER, font=('Helvetica', 12), foreground="gray", width=14)
        self.nameLabel.grid(row=0, column=0, padx=0, sticky="ew")
        self.subtitleLabel.grid(row=1, column=0, padx=0, sticky="ew")

        self.notesText = textext.TextExtension(self.infoframe, textvariable=self.hexNotes, width=5)
        #self.bind("<KeyPress>", self.saveNotes)

        self.hexTitleFrame.pack(anchor=N, expand=False, padx=0)
        self.notesText.pack(anchor=W, fill=BOTH, expand=True)

    def setCell(self, q, r, s, *args, **kwargs):
        self.hexmap.setCell(q, r, s, *args, **kwargs)

    def getClickedHex(self):
        return self.hxm.getHex(self.hexmap.selectedHex)
    
    def getLastHex(self):
        return self.hxm.getHex(self.hexmap.oldHex)

    def updateHex(self):
        hex = self.getClickedHex()
        self.hexName.set(hex.getName())
        self.hexNotes.set(hex.getNotes())
        self.hexCoord.set(str(hex.getCoordStr()))
        
    def toggleFog(self):
        for hex in self.hxm.getHexes():
            coord = hex.getCoord()
            poly = self.hexmap.polys[coord]

            if self.fogEnabled.get():
                print("fog on")
                #TODO: EXPERIMENTAL
                if(hex.getVisibility() == "hidden"):
                    self.hexmap.itemconfig(poly, fill="black", stipple="")
                elif(hex.getVisibility() == "fogged"):
                    self.hexmap.itemconfig(poly, fill="black", stipple="gray75")
                else:
                    self.hexmap.itemconfig(poly, fill="", stipple="")
            else:
                print("fog off")
                self.hexmap.itemconfig(poly, fill="", stipple="")

    def saveNotes(self):
        print("savey")
        hex = self.getLastHex()
        notes = self.hexNotes.get()
        hex.setNotes(notes)

    def update(self):
        self.updateHex()

    def onClickHex(self, event):
        self.saveNotes()
        if self.fogEnabled.get():
            self.hxm.revealNeighbors(self.getClickedHex())
        self.updateHex()
        self.redrawHexmap()
        

    def save_file(self):
        filetypes = (
            ('Hexmap files', '*.hxm'),
            ('All files', '*.*')
        )

        filename = fd.asksaveasfilename(
            title='Save HXM as...',
            initialdir='hexmaps/',
            filetypes=filetypes)

        return filename+".hxm"

    def open_file(self):
        filetypes = (
            ('Hexmap files', '*.hxm'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='hexmaps/',
            filetypes=filetypes)

        return filename

    def open_image(self):
        filetypes = (
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='images/',
            filetypes=filetypes)

        return filename

    def loadNewImage(self):
        imageFile = self.open_image()
        image = Image.open(imageFile)
        self.hexmap.loadImage(image)
        self.hxm.setImage(image)

    def newHXM(self):
        create = False
        

        win = Toplevel()
        win.wm_title("New Map")

        widthVar = IntVar()
        heightVar = IntVar()

        widthLabel = Label(win, text="Width: ")
        heightLabel = Label(win, text="Height")

        widthEntry = Entry(win, textvariable=widthVar)
        heightEntry = Entry(win, textvariable=heightVar)

        createButton = Button(win, text="Create Map", command=lambda ent=win: [self.loadHXM(hxm.buildNewHXM(widthVar.get(), heightVar.get())), win.destroy])
        cancelButton = Button(win, text="Cancel", command=win.destroy)

        widthLabel.grid(column=0, row=0)
        heightLabel.grid(column=0, row=1)
        widthEntry.grid(column=1, row=0)
        heightEntry.grid(column=1, row=1)
        createButton.grid(column=1, row=2)
        cancelButton.grid(column=0, row=2)


    def onSave(self):
        filepath = self.save_file()
        hxm.save_hxm(filepath, self.hxm)

    def onQuickSave(self):
        hxm.save_hxm(self.currentFilepath, self.hxm)

    def onLoad(self):
        filepath = self.open_file()
        self.currentFilepath = filepath
        print(filepath)
        map = hxm.load_hxm(filepath)
        self.loadHXM(map)
        
    def loadHXM(self, hxm):
        self.hxm = hxm
        width = self.hxm.getWidth()
        height = self.hxm.getHeight()
        self.hexmap.setGridSize(height, width)

        image = self.hxm.getImage()
        if image != None:
            self.hexmap.loadImage(image)

        for hex in self.hxm.getHexes():
            if self.fogEnabled.get():
                #TODO: EXPERIMENTAL
                if(hex.getVisibility() == "hidden"):
                    self.hexmap.setCell(*hex.getCoord(),fill="black", stipple=None)
                elif(hex.getVisibility() == "fogged"):
                    self.hexmap.setCell(*hex.getCoord(),fill="black", stipple="gray75")
                else:
                    self.hexmap.setCell(*hex.getCoord(),fill=None, stipple=None)

            else:
                color = hex.getColor()
                self.hexmap.setCell(*hex.getCoord(),fill=None, stipple=None)

           


        self.update()
        self.redrawHexmap()
    

    def drawFog(self):
        for hex in self.hxm.getHexes():
            if self.fogEnabled.get():
                #TODO: EXPERIMENTAL
                if(hex.getVisibility() == "hidden"):
                    self.hexmap.setCell(*hex.getCoord(),fill="black", stipple=None)
                elif(hex.getVisibility() == "fogged"):
                    self.hexmap.setCell(*hex.getCoord(),fill="black", stipple="gray75")
                else:
                    self.hexmap.setCell(*hex.getCoord(),fill=None, stipple=None)


    def refogMap(self):
        for hex in self.hxm.getHexes():
            hex.setVisibility("hidden")
        if self.fogEnabled.get():
            self.loadHXM(self.hxm)

    def redrawHexmap(self):
        
        selCoord = self.hexmap.selectedHex
        oldCoord = self.hexmap.oldHex
        
        selHex = self.hxm.getHex(selCoord)
        oldHex = self.hxm.getHex(oldCoord)

        selHex.setColor("blue")
        selHex.setStipple("gray50")

        oldHex.setColor("")
        oldHex.setStipple("")

        selPoly = self.hexmap.polys[selCoord]
        oldPoly = self.hexmap.polys[oldCoord]

        if(self.fogEnabled.get()):
            neighborCoords = selHex.getNeighbors()

            for coord in neighborCoords:
                if(coord in self.hxm.grid.keys()):
                    print("trying")
                    neighbor = self.hxm.getHex(coord)
                    print(neighbor.getVisibility())
                    if(neighbor.getVisibility() == "fogged"):
                        neighborPoly = self.hexmap.polys[coord]
                        self.hexmap.itemconfig(neighborPoly, fill="black", stipple="gray75")

        self.hexmap.itemconfig(oldPoly, fill=oldHex.color, stipple=selHex.stipple)
        self.hexmap.itemconfig(selPoly, fill=selHex.color, stipple=selHex.stipple)
        
        

        #Laggy
        # for coord in self.hexmap.polys.keys():
        #     hex = self.hxm.getHex(coord)
        #     color = hex.getColor()

        #     poly = self.hexmap.polys[coord]
        #     if(coord == self.hexmap.selectedHex):
        #         self.hexmap.itemconfig(poly, fill="blue", stipple="gray75") 
        #     else:
        #         self.hexmap.itemconfig(poly, fill="blue", stipple="gray25")
        
    def onExit(self):
        self.quit()
if __name__ == "__main__":
    root = MainWindow()

    root.geometry("600x400")
    root.grid_propagate(False)
    root.hexmap.setGridSize(3,3)

    # grid.setCell(0,0, fill='blue')
    # grid.setCell(1,0, fill='red')
    # grid.setCell(0,1, fill='green')
    # grid.setCell(1,1, fill='yellow')
    # grid.setCell(2,0, fill='cyan')
    # grid.setCell(0,2, fill='teal')
    # grid.setCell(2,1, fill='silver')
    # grid.setCell(1,2, fill='white')
    # grid.setCell(2,2, fill='gray')

    root.setCell(*(0,0,0), fill='black')
    root.setCell(*(0,1,-1), fill='grey')
    root.setCell(*(1,0,-1), fill='grey')
    root.setCell(*(1,-1,0), fill='grey')
    root.setCell(*(-1,1,0), fill='grey')
    root.setCell(*(-1,0,1), fill='grey')
    root.setCell(*(0,-1,1), fill='grey')

    root.hexmap.drawCenter()
    root.mainloop()







