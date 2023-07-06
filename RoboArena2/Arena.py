import math
import sys
import configparser

from Globals import gl_arena_size_width, gl_arena_size_height , gl_tile_size , gl_tiles_amount, \
    gl_selected_arena
from BasicRobot import BasicRobot, MovementTyp
from MovementManager import MovementManager_
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QBrush, QKeyEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from Terrain import boost, fire, normal, spikes, wall, water
from Weapon import WeaponTyp


config = configparser.ConfigParser()


class Worker(QThread):
    def __init__(
        self, robot: BasicRobot, keys: dict, robots: type[BasicRobot]
    ):
        QThread.__init__(self)
        self.robot = robot
        self.keys = keys
        self.robots = robots

    def run(self):
        # function gets called at start()
        self.movementManager = MovementManager_(self.robot)

    def moveRobot(self):
        # MovementManager handles the inputs
        self.movementManager.handleInput(self.keys)

    def calculateDamage(self) -> None:
        if self.robot.weaponsCurrentlyShoot:
            xEndLine = self.getLineXEnd()
            yEndLine = self.getLineYEnd()
            lineX = self.robot.x - xEndLine
            lineY = self.robot.y - yEndLine
            lengthLine = self.LengthVector(lineX, lineY)
            lineDirectionX = self.normalizeVector(lineX, lengthLine)
            lineDirectionY = self.normalizeVector(lineY, lengthLine)
            for i in self.robots:
                if not (i is self.robot):
                    lineCircleXVector = float(
                        self.getCircleToLineX(i, xEndLine)
                    )
                    lineCircleYVector = float(
                        self.getCircleToLineY(i, yEndLine)
                    )
                    distance = self.dotProduct(
                        lineDirectionX,
                        lineDirectionY,
                        lineCircleXVector,
                        lineCircleYVector,
                    )
                    distance = self.distanceOnLine(distance, lengthLine)
                    projectionX = int(lineDirectionX * distance)
                    projectionY = int(lineDirectionY * distance)
                    closestX = xEndLine + projectionX
                    closestY = yEndLine + projectionY
                    distanceToShot = self.distanceBetweenPonts(
                        i.x, i.y, closestX, closestY
                    )
                    self.applyDamage(i, distanceToShot)

    def getLineXEnd(self) -> int:
        pi = 3.14  # calculate pi
        radians = self.robot.alpha / 180.0 * pi  # convert degrees to radians
        return int(self.robot.x + math.cos(radians) * self.robot.weapon.size)

    def getLineYEnd(self) -> int:
        pi = 3.14  # calculate pi
        radians = self.robot.alpha / 180.0 * pi  # convert degrees to radians
        return int(self.robot.y + math.sin(radians) * self.robot.weapon.size)

    def getCircleToLineX(self, target: BasicRobot, xPos: int) -> int:
        return target.x - xPos

    def getCircleToLineY(self, target: BasicRobot, yPos: int) -> int:
        return target.y - yPos

    def LengthVector(self, xVec: int, yVec: int) -> float:
        length = math.sqrt(xVec * xVec + yVec * yVec)
        return length

    def normalizeVector(self, Vec: int, length: float) -> float:
        vecAsFloat = float(Vec)
        normalized = vecAsFloat / length
        return normalized

    def dotProduct(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return x1 * x2 + y1 * y2

    def distanceOnLine(self, distance: float, length: float) -> float:
        dist = distance
        if dist < 0:
            dist = 0
        if dist > length:
            dist = length
        return dist

    def distanceBetweenPonts(self, x1: int, y1: int, x2: int, y2: int) -> int:
        dist = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        return dist

    def applyDamage(self, robot: BasicRobot, dist: int) -> None:
        didHit = robot.radius >= dist
        if didHit:
            robot.takeDamage(self.robot.weapon.damage)

    def getRobotOfThread(self) -> BasicRobot:
        return self.robot

    def stop(self) -> None:
        self.wait()


class Arena(QMainWindow):  # Erbt von QMainWindow class,
    # allows to use methods like setWindowTitle directly...
    robotSignal = pyqtSignal()
    hitSignal = pyqtSignal()
    listOfThreads = {}
    keysPressed = {}

    def __init__(self):
        super().__init__()
        self.width = gl_arena_size_width
        self.height = gl_arena_size_height
        self.tiles = [[object() for i in range(gl_tiles_amount)] for j in range(gl_tiles_amount)]
        self.robots = []
        self.title = "RoboArena"
        self.top = 0
        self.left = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_arena)
        self.timer.start(100)

        list_with_tiles = []

        config.read("config.txt")  # Path to config file
        with open(config.get("Map", "selected_map"), "r") as file:  # Opens the textfile
            content = file.read()
            content = content.replace(" ", "").replace("\n", "")
        for letter in content:  # saves every letter in a list
            list_with_tiles.append(letter)
        for y in range(0, gl_tiles_amount):  # Iterates through every possible tile
            for x in range(0, gl_tiles_amount):
                next_tile = list_with_tiles.pop(
                    0
                )  # first element is deleted and returned from the list
                if next_tile == "w":
                    self.tiles[y][x] = wall()  # The coordinate is marked with
                    # the designated terrain_type
                    # Depending on the type of the tile, different
                    # colors are used
                elif next_tile == "a":
                    self.tiles[y][x] = water()
                elif next_tile == "f":
                    self.tiles[y][x] = fire()
                elif next_tile == "s":
                    self.tiles[y][x] = spikes()
                elif next_tile == "b":
                    self.tiles[y][x] = boost()
                else:
                    self.tiles[y][x] = normal()

        # Draw arena
        self.arena_drawn = 0
        self.arena_pixmap = QPixmap(gl_arena_size_width, gl_arena_size_height)
        self.arena_pixmap.fill(Qt.transparent)
        self.render_arena()

    def render_arena(self):
        painter = QPainter(self.arena_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for y in range(0, gl_tiles_amount):  # Iterates through every possible tile
            for x in range(0, gl_tiles_amount):
                print(type(self.tiles[x][y]))
                pix = QPixmap(self.tiles[x][y].imagePath)
                pix = pix.scaledToWidth(gl_tile_size)
                painter.drawPixmap(y * gl_tile_size, x * gl_tile_size, pix)

    def get_size(self):  # method to print actual size of the arena
        print(  # split the string in two lines due to max line length
            f"The arena size is {self.width}x{self.height} pixels and "
            f"positioned top {self.top}, left {self.left}."
        )

    def update_arena(self):
        self.robotSignal.emit()
        self.hitSignal.emit()
        self.reoveOnDeath()
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
        for r in self.robots:
            for ro in self.robots:
                if ro not in r.robots:
                    r.robots.append(ro)

    def InitWindow(self):  # Displays the Arena
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    # killing the robot
    def reoveOnDeath(self) -> None:
        foundDeadrobot = False
        RobotToKill = testRobot1
        for key in self.listOfThreads:
            if key.health <= 0:
                thread = self.listOfThreads[key]
                self.killThread(thread)
                foundDeadrobot = True
                RobotToKill = key
        if foundDeadrobot:
            self.removeThreadFromDictionary(RobotToKill)
            self.removeRobotFromList(RobotToKill)

    def killThread(self, thread: Worker) -> None:
        thread.exec_
        try:
            self.robotSignal.disconnect(thread.moveRobot)
        except Exception:
            pass
        try:
            self.hitSignal.disconnect(thread.moveRobot)
        except Exception:
            pass
        thread.stop()

    def removeThreadFromDictionary(self, key: BasicRobot) -> None:
        try:
            del self.listOfThreads[key]
        except Exception:
            pass

    def removeRobotFromList(self, robot: BasicRobot) -> None:
        robotlocation = len(self.robots)
        for i in range(len(self.robots)):
            if robot is self.robots[i]:
                robotlocation = i

        if self.robots[robotlocation].health <= 0:
            del self.robots[robotlocation]

    # basic threading
    def runTask(self):
        # adds all robots to the threading dictionary
        for i in range(len(self.robots)):
            # key = i
            robot = self.robots[i]
            key = robot
            value = Worker(robot, self.keysPressed, self.robots)
            self.listOfThreads[key] = value

        # starting the threads and connecting the signals
        for i in range(len(self.listOfThreads)):
            robotOfThread = self.robots[i]
            self.robotSignal.connect(
                self.listOfThreads[robotOfThread].moveRobot
            )
            self.hitSignal.connect(
                self.listOfThreads[robotOfThread].calculateDamage
            )
            self.listOfThreads[robotOfThread].start()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keysPressed[event.key()] = True

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        self.keysPressed[event.key()] = False

    def paintEvent(self, event):  # Colors the tiles
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the pre-rendered arena pixmap onto the widget
        painter.drawPixmap(self.rect(), self.arena_pixmap)

        for i in range(len(self.robots)):  # draw robots
            painter.setPen(QPen(self.robots[i].color, 1, Qt.DashLine))
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

        for i in self.robots:
            barSize = 10
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            xPos = self.calcxPositionHealthBar(i)
            yPos = self.calcyPositionHealthBar(i, barSize)
            painter.drawRect(xPos, yPos, i.health, barSize)
            if i.weaponsCurrentlyShoot:
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                match (i.weapon.typ):
                    case WeaponTyp.hitscan:
                        endPosX = self.calcXEndHitScan(i)
                        endPosY = self.calcYEndHitScan(i)
                        painter.drawLine(i.x, i.y, endPosX, endPosY)
                    case _:
                        pass

    def calcxPositionHealthBar(self, robot: BasicRobot) -> int:
        xPos = robot.x - int(robot.health / 2)
        return xPos

    def calcyPositionHealthBar(self, robot: BasicRobot, barSize: int) -> int:
        yPos = robot.y - robot.radius - barSize
        return yPos

    def calcXEndHitScan(self, robot: BasicRobot) -> int:
        pi = 3.14  # calculate pi
        radians = robot.alpha / 180.0 * pi  # convert degrees to radians
        return int(robot.x + math.cos(radians) * robot.weapon.size)

    def calcYEndHitScan(self, robot: BasicRobot) -> int:
        pi = 3.14  # calculate pi
        radians = robot.alpha / 180.0 * pi  # convert degrees to radians
        return int(robot.y + math.sin(radians) * robot.weapon.size)


xPosition = 500
yPosition = 250
testRobot = BasicRobot(
    xPos=xPosition,
    yPos=yPosition,
    movementtype=MovementTyp.Line,
)
testRobot1 = BasicRobot(
    xPos=xPosition - 100,
    yPos=yPosition,
    movementtype=MovementTyp.Wave,
)

testRobot2 = BasicRobot(
    xPos=xPosition + 100,
    yPos=yPosition,
    movementtype=MovementTyp.Circle,
)

testRobot3 = BasicRobot(
    xPos=xPosition + 300,
    yPos=yPosition,
    movementtype=MovementTyp.Player1Control,
)
print("asss")
App = QApplication(sys.argv)
testarena = Arena()
# testarena.add_robot(testRobot)
# testarena.add_robot(testRobot1)
testarena.add_robot(testRobot2)
testarena.add_robot(testRobot3)
testarena.runTask()
testarena.InitWindow()


sys.exit(App.exec())
