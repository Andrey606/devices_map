from mqtt_client import send_responce
from connect_by_ssh import get_file
from draw import *



if send_responce() == True:
    for row in get_file():
        print(row)

person1 = Coordinator("coord")
person1.display() 

init()

