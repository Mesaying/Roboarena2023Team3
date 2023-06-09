from BasicRobot import BasicRobot, MovementTyp
from PyQt5.QtCore import Qt


class MovementManager_:
    waveConter = 0
    weaponsCurrentlyShoot = False
    ticksToNextShoot = 0

    def __init__(self, robot: BasicRobot):
        self.robot = robot

    def handleInput(self, keys: dict):
        Movementtyp_ = self.robot.getMovementType()

        match (Movementtyp_):
            case MovementTyp.Line:
                self.moveInLine()
            case MovementTyp.Circle:
                self.moveInCircle()
            case MovementTyp.Wave:
                self.moveInWave()
            case MovementTyp.Player1Control:
                self.handleInputPlayer1(keys)
            case _:
                print("MovementType not yet defined")

    def moveInLine(self):
        self.robot.move()

    def moveInCircle(self):
        self.robot.move()
        self.robot.rotate()

    def moveInWave(self):
        if self.waveConter < 50:
            self.robot.move()
            self.robot.rotate()
            self.waveConter += 1
        else:
            self.robot.move()
            self.robot.rotateLeft()
            self.waveConter += 1
            self.waveConter = self.waveConter % 100

    def handleInputPlayer1(self, keys: dict):
        self.reduceTimerToShoot()
        moveForward = Qt.Key.Key_W
        moveBack = Qt.Key.Key_S
        turnLeft = Qt.Key.Key_A
        turnRight = Qt.Key.Key_D
        shootWeapon = Qt.Key.Key_F
        PressedMoveForward = moveForward in keys and keys[moveForward]
        PressedMoveBack = moveBack in keys and keys[moveBack]
        PressedTurnLeft = turnLeft in keys and keys[turnLeft]
        PressedTurnRight = turnRight in keys and keys[turnRight]
        PressedShootWeapon = shootWeapon in keys and keys[shootWeapon]

        if PressedMoveForward and not PressedMoveBack:
            self.robot.move()

        if PressedMoveBack and not PressedMoveForward:
            self.robot.moveBack()

        if PressedTurnLeft and not PressedTurnRight:
            self.robot.rotateLeft()

        if PressedTurnRight and not PressedTurnLeft:
            self.robot.rotate()

        if PressedShootWeapon and self.ticksToNextShoot < 1:
            self.weaponsCurrentlyShoot = True
            self.ticksToNextShoot = self.robot.weapon.ticksToNextShoot
            self.robot.weapon.shootWeapon()
        else:
            self.weaponsCurrentlyShoot = False

        self.robot.weaponsCurrentlyShoot = self.weaponsCurrentlyShoot

    def reduceTimerToShoot(self) -> None:
        if self.ticksToNextShoot > 0:
            self.ticksToNextShoot -= 1
