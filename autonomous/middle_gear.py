

from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

from components.drivetrain import DriveTrain
from components.rotator import Rotator

class MiddleGear(AutonomousStateMachine):

    MODE_NAME = 'MiddleGear'
    DEFAULT = False

    drivetrain = DriveTrain
    rotator = Rotator

    @state(first=True)
    def rotateTotarget(self):
        self.drivetrain.driveToWall()
        self.rotator.rotateTotarget()
