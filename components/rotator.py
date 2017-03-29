from magicbot import AutonomousStateMachine, timed_state, state, tunable
import wpilib
from networktables.util import ntproperty
from components.drivetrain import DriveTrain


INF = float('inf')


class Rotator:

    enabled = ntproperty('/camera/enabled', False)
    target = ntproperty('/camera/target', (0, 0, INF))
    Px = tunable(0.1)



    drivetrain = DriveTrain
    gyro = wpilib.ADXRS450_Gyro

    def __init__(self):
        self.lasttime = 0
        self.found = False

    def rotateTotarget (self):
        self.do_rotate=True



    def execute (self):
        found, time, lasttime, offset=self.target
        ra=self.gyro.getAngle()

        if self.lasttime < time:
           self.found = found
           self.lasttime = time
           self.target = ra - offset

        if self.found:
            offset = ra-self.target
            x=self.Px*offset
            if abs(offset)<10:
                self.drivetrain.driveToWall()
