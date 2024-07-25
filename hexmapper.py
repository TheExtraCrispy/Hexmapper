

#Hex grid coordinates, cube coordinates

#3 axis: 
#   Z/R: Equatorial        like ------
#   X/Q: Moonwise        like \\\\\\
#   Y/S: Sunwise           like //////



import gui


root = gui.MainWindow()
root.grid_propagate(False)
root.state("zoomed")

root.mainloop()

