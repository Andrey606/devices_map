from tkinter import *
from time import sleep

root = Tk()

# windows settings
WIDTH = 800
HEIGHT = 500

class Coordinator:
    name = "Coordinator"
    X_coord = WIDTH/2
    Y_coord = HEIGHT/2
    MAC_Address = 0
    Short_Address = 0
 
    def display(self):
        print("Привет, меня зовут", self.name)
        c.create_polygon(100, 10, 20, 90, 180, 90)


def init():
    # create window 
    c = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
    c.pack()
    root.mainloop()
