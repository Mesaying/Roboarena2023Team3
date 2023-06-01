import math
from enum import Enum

from PyQt5.QtCore import Qt

from Terrain import wall, water, fire, spikes, boost, normal


class MovementTyp(Enum):
    Line = "Line"
    Circle = "Circle"
    Wave = "Wave"


class BasicRobot:
    MAX_SPEED = 5
    MAX_TURNSPEED = 2

    def __init__(
        self,
        xPos,
        yPos,
        movementtype,
    ):
        self.x = xPos
        self.y = yPos
        self.movementtype = movementtype
        self.tiles = [[object() for i in range(100)] for j in range(100)]
        self.color = Qt.black
        self.turnAccel = 2
        self.acceleration = 10
        self.alpha = -45
        self.radius = 50
        self.speed = 0
        self.turnSpeed = 0

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

    def getMovementType(self):
        return self.movementtype

    # cos(a)^2+sin(a)^2=1 that is why we use this for movement
    def move(self):
        # TODO: replace this with tick time eventually
        self.calculateSpeed(1 / 30)

        xVelocity = (math.cos(math.radians(self.alpha))) * self.speed
        yVelocity = (math.sin(math.radians(self.alpha))) * self.speed
        colls = self.collisionDetection(self.x + xVelocity, self.y + yVelocity)
        self.x = int(colls[0])
        self.y = int(colls[1])

    def rotate(self):
        # TODO: replace this with tick time eventually
        self.calculateTurnSpeed(1 / 30)

        self.alpha += self.turnSpeed

    def rotateLeft(self):
        # TODO: replace this with tick time eventually
        self.calculateTurnSpeed(1 / 30)

        self.alpha -= self.turnSpeed

    def calculateSpeed(self, deltaTime):
        self.speed = min(
            self.speed + self.acceleration * deltaTime, self.MAX_SPEED
        )

    def calculateTurnSpeed(self, deltaTime):
        self.turnSpeed = min(
            self.turnSpeed + self.turnAccel * deltaTime, self.MAX_TURNSPEED
        )

    def collisionDetection(self, endX, endY):
        currX = self.x
        currY = self.y

        endX = round(endX)
        endY = round(endY)

        while (currY != endY) | (currX != endX):

            xDir = endX - currX
            yDir = endY - currY

            if (xDir != 0):
                xDir = math.copysign(1, xDir)

            if (yDir != 0):
                yDir = math.copysign(1, yDir)

            currX += xDir
            currY += yDir

            for x in range(int(currX - int((self.radius/10))), int(currX + math.ceil((self.radius/10)))):
                for y in range(int(currY - math.ceil((self.radius/10))), int(currY + math.ceil((self.radius/10)))):
                    #print(xDir)
                    if self.tiles[round(y/10)][round(x/10)].getCollision() != 0:
                        return (currX - xDir), (currY - yDir)

        return endX, endY
