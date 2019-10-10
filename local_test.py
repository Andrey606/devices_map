from mqtt_client import send_responce
from connect_by_ssh import get_file, parse_file, inArray
from draw import *
import time

objects = []

# find all nodes
def find_nods(parent, table, depth, parent_coord): 
    child_list = []
    child_position = []
    global objects

    # look for nodes of parent
    for row in table:
        if row[3] == '1' and not inArray(row[1], child_list) and row[6] == parent:  
            child_list.append( [row[1], row[0], row[4], row[2]] )

        if row[3] == '0' and row[1] == parent and not inArray(row[6], child_list):
            child_list.append( [row[6], 'null', row[4], 'null'] )
            for row2 in table:
                if row2[1] == row[6] and row2[6] == parent:
                    child_list[-1] =  [row2[1], row2[0], row2[4], row2[2]] 
                    break

    # draw them on the holst
    child_position = post_items(child_list, depth+1, parent_coord)

    for i, node in enumerate(child_position):
        objects.append(child_position[i][0])

    # find siblings
    if child_position :
        for row in table:
            if row[3] == '2': 
                for i, node in enumerate(child_position):
                    if child_position[i][0].MAC_Address == row[1] and not parent == row[6]:
                        child_position[i][0].add_siblingTable([row[6], row[4]])
                    elif child_position[i][0].MAC_Address == row[6] and not parent == row[1]:
                        child_position[i][0].add_siblingTable([row[1], row[4]])



    # recall this function for looking nodes of found nodes
    if child_position :
        for i, node in enumerate(child_list):
            find_nods(node[0], table, depth+1, [ child_position[i][0].X_center_coord, child_position[i][0].Y_center_coord, child_position[i][1] ])

    return child_list


def click_button():
    table = []
    
    t = time.time()
    if True:
        print("1: ",  time.time() - t)
        t = time.time()
        f = open("table.txt", "r")
        table = parse_file(f)
        print("2: ",  time.time() - t)
        t = time.time()
        c.delete("all")

        find_nods("00158D00015F3619", table, 0, [Coordinator.X_center_coord, Coordinator.Y_center_coord])

        for node in objects:
            for i, node5 in enumerate(node.siblings):
                for node2 in objects:

                    if node5[0] == node2.MAC_Address:
                        R = 255 + int(node.siblings[i][1]) * round((0 - 255) / 255)
                        G = 0 + int(node.siblings[i][1]) * round((255 - 0) / 255)
                        B = 0 + int(node.siblings[i][1]) * round((0 - 0) / 255)
                        tk_rgb = "#%02x%02x%02x" % (R, G, B)

                        m = 100
                        n = math.sqrt((((node2.X_center_coord + node.X_center_coord)/2)**2) + (((node2.Y_center_coord + node.Y_center_coord)/2)**2))

                        x = node2.X_center_coord +  (m*((node.Y_center_coord - node2.Y_center_coord)/n))
                        y = node2.Y_center_coord +  (m*((node.X_center_coord - node2.X_center_coord)/n))

                        #print("x:", x)
                        #print("y:", y)

                        #print("node.X_center_coord:", node.X_center_coord)
                        #print("node.Y_center_coord:", node.Y_center_coord)
                        #print("node2.X_center_coord:", node2.X_center_coord)
                        #print("node2.Y_center_coord:", node2.Y_center_coord)
        
                        c.create_line(node2.X_center_coord, node2.Y_center_coord, node.X_center_coord, node.Y_center_coord, fill = tk_rgb, width = 1, dash=(2, 2))
                        #c.create_arc([node.X_center_coord,node.Y_center_coord+20], [node2.X_center_coord,node2.Y_center_coord-20],start=0,extent=180,style=ARC,outline=tk_rgb,width=1, dash=(2, 2))
                        i=c.create_text((node2.X_center_coord+node.X_center_coord)/2, (node2.Y_center_coord+node.Y_center_coord)/2, text=node.siblings[i][1], font="Verdana "+"{}".format(SIZE-4), fill="black")
                        r=c.create_rectangle(c.bbox(i),fill="white")
                        c.tag_lower(r,i)
            
            #print("MAC :",node.MAC_Address,"nodes {", node.siblings, "}")

            
            

        Coordinator("00158D00015F3619").display()
        
        print("3: ",  time.time() - t)

        init()
        
    

btn = Button(text="Update", command=click_button)
btn.pack()

init()