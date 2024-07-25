

#Hex grid coordinates, cube coordinates

#3 axis: 
#   Z/R: Equatorial        like ------
#   X/Q: Moonwise?         like \\\\\\
#   Y/S: Sunwise           like //////

#pickle? To save load dict?

#Idea: Use a dict to store data. Data is plain text, coordinates are the key. [X,Y,Z]

#maybe even use tkinter to make aGUI?


#Data structure?
#A dict, contains:
#   a grid (another dict)
#   A map image for tkinter
#   Other info? Can add as desired.
#   Maybe a grid size? X by Y by Z


import gui


root = gui.MainWindow()
root.grid_propagate(False)
root.state("zoomed")

root.mainloop()

