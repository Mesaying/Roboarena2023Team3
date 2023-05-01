import sys
from PyQt5.QtWidgets import QApplication, QWidget

class Arena:
    def __init__(self):
        self.width = 1000      #When a new instance is initialized, width and height is automatically set to 1000
        self.height = 1000
        self.tiles = [[0 for i in range(100)] for j in range(100)] # creates 2 dimensional Array

    def get_size(self):        #method to print actual size of the arena
        print(f"The arena size is {self.width}x{self.height} pixels.")

    def change_size(self, w, h): #method to change size of the arena
        self.width = w
        self.height = h

    def set_tile(self,x,y, type): #changes the type of tile in the included coordinate
        self.tiles[y][x] = type

    def get_tile(self,x, y):    # return the type of the tile in the included coordinate
        return self.tiles[y][x]

    def draw(self):   #draw the arena, the code is the same like in the tutorial program
        app = QApplication(sys.argv)

        w = QWidget()
        w.resize(self.width, self.height)

        w.setWindowTitle('Arena')
        w.show()

        sys.exit(app.exec_())



test_arena = Arena()
test_arena.set_tile(4,7, "wall")
print(test_arena.get_tile(4,7))
test_arena.draw()


