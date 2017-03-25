

from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

class Movement(AutonomousStateMachine):


    MODE_NAME = 'Movement'
    DEFAULT = False

    myRobot = wpilib.RobotDrive
    gyro = wpilib.ADXRS450_Gyro

    @timed_state(duration=6,next_state ="stop", first=True)
    def drive_Foward(self):
        e = 45 - self.gyro.getAngle()
        self.myRobot.arcadeDrive(0, 0.1*e)

    @state
    def stop(self):
        self.myRobot.drive(0,0)
        self.done()
