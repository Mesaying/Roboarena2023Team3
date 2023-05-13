import math


class BasicRobot:
    MAX_SPEED = 5
    MAX_TURNSPEED = 2

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
        # TODO: replace this with tick time eventually
        self.calculateSpeed(1 / 30)

        xVelocity = (math.cos(math.radians(self.alpha))) * self.speed
        yVelocity = (math.sin(math.radians(self.alpha))) * self.speed
        self.x = int(self.x + xVelocity)
        self.y = int(self.y + yVelocity)

    def rotate(self):
        # TODO: replace this with tick time eventually
        self.calculateTurnSpeed(1 / 30)

        self.alpha += self.turnSpeed

    def calculateSpeed(self, deltaTime):
        self.speed = min(
            self.speed + self.acceleration * deltaTime, self.MAX_SPEED
        )

    def calculateTurnSpeed(self, deltaTime):
        self.turnSpeed = min(
            self.turnSpeed + self.turnAccel * deltaTime, self.MAX_TURNSPEED
        )
