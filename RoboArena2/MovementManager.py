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
        self.robot.tick(1, 0, (1 / 30))

    def moveInCircle(self):
        self.robot.tick(1, 1, (1 / 30))

    def moveInWave(self):
        if self.waveConter < 50:
            self.robot.tick(1, 1, (1 / 30))
            self.waveConter += 1
        else:
            self.robot.tick(1, -1, (1 / 30))
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

        moveVec = 0
        rotVec = 0

        if PressedMoveForward and not PressedMoveBack:
            moveVec += 1

        if PressedMoveBack and not PressedMoveForward:
            moveVec -= 1

        if PressedTurnLeft and not PressedTurnRight:
            rotVec -= 1

        if PressedTurnRight and not PressedTurnLeft:
            rotVec -= 1

        self.robot.tick(moveVec, rotVec, 1 / 30)
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
