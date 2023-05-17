from BasicRobot import MovementTyp


class MovementManager_:
    waveConter = 0

    def __init__(self, robot):
        self.robot = robot

    def moveInShape(self):
        Movementtyp_ = self.robot.getMovementType()

        match (Movementtyp_):
            case MovementTyp.Line:
                self.moveInLine()
            case MovementTyp.Circle:
                self.moveInCircle()
            case MovementTyp.Wave:
                self.moveInWave()
            case _:
                print("not yet defined")

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
