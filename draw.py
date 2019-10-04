from tkinter import *
from time import sleep

root = Tk()

# windows settings
WIDTH = 800
HEIGHT = 500
SIZE = 10
STEP = 50

c = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
c.pack()

def init():
    # create window 
    root.mainloop()

class Coordinator:
    X_center_coord = WIDTH/2
    Y_center_cecoord = HEIGHT/2
    MAC_Address = 0
    Short_Address = 0

    def __init__(self, mac, short):
        self.MAC_Address = mac
        self.Short_Address = short
 
    def display(self):
        c.create_polygon(self.X_center_coord, self.Y_center_cecoord-SIZE, self.X_center_coord-SIZE, self.Y_center_cecoord+SIZE, self.X_center_coord+SIZE, self.Y_center_cecoord+SIZE)
        c.create_text(self.X_center_coord+SIZE+25, self.Y_center_cecoord-(SIZE/2), text="{:08d}".format(self.MAC_Address), justify=CENTER, font="Verdana "+"{}".format(SIZE-4))
        c.create_text(self.X_center_coord+SIZE+15, self.Y_center_cecoord+(SIZE/2), text="{:04d}".format(self.Short_Address), justify=CENTER, font="Verdana "+"{}".format(SIZE-4))

class End_device:
    X_center_coord = 0
    Y_center_cecoord = 0
    MAC_Address = 0
    Short_Address = 0

    def __init__(self, x, y, mac, short):
        self.X_center_coord = x
        self.Y_center_cecoord = y
        self.MAC_Address = mac
        self.Short_Address = short
    
    def display(self):
        c.create_oval(self.X_center_coord-SIZE, self.Y_center_cecoord-SIZE, self.X_center_coord+SIZE, self.Y_center_cecoord+SIZE, fill="black")
        c.create_text(self.X_center_coord+SIZE+25, self.Y_center_cecoord-(SIZE/2), text="{:08d}".format(self.MAC_Address), justify=CENTER, font="Verdana "+"{}".format(SIZE-4))
        c.create_text(self.X_center_coord+SIZE+15, self.Y_center_cecoord+(SIZE/2), text="{:04d}".format(self.Short_Address), justify=CENTER, font="Verdana "+"{}".format(SIZE-4))


class Router:
    X_center_coord = 0
    Y_center_cecoord = 0
    MAC_Address = 0
    Short_Address = 0

    def __init__(self, x, y, mac, short):
        self.X_center_coord = x
        self.Y_center_cecoord = y
        self.MAC_Address = mac
        self.Short_Address = short

    def display(self):
        c.create_rectangle(self.X_center_coord-SIZE, self.Y_center_cecoord-SIZE, self.X_center_coord+SIZE, self.Y_center_cecoord+SIZE, fill="black")
        c.create_text(self.X_center_coord+SIZE+25, self.Y_center_cecoord-(SIZE/2), text="{:08d}".format(self.MAC_Address), justify=CENTER, font="Verdana "+"{}".format(SIZE-4))
        c.create_text(self.X_center_coord+SIZE+15, self.Y_center_cecoord+(SIZE/2), text="{:04d}".format(self.Short_Address), justify=CENTER, font="Verdana "+"{}".format(SIZE-4))
    
    
