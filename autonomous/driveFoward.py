

from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

class DriveFoward(AutonomousStateMachine):

    MODE_NAME = 'Drive Foward'
    DEFAULT = False

    myRobot = wpilib.RobotDrive

    @timed_state(duration=3,next_state ="stop", first=True)
    def drive_Foward(self):
        self.myRobot.drive(-0.5,0)

    @state
    def stop(self):
        self.myRobot.drive(0,0)
        self.done()
