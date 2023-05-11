import math


class BasicRobot:
    def __init__(self, xPos, yPos, rad, dir, acceleration, turnAccel, color):
        self.x = xPos
        self.y = yPos
        self.radius = rad
        self.alpha = -dir
        self.color = color
        self.acceleration = acceleration
        self.turnAccel = turnAccel

        self.speed = 0
        self.turnSpeed = 0

    # cos(a)^2+sin(a)^2=1 that is why we use this for movement
    def move(self):
        #TODO: replace this with tick time eventually
        self.calculateSpeed(1/30)

        xVelocity = (math.cos(math.radians(self.alpha))) * self.speed
        yVelocity = (math.sin(math.radians(self.alpha))) * self.speed
        self.x = int(self.x + xVelocity)
        self.y = int(self.y + yVelocity)

    def rotate(self):
        self.calculateTurnSpeed(1/30)

        self.alpha += self.turnSpeed

    def calculateSpeed(self, deltaTime):
        self.speed += self.acceleration * deltaTime

    def calculateTurnSpeed(self, deltaTime):
        self.turnSpeed += self.turnAccel * deltaTime