from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
import sys
import math
class BasicRobot:


    def __init__(self, xPos, yPos, rad, dir):
        self.x = xPos
        self.y = yPos
        self.radius = rad
        self.alpha = -dir

    def move(self):
        self.x = self.x+2
        self.y = self.y+2
