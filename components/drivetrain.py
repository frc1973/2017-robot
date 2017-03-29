import wpilib

from magicbot import tunable

class DriveTrain:
    '''
        Simple magicbot drive object
    '''

    wall_p = tunable(-0.1)
    distance = tunable(0)
    analog = tunable(0)
    
    ultrasonic = wpilib.AnalogInput
    myRobot = wpilib.RobotDrive

    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, y, x):
        self.y = y
        self.x = x

    def rotate(self, x):
        self.x = x

    def driveToWall(self):
        distance = self.getDistance()
        self.y = self.wall_p*distance


    def getDistance(self):
        # returns distance in feet
        return self.ultrasonic.getAverageVoltage()/0.3

    def execute(self):
        self.myRobot.arcadeDrive(self.y, self.x, True)

        self.distance = self.getDistance()
        self.analog = self.ultrasonic.getAverageVoltage()

        self.x = 0
        self.y = 0
