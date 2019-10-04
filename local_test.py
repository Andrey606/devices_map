from mqtt_client import send_responce
from connect_by_ssh import get_file, parse_file
from draw import *

f = open("table.txt", "r")

for row in parse_file(f):
    print(row)


coord = Coordinator(20, 100)
coord.display()

i = 1
while i < 10:
    End_device(0+(i*70), 100, 56, 80).display()
    i = i + 1


init()