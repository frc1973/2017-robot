
import math
import wpilib

from magicbot import tunable

class DriveTrain:
    '''
        Simple magicbot drive object
    '''

    wall_p = tunable(-15)
    distance = tunable(0)
    analog = tunable(0)

    tx = tunable(0)
    ty = tunable(0)
    offset = tunable(1.3)

    MaxY = tunable(0.8)

    ultrasonic = wpilib.AnalogInput
    myRobot = wpilib.RobotDrive

    def __init__(self):
        self.x = 0
        self.y = 0
# distance is .98
    def move(self, y, x):
        self.y = y
        self.x = x

    def rotate(self, x):
        self.x = x

    def driveToWall(self):

        distance = self.getDistance()
        distance = max(min(14.0, distance), -self.offset)

        if abs(distance)<0.2:
            self.y = 0
        else:

            y = self.wall_p*distance

            scaled_y = 0.5 + abs(y)/30.0
            scaled_y = math.copysign(scaled_y, y)

            scaled_y = max(min(self.MaxY, scaled_y), -self.MaxY)

            self.y = scaled_y



    def getDistance(self):
        # returns distance in feet
        return (self.ultrasonic.getAverageVoltage()/0.3) - self.offset

    def execute(self):
        self.tx = self.x
        self.ty = self.y
        self.myRobot.arcadeDrive(self.y, self.x, True)

        self.distance = self.getDistance()
        self.analog = self.ultrasonic.getAverageVoltage()

        self.x = 0
        self.y = 0
