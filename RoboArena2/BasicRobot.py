import math


class BasicRobot:
    def __init__(self, xPos, yPos, rad, dir):
        self.x = xPos
        self.y = yPos
        self.radius = rad
        self.alpha = -dir

    # cos(a)^2+sin(a)^2=1 that is why we use this for movement
    def move(self):
        self.x = self.x + math.cos(self.radius) ** 2
        self.y = self.y + math.sin(self.radius) ** 2
