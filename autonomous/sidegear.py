

from magicbot import AutonomousStateMachine, timed_state, state, tunable
import wpilib

from components.drivetrain import DriveTrain
from components.rotator import Rotator

class SideGear(AutonomousStateMachine):

    drivetrain = DriveTrain
    rotator = Rotator

    turn = tunable(.73)

    def on_enable(self):
        super().on_enable()
        self.p = wpilib.Timer()
        self.p.start()

    def execute(self):
        super().execute()
        if self.p.hasPeriodPassed(0.3):
            self.logger.info("Distance: %0.3f", self.drivetrain.getDistance())

    @timed_state(duration=1.5, first=True, next_state='initialRotate')
    def drive_forward(self):
        self.drivetrain.move(-0.7, 0)


    @timed_state(duration=4, next_state='nextRotate')
    def initialRotate (self):
        self.drivetrain.move(0, self.sign*self.turn)
        self.rotator.rotateTotarget()
        if self.rotator.found:
            self.next_state('detect')

    @timed_state(duration=4, next_state='initialRotate')
    def nextRotate (self):
        self.drivetrain.move(0, self.sign*-self.turn)
        self.rotator.rotateTotarget()
        if self.rotator.found:
            self.next_state('detect')

    @timed_state(duration=3, next_state='drive_to_the_wall')
    def detect(self):
        self.drivetrain.move(0, self.sign*self.turn)
        self.rotator.rotateTotarget()
        if not self.rotator.found:
            self.next_state('initialRotate')

    @state
    def drive_to_the_wall(self):
        self.rotator.rotateTotarget()
        self.drivetrain.driveToWall()

class LeftSideGear (SideGear):
    MODE_NAME = 'LeftSideGear'
    DEFAULT = False
    sign = 1



class RightSideGear (SideGear):
    MODE_NAME = 'RightSideGear'
    DEFAULT = True

    sign = -1
