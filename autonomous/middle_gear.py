

from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

from components.drivetrain import DriveTrain

class MiddleGear(AutonomousStateMachine):

    MODE_NAME = 'Drive Forward'
    default = False
    
    drivetrain = DriveTrain
    
    def deriveTothewall (self):
        self.derive_forward()
    
        
        