from tkinter import *
from time import sleep
import math

root = Tk()

# windows settings
WIDTH = 800
HEIGHT = 500
SIZE = 10
RADIUS  = 100
STEP = 50

c = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
c.pack()

def init():
    # create window 
    root.mainloop()

class Coordinator:
    X_center_coord = WIDTH/2
    Y_center_coord = HEIGHT/2
    MAC_Address = 0
    Short_Address = "0000"

    def __init__(self, mac):
        self.MAC_Address = mac
 
    def display(self):
        c.create_polygon(self.X_center_coord, self.Y_center_coord-SIZE, self.X_center_coord-SIZE, self.Y_center_coord+SIZE, self.X_center_coord+SIZE, self.Y_center_coord+SIZE)
        c.create_text(self.X_center_coord+SIZE+5, self.Y_center_coord-(SIZE/2), text=self.MAC_Address, justify=CENTER, font="Verdana "+"{}".format(SIZE-4), anchor="w")
        c.create_text(self.X_center_coord+SIZE+5, self.Y_center_coord+(SIZE/2), text=self.Short_Address, justify=CENTER, font="Verdana "+"{}".format(SIZE-4), anchor="w")

class End_device:
    Y_center_coord = 0
    X_center_coord = 0
    Y_center_coord = 0
    MAC_Address = 0
    Short_Address = 0

    def __init__(self, x, y, mac, short):
        self.X_center_coord = x
        self.Y_center_coord = y
        self.MAC_Address = mac
        self.Short_Address = short
    
    def display(self):
        c.create_oval(self.X_center_coord-SIZE, self.Y_center_coord-SIZE, self.X_center_coord+SIZE, self.Y_center_coord+SIZE, fill="black")
        c.create_text(self.X_center_coord+SIZE+5, self.Y_center_coord-(SIZE/2), text=self.MAC_Address, justify=CENTER, font="Verdana "+"{}".format(SIZE-4), anchor="w")
        c.create_text(self.X_center_coord+SIZE+5, self.Y_center_coord+(SIZE/2), text=self.Short_Address, justify=CENTER, font="Verdana "+"{}".format(SIZE-4), anchor="w")

class Router:
    X_center_coord = 0
    Y_center_coord = 0
    MAC_Address = 0
    Short_Address = 0

    def __init__(self, x, y, mac, short):
        self.X_center_coord = x
        self.Y_center_coord = y
        self.MAC_Address = mac
        self.Short_Address = short

    def display(self):
        c.create_rectangle(self.X_center_coord-SIZE, self.Y_center_coord-SIZE, self.X_center_coord+SIZE, self.Y_center_coord+SIZE, fill="black")
        c.create_text(self.X_center_coord+SIZE+5, self.Y_center_coord-(SIZE/2), text=self.MAC_Address, justify=CENTER, font="Verdana "+"{}".format(SIZE-4), anchor="w")
        c.create_text(self.X_center_coord+SIZE+5, self.Y_center_coord+(SIZE/2), text=self.Short_Address, justify=CENTER, font="Verdana "+"{}".format(SIZE-4), anchor="w")
    

def post_items(child_list, depth, parent_coord):
    points = []
    length = len(child_list)
    
    if length <= 0:
        return []

    if depth == 1:
        points = getPoints(WIDTH/2, HEIGHT/2, RADIUS, length, 90, 360) 
    elif depth >= 2:
        points = getPoints(parent_coord[0], parent_coord[1], (RADIUS*(depth-1)), length, parent_coord[2] - ((120 - (120/length))/2), 120)
    
    for i, node in enumerate(child_list):
        R      = 255 + int(node[2]) * round((0 - 255) / 255)
        G      = 0 + int(node[2]) * round((255 - 0) / 255)
        B      = 0 + int(node[2]) * round((0 - 0) / 255)
        tk_rgb = "#%02x%02x%02x" % (R, G, B)

        c.create_line(points[i][0], points[i][1], parent_coord[0], parent_coord[1], fill = tk_rgb, width = 3)
        i=c.create_text((points[i][0]+parent_coord[0])/2, (points[i][1]+parent_coord[1])/2, text=node[2], font="Verdana "+"{}".format(SIZE-4), fill="black")
        r=c.create_rectangle(c.bbox(i),fill="white")
        c.tag_lower(r,i)
        
    for i, node in enumerate(child_list):
        if node[3] == '2': # End evice
            End_device(points[i][0], points[i][1], node[0], node[1]).display()
        elif node[3] == '1': # Router
            Router(points[i][0], points[i][1], node[0], node[1]).display()
        

    return points
            

        


def getPoints(x0, y0, r, noOfDividingPoints, offset, ang):
    angle = 0
    res = []

    for i in range(0, noOfDividingPoints):
        angle = offset + (i * (ang/noOfDividingPoints))
        res.append([round(x0 + r * math.cos(math.radians(angle)), 1), round(y0 + r * math.sin(math.radians(angle)),1), angle])

    return res
    


