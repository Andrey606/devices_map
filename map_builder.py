from mqtt_client import send_responce
from connect_by_ssh import get_file
from draw import *


if send_responce() == True:
    for row in get_file():
        print(row)


coord = Coordinator(20, 100)
coord.display()

i = 1
while i < 10:
    End_device(0+(i*70), 100, 56, 80).display()
    i = i + 1





init()

