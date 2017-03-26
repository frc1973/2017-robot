

from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

from components.drivetrain import DriveTrain

class MiddleGear(AutonomousStateMachine):

    MODE_NAME = 'MiddleGear'
    default = False

    drivetrain = DriveTrain

    @timed_state(duration=5, first=True)
    def driveTothewall(self):
        self.drivetrain.driveToWall()
