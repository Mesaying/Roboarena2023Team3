import math


class BasicRobot:
    def __init__(self, xPos, yPos, rad, dir, speed, color):
        self.x = xPos
        self.y = yPos
        self.radius = rad
        self.alpha = -dir
        self.color = color
        self.speed = speed

    # cos(a)^2+sin(a)^2=1 that is why we use this for movement
    def move(self):
        xVelocity = (math.cos(math.radians(self.alpha))) * self.speed
        yVelocity = (math.sin(math.radians(self.alpha))) * self.speed
        self.x = int(self.x + xVelocity)
        self.y = int(self.y + yVelocity)
