from BasicRobot import *


class Destroyer(BasicRobot):
    def __init__(self, xPos, yPos, movementtype):
        super().__init__(xPos, yPos, movementtype)
        self.health = 50
        self.speed = 10


class Tank(BasicRobot):
    def __init__(self, xPos, yPos, movementtype):
        super().__init__(xPos, yPos, movementtype)
        self.health = 100
        self.speed = 5


class Velocity(BasicRobot):
    def __init__(self, xPos, yPos, movementtype):
        super().__init__(xPos, yPos, movementtype)
        self.health = 75
        self.speed = 15
