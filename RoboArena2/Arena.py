import math
import sys

from BasicRobot import BasicRobot, MovementTyp
from MovementManager import MovementManager_
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from Terrain import boost, fire, normal, spikes, wall, water, terrain


class Worker(QThread):
    def __init__(self, robot):
        QThread.__init__(self)
        self.robot = robot

    def run(self):
        # function gets called at start()
        self.movementManager = MovementManager_(self.robot)

    def moveRobot(self):
        # MovementManager handles the movement
        self.movementManager.moveInShape()


class Arena(QMainWindow):  # Erbt von QMainWindow class,
    # allows to use methods like setWindowTitle directly...
    robotSignal = pyqtSignal()
    listOfThreads = {}

    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 1000
        self.tiles = [[terrain() for i in range(100)] for j in range(100)]
        self.robots = []
        self.title = "RoboArena"
        self.top = 0
        self.left = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_arena)
        self.timer.start(100)


        list_with_tiles = []
        with open("testarena.txt", "r") as file:  # Opens the textfile
            content = file.read()
            content = content.replace(" ", "").replace("\n", "")
        for letter in content:  # saves every letter in a list
            list_with_tiles.append(letter)
        for y in range(0, 100):  # Iterates through every possible tile
            for x in range(0, 100):
                next_tile = list_with_tiles.pop(
                    0
                )  # first element is deleted and returned from the list
                if next_tile == "w":
                    self.tiles[y][x] = wall()  # The coordinate is marked with
                    # the designated terrain_type
                    # Depending on the type of the tile, different
                    # colors are used
                if next_tile == "a":
                    self.tiles[y][x] = water()
                if next_tile == "f":
                    self.tiles[y][x] = fire()
                if next_tile == "s":
                    self.tiles[y][x] = spikes()
                if next_tile == "b":
                    self.tiles[y][x] = boost()
                if next_tile == "n":
                    self.tiles[y][x] = normal()


    def get_size(self):  # method to print actual size of the arena
        print(  # split the string in two lines due to max line length
            f"The arena size is {self.width}x{self.height} pixels and "
            f"positioned top {self.top}, left {self.left}."
        )

    def update_arena(self):
        self.robotSignal.emit()
        self.update()

    def set_tile(
        self, x, y, type
    ):  # changes the type of tile in the included coordinate
        self.tiles[y][x] = type

    def get_tile(
        self, x, y
    ):  # return the type of the tile in the included coordinate
        return self.tiles[y][x]

    def add_robot(self, robot):
        self.robots.append(robot)

    def InitWindow(self):  # Displays the Arena
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    # basic threading
    def runTask(self):
        # adds all robots to the threading dictionary
        for i in range(len(self.robots)):
            key = i
            robot = self.robots[i]
            value = Worker(robot)
            self.listOfThreads[key] = value
        # starting the threads and connecting the signals
        for i in range(len(self.listOfThreads)):
            self.robotSignal.connect(self.listOfThreads[i].moveRobot)
            self.listOfThreads[i].start()

    def paintEvent(self, event):  # Colors the tiles
        painter = QPainter(self)
        for y in range(0, 100):  # Iterates through every possible tile
            for x in range(0, 100):
                painter.drawPixmap(y * 10, x * 10, self.tiles[y][x].graphic)

        for i in range(len(self.robots)):  # draw robots
            painter.setPen(QPen(self.robots[i].color, 8, Qt.DashLine))
            pi = 3.14  # calculate pi
            radians = (
                self.robots[i].alpha / 180.0 * pi
            )  # convert degrees to radians

            endx = int(
                self.robots[i].x + math.cos(radians) * self.robots[i].radius
            )
            endy = int(
                self.robots[i].y + math.sin(radians) * self.robots[i].radius
            )
            diameter = self.robots[i].radius * 2
            painter.drawLine(self.robots[i].x, self.robots[i].y, endx, endy)
            painter.drawEllipse(
                self.robots[i].x - self.robots[i].radius,
                self.robots[i].y - self.robots[i].radius,
                diameter,
                diameter,
            )


xPosition = 500
yPosition = 500
testRobot = BasicRobot(
    xPos=xPosition,
    yPos=yPosition,
    movementtype=MovementTyp.Line,
)
testRobot1 = BasicRobot(
    xPos=xPosition - 100,
    yPos=yPosition,
    movementtype=MovementTyp.Circle,
)

testRobot2 = BasicRobot(
    xPos=xPosition + 100,
    yPos=yPosition,
    movementtype=MovementTyp.Wave,
)

App = QApplication(sys.argv)
testarena = Arena()

testarena.add_robot(testRobot)
testarena.add_robot(testRobot1)
testarena.add_robot(testRobot2)
testarena.runTask()
testarena.InitWindow()


sys.exit(App.exec())
