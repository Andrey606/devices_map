from tkinter import *
import math

class Map():
    # size of objects
    SIZE = 10
    RADIUS = 100

    # Info table 
    table = []

    # Objects array
    routers = []
    end_devices = []
    coordinators = []

    # Array with info
    child_links = []
    sibling_links = []

    def __init__(self, canvas, table, root):
        self.canv = canvas
        self.table = table
        self.canv.pack(side="left")
        self.canv.config(scrollregion=(-0,0,1000, 1000))
        self.canv.config(highlightthickness=0)

        self.sbar = Scrollbar(root)
        self.sbar.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=self.sbar.set)

    def create_new_coordinator(self, mac, x_centr, y_centr):
        coord = Map.Coordinator(mac, x_centr, y_centr, self.canv, self.SIZE)
        self.coordinators.append(coord)

    def create_new_router(self, x_centr, y_centr, mac, short, angle):
        router = Map.Router(x_centr, y_centr, mac, short, angle, self.canv, self.SIZE)
        self.routers.append(router)
        return router

    def create_new_end_device(self, x_centr, y_centr, mac, short, angle):
        end_device = Map.End_device(x_centr, y_centr, mac, short, angle, self.canv, self.SIZE)
        self.end_devices.append(end_device)

    def create_new_child_link(self, x1, y1, x2, y2, width, text):
        self.child_links.append( [x1, y1, x2, y2, width, text] )

    def create_siblings_link(self, width):
        for node in self.routers:
            for i, node5 in enumerate(node.siblings):
                for node2 in self.routers:

                    if node5[0] == node2.MAC_Address:
                        m = 20
                        n = math.sqrt((((node2.X_center_coord + node.X_center_coord)/2)**2) + (((node2.Y_center_coord + node.Y_center_coord)/2)**2))
                        x = node2.X_center_coord +  (m*((node.Y_center_coord - node2.Y_center_coord)/n))
                        y = node2.Y_center_coord +  (m*((node.X_center_coord - node2.X_center_coord)/n))

                        if((node.angle - node2.angle)%180 == 0):
                            m=20
                        else:
                            self.sibling_links.append( [ node2.X_center_coord, node2.Y_center_coord, node.X_center_coord, node.Y_center_coord, width, node.siblings[i][1] ] )

    def display_all_siblings_link(self):
        for link in self.sibling_links:
            R = 255 + int(link[5]) * round((0 - 255) / 255)
            G = 0 + int(link[5]) * round((255 - 0) / 255)
            B = 0 + int(link[5]) * round((0 - 0) / 255)
            tk_rgb = "#%02x%02x%02x" % (R, G, B)
            self.canv.create_line(link[0], link[1], link[2], link[3], fill=tk_rgb, width=link[4], dash=(4,2))
            i=self.canv.create_text( (link[0]+link[2])/2, (link[1]+link[3])/2, text=link[5], font="Verdana "+"{}".format(self.SIZE-4), fill="black")
            r=self.canv.create_rectangle(self.canv.bbox(i),fill="white")
            self.canv.tag_lower(r,i)

    def display_all_child_link(self):
        for link in self.child_links:
            R      = 255 + int(link[5]) * round((0 - 255) / 255)
            G      = 0 + int(link[5]) * round((255 - 0) / 255)
            B      = 0 + int(link[5]) * round((0 - 0) / 255)
            tk_rgb = "#%02x%02x%02x" % (R, G, B)
            self.canv.create_line(link[0], link[1], link[2], link[3], fill=tk_rgb, width=link[4])
            i=self.canv.create_text( (link[0]+link[2])/2, (link[1]+link[3])/2, text=link[5], font="Verdana "+"{}".format(self.SIZE-4), fill="black")
            r=self.canv.create_rectangle(self.canv.bbox(i),fill="white")
            self.canv.tag_lower(r,i)

    def display_all_nodes(self):
        for node in self.routers:
            node.display()

        for node in self.end_devices:
            node.display()

        for node in self.coordinators:
            node.display()

    def find_nods(self, parent_mac, depth, parent_coord): 
        child_list = []

        # create coordinator if not created
        if not self.coordinators:
            self.create_new_coordinator( parent_mac, parent_coord[0], parent_coord[1] )

        # look for nodes of parent
        for row in self.table:
            if row[3] == '1' and not self.inArray(row[1], child_list) and row[6] == parent_mac:  
                child_list.append( [row[1], row[0], row[4], row[2]] )

            if row[3] == '0' and row[1] == parent_mac and not self.inArray(row[6], child_list):
                child_list.append( [row[6], 'xxxx', row[4], '1'] )
                for row2 in self.table:
                    if row2[1] == row[6] and row2[6] == parent_mac:
                        child_list[-1] =  [row2[1], row2[0], row2[4], row2[2]] 
                        break
        
        # create objects of routers and end_devices
        # child_list      = [ ["00158D00015F6556", "BF0F", LQI, TYPE], ... ]
        self.post_items(child_list, depth+1, parent_coord, parent_mac)

        self.create_siblings_link(1)
        
    def post_items(self, child_list, depth, parent_coord, parent_mac):
        # parent_coord = [x, y]
        # parent_coord = [x, y, angle]
        points = []
        
        if not (len(child_list) <= 0): 
            if depth == 1:
                points = self.getPoints(self.coordinators[0].X_center_coord, self.coordinators[0].Y_center_coord, self.RADIUS, len(child_list), 90, 360) 
            elif depth >= 2:
                points = self.getPoints(parent_coord[0], parent_coord[1], (self.RADIUS), len(child_list), parent_coord[2] - ((120 - (120/len(child_list)))/2), 120)
            
            for i, node in enumerate(child_list):
                self.create_new_child_link( points[i][0], points[i][1], parent_coord[0], parent_coord[1], 3, node[2] )
                
                if node[3] == '2': # End evice
                    self.create_new_end_device(points[i][0], points[i][1], node[0], node[1], points[i][2])
                elif node[3] == '1': # Router
                    router = self.create_new_router(points[i][0], points[i][1], node[0], node[1], points[i][2])
                    self.find_nods( node[0], depth+1, [ points[i][0], points[i][1], points[i][2] ] )
                    
                    # find siblings
                    for row in self.table:
                        if row[3] == '2': 
                            for i, node in enumerate(self.routers):
                                if node.MAC_Address == row[1] and not parent_mac == row[6]:
                                    node.add_siblingTable([row[6], row[4]])
                                elif node.MAC_Address == row[6] and not parent_mac == row[1]:
                                    node.add_siblingTable([row[1], row[4]])

    def getPoints(self, x0, y0, r, noOfDividingPoints, offset, ang):
        angle = 0
        res = []

        for i in range(0, noOfDividingPoints):
            angle = offset + (i * (ang/noOfDividingPoints))
            res.append([ round(x0 + r * math.cos(math.radians(angle)), 1), round(y0 + r * math.sin(math.radians(angle)),1), angle ])
    
        return res

    def inArray(self, var, array):
        for arr1 in array:
            if var in arr1:
                return True
        
        return False

    def clean_canv(self):
        self.canv.delete("all")
        #self.table.clear()
        self.routers.clear()
        self.end_devices.clear()
        self.coordinators.clear()
        self.child_links.clear()
        self.sibling_links.clear()

    def load_table(self, table):
        self.table.clear()
        self.table = table

    class Coordinator:
        def __init__(self, mac, x_centr, y_centr, canv, size):
            self.MAC_Address = mac
            self.X_center_coord = x_centr
            self.Y_center_coord = y_centr
            self.Short_Address = "0000"
            self.siblings = []
            self.canv = canv
            self.SIZE = size
    
        def display(self):
            self.canv.create_polygon(self.X_center_coord, self.Y_center_coord-self.SIZE, self.X_center_coord-self.SIZE, self.Y_center_coord+self.SIZE, self.X_center_coord+self.SIZE, self.Y_center_coord+self.SIZE)
            self.canv.create_text(self.X_center_coord+self.SIZE+5, self.Y_center_coord-(self.SIZE/2), text=self.MAC_Address, justify=CENTER, font="Verdana "+"{}".format(self.SIZE-4), anchor="w")
            self.canv.create_text(self.X_center_coord+self.SIZE+5, self.Y_center_coord+(self.SIZE/2), text=self.Short_Address, justify=CENTER, font="Verdana "+"{}".format(self.SIZE-4), anchor="w")

    class Router:
        def __init__(self, x, y, mac, short, angle, canv, size):
            self.X_center_coord = x
            self.Y_center_coord = y
            self.MAC_Address = mac
            self.Short_Address = short
            self.siblings = []
            self.angle = angle
            self.canv = canv
            self.SIZE = size

        def clean_siblingTable(self):  
            self.siblings.clear()

        def add_siblingTable(self, mac):
            if not mac == self.MAC_Address :
                if not self.siblings:
                    self.siblings.append(mac)
                else:
                    for sibling in self.siblings:
                        if sibling == mac:
                            break
                        self.siblings.append(mac)  

        def display(self):
            self.canv.create_rectangle(self.X_center_coord-self.SIZE, self.Y_center_coord-self.SIZE, self.X_center_coord+self.SIZE, self.Y_center_coord+self.SIZE, fill="black")
            self.canv.create_text(self.X_center_coord+self.SIZE+5, self.Y_center_coord-(self.SIZE/2), text=self.MAC_Address, justify=CENTER, font="Verdana "+"{}".format(self.SIZE-4), anchor="w")
            self.canv.create_text(self.X_center_coord+self.SIZE+5, self.Y_center_coord+(self.SIZE/2), text=self.Short_Address, justify=CENTER, font="Verdana "+"{}".format(self.SIZE-4), anchor="w")

    class End_device:
        def __init__(self, x, y, mac, short, angle, canv, size):
            self.X_center_coord = x
            self.Y_center_coord = y
            self.MAC_Address = mac
            self.Short_Address = short
            self.angle = angle
            self.canv = canv
            self.SIZE = size

        def display(self):
            self.canv.create_oval(self.X_center_coord-self.SIZE, self.Y_center_coord-self.SIZE, self.X_center_coord+self.SIZE, self.Y_center_coord+self.SIZE, fill="black")
            self.canv.create_text(self.X_center_coord+self.SIZE+5, self.Y_center_coord-(self.SIZE/2), text=self.MAC_Address, justify=CENTER, font="Verdana "+"{}".format(self.SIZE-4), anchor="w")
            self.canv.create_text(self.X_center_coord+self.SIZE+5, self.Y_center_coord+(self.SIZE/2), text=self.Short_Address, justify=CENTER, font="Verdana "+"{}".format(self.SIZE-4), anchor="w")
       
