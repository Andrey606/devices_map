from mqtt_client import send_responce
from connect_by_ssh import get_file, parse_file, inArray
from draw import *

# find all nodes
def find_nods(parent, table, depth, parent_coord): 
    child_list = []
    child_position = []

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
    print(child_position)

    # recall this function for looking nodes of found nodes
    for i, node in enumerate(child_list):
        find_nods(node[0], table, depth+1, child_position[i])

    return child_list


# test
f = open("table.txt", "r")
table = parse_file(f)

# draw
Coordinator("00158D00015F3619").display()

find_nods("00158D00015F3619", table, 0, [Coordinator.X_center_coord, Coordinator.Y_center_coord])

init()