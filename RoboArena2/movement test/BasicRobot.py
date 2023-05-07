class BasicRobot:
    def __init__(self, xPos, yPos, rad, dir):
        self.x = xPos
        self.y = yPos
        self.radius = rad
        self.alpha = -dir

    def move(self):
        self.x = self.x + 2
        self.y = self.y + 2
