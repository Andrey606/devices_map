from mqtt_client import *
from Map import *
from connect_by_ssh import *

# buttons 
def update_button():
    
    if MQTT.send_discovery_request():
        text.insert(END, "Updated!\n")
        var.clean_canv()

        file = SSH.get_file()
        table = SSH.parse_file(file)
    
        var.load_table(table)
        var.find_nods("00158D00015F3619", 0, [400, 350])
        var.display_all_child_link()
        var.display_all_siblings_link()
        var.display_all_nodes()

        root.mainloop()
    else:
        text.insert(END, "TIMEOUT\n")

def sermit_button():
    MQTT.send_setpermit_request()
    text.insert(END, "Permit Opened (60)\n")

def closepermit_button():
    MQTT.send_closepermit_request()
    text.insert(END, "Permit Closed\n")

SSH = SSH()
MQTT = MQTT()

def open_conection_button():
    MQTT.create_connection()    
    SSH.create_connection()
    text.insert(END, "Conection opened\n")

def close_conection_button():
    MQTT.close_connection()
    SSH.close_connection()
    text.insert(END, "Conection closed\n")


# window
root = Tk()
root.geometry('1000x700')
root.title("  zigbee network map")
root.iconbitmap("OMO_logo_Pantone_white_back_150_150.ico")

# button
btn = Button(text="Update", command=update_button).place(x=800, y=0, width=100, height=30)

btn = Button(text="Set permit", command=sermit_button).place(x=800, y=30, width=100, height=30)

btn = Button(text="Close  permit", command=closepermit_button).place(x=900, y=30, width=100, height=30)

btn = Button(text="Open conection", command=open_conection_button).place(x=800, y=60, width=100, height=30)

btn = Button(text="Close conection", command=close_conection_button).place(x=900, y=60, width=100, height=30)

# text
text = Text(root)
text.place(x=802, y=200, width=198, height=500)

# map
f = open("table.txt", "r")
table = SSH.parse_file(f)

var = Map(Canvas(root, width=800, height=700, bg='white'), table, root)
var.find_nods("00158D00015F3619", 0, [400, 350])
var.display_all_child_link()
var.display_all_siblings_link()
var.display_all_nodes()

# ?
root.mainloop()