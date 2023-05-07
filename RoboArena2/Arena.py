import math
import sys

from BasicRobot import BasicRobot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow
from Terrain import *


class Arena(
    QMainWindow
):  # Erbt von QMainWindow class, allows to use methods like setWindowTitle directly...
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 1000
        self.tiles = [[0 for i in range(100)] for j in range(100)]
        self.robots = []
        self.title = "RoboArena"
        self.top = 0
        self.left = 0

    def get_size(self):  # method to print actual size of the arena
        print(
            f"The arena size is {self.width}x{self.height} pixels and positioned top {self.top}, left {self.left}."
        )

    def set_tile(
        self, x, y, type
    ):  # changes the type of tile in the included coordinate
        self.tiles[y][x] = type

    def get_tile(self, x, y):  # return the type of the tile in the included coordinate
        return self.tiles[y][x]

    def add_robot(self, robot):
        self.robots.append(robot)

    def InitWindow(self):  # Displays the Arena
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, event):  # Colors the tiles
        list_with_tiles = []
        with open("testarena.txt", "r") as file:  # Opens the textfile
            content = file.read()
        for letter in content:  # saves every letter in a list
            list_with_tiles.append(letter)

        painter = QPainter(self)
        for y in range(0, 100):  # Iterates through every possible tile
            for x in range(0, 100):
                next_tile = list_with_tiles.pop(
                    0
                )  # first element is deleted and returned from the list
                if next_tile == "w":
                    self.tiles[y][
                        x
                    ] = (
                        wall()
                    )  # The coordinate is marked with the designated terrain_type
                    painter.setPen(
                        QPen(Qt.black, 8, Qt.DashLine)
                    )  # Depending on the type of the tile, different
                    painter.drawRect(x * 10, y * 10, 10, 10)  # colors are used
                if next_tile == "a":
                    self.tiles[y][x] = water()
                    painter.setPen(QPen(Qt.blue, 8, Qt.DashLine))
                    painter.drawRect(x * 10, y * 10, 10, 10)
                if next_tile == "f":
                    self.tiles[y][x] = fire()
                    painter.setPen(QPen(Qt.red, 8, Qt.DashLine))
                    painter.drawRect(x * 10, y * 10, 10, 10)
                if next_tile == "s":
                    self.tiles[y][x] = spikes()
                    painter.setPen(QPen(Qt.black, 8, Qt.DashLine))
                    painter.drawRect(x * 10, y * 10, 10, 10)
                if next_tile == "n":
                    self.tiles[y][x] = normal()

        for i in range(len(self.robots)):  # draw robots
            pi = 3.14  # calculate pi
            radians = self.robots[i].alpha / 180.0 * pi  # convert degrees to radians

            endx = int(self.robots[i].x + math.cos(radians) * self.robots[i].radius)
            endy = int(self.robots[i].y + math.sin(radians) * self.robots[i].radius)
            diameter = self.robots[i].radius * 2
            painter.drawLine(self.robots[i].x, self.robots[i].y, endx, endy)
            painter.drawEllipse(
                self.robots[i].x - self.robots[i].radius,
                self.robots[i].y - self.robots[i].radius,
                diameter,
                diameter,
            )


App = QApplication(sys.argv)
testarena = Arena()
testarena.set_tile(2, 2, "Wall")
testarena.set_tile(3, 3, "Wall")
testarena.set_tile(2, 2, "Wall")
testarena.add_robot(BasicRobot(500, 500, 250, -90))
testarena.InitWindow()
sys.exit(App.exec())
