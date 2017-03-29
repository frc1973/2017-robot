
import wpilib
from networktables.util import ntproperty
from components.drivetrain import DriveTrain

from magicbot import StateMachine, state, tunable

INF = float('inf')


class Rotator(StateMachine):

    enabled = ntproperty('/camera/enabled', False)
    target = ntproperty('/camera/target', (0, 0, INF))
    Px = tunable(0.1)
    MaxX = tunable(0.6)
    
    #rotate_x = tunable(0)
    #offset = tunable(0)

    drivetrain = DriveTrain
    gyro = wpilib.ADXRS450_Gyro

    def __init__(self):
        self.lasttime = 0
        self.found = False

    def rotateTotarget (self):
        self.engage()

    @state(first=True)
    def doit(self, initial_call):
        
        if initial_call:
            self.enabled = True
        
        found, time, offset=self.target
        ra=self.gyro.getAngle()

        # do I have new information?
        if self.lasttime < time:
            # update the information
            self.found = found > 0
            self.targetangle = ra - offset

        if self.found:
            offset = ra-self.targetangle
            x = self.Px*offset
            
            x = max(min(self.MaxX, x), -self.MaxX)
            
            #self.offset = offset
            #self.rotate_x = x
            
            self.drivetrain.rotate(x)

            if abs(offset)<10:
                self.drivetrain.driveToWall()
                
        #else:
        #    self.offset = 0
        #    self.rotate_x = 0
    
    def done(self):
        super().done()
        self.enabled = False
        #self.offset = 0
        #self.rotate_x = 0
