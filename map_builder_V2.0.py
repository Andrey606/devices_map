from mqtt_client import *
from Map import *
from connect_by_ssh import *

#button 
def update_button():
    var.clean_canv()

    f = open("table.txt", "r")
    table = SSH.parse_file(f)

    var.load_table(table)
    var.find_nods("00158D00015F3619", 0, [400, 250])
    var.display_all_child_link()
    var.display_all_siblings_link()
    var.display_all_nodes()

    root.mainloop()


# create table and print 
f = open("table.txt", "r")
table = SSH.parse_file(f)


# window
root = Tk()

# button
btn = Button(text="Update", command=update_button)
btn.pack()

# map
var = Map(Canvas(root, width=800, height=500, bg='white'), table)
var.find_nods("00158D00015F3619", 0, [400, 250])
var.display_all_child_link()
var.display_all_siblings_link()
var.display_all_nodes()

# ?
root.mainloop()